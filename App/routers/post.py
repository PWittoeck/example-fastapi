
from datetime import datetime
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from ..import models, schemas,utils, oauth2
from ..database import engine, get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts'] # tag for fastapi doc
)

# part 1 : user data 
# posts to manage data to the sql database

@router.get("/", response_model=List[schemas.PostOut])

#def get_posts():
def get_posts(db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0,
                  search: Optional[str] = ""):

#     cursor.execute("""SELECT * FROM posts """)
#     posts = cursor.fetchall()
     print(limit)
#     get posts from all users !!!
#     posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # type: ignore # 
     
     posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
          models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(
          models.Post.title.contains(search)).limit(limit).offset(skip).all()
     
#     get only posts from current user
#     posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() # type: ignore #  

#     return {"data": posts}
     return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):

     #        cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """,
     #                       (post.title, post.content, post.published))
     # get message back 
     #       new_post = cursor.fetchone() 
     # save cmd to the database  
     #       conn.commit() 
     #    print(**post.dict())    
     #   

     new_post = models.Post(owner_id = current_user.id, **post.dict()) # type: ignore # 
     db.add(new_post)
     db.commit()
     db.refresh(new_post)

     return new_post


# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail": post}
# title str, content str


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
#     cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
#     post = cursor.fetchone()
#     post = db.query(models.Post).filter(models.Post.id == id).first()

     post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.
     Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    # get all posts 
     if not post:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"post with id: {id} was not found")
     
     # get posts depends on user id
     # if post.owner_id != current_user.id:
     #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
     #                         detail=f"Not authorized to perform requested action")
     
     return post


# deleting post
# find the index in the array that has required id

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):

#      cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
#      deleted_post = cursor.fetchone
#      conn.commit()
     
     post_query = db.query(models.Post).filter(models.Post.id == id)

     post = post_query.first()

     if post == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                               detail=f"post with id: {id} does not exist") 
     
     if post.owner_id != oauth2.get_current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                              detail=f"Not authorized to perform requested action")

     post_query.delete(synchronize_session = False)
     db.commit()

     return Response(status_code = status.HTTP_204_NO_CONTENT)
   

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):

     # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING  * """,
     #                 (post.title, post.content, post.published, str(id)))
     
     # updated_post = cursor.fetchone()
     # conn.commit()

     post_query = db.query(models.Post).filter(models.Post.id == id)
     post = post_query.first()

     if post == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                               detail=f"post with id: {id} does not exist") 
     
     if post.owner_id != current_user.id: # type: ignore # 
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                              detail=f"Not authorized to perform requested action")
     
     post_query.update(updated_post.dict(), synchronize_session=False)
     
     db.commit()

     return post_query.first()




from ast import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from httpx import post
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import database, schemas, models, oauth2
from..database import get_db
from . import auth
from typing import Optional



router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)




# # @router.get('/', response_model=list[schemas.PostResponse])
# @router.get('/', response_model=List[schemas.VoteCount])
# def test_it(db: Session = Depends(get_db), user_id: id = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0, search: Optional[str] = ''):

#     # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

#     join_posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
#     result = [schemas.VoteCount(post=post, vote_count=vote_count) for post, vote_count in join_posts]
    
#     schema = schemas.VoteCount.schema()
    
#     return JSONResponse(content=result, schema=schema)

@router.get('/', response_model=list[schemas.PostOut])
def test_it(db: Session = Depends(get_db), user_id: id = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0, search: Optional[str] = ''):

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()


    return results


@router.post("/", response_model=schemas.PostResponse)
def make_post(post: schemas.PostMake, db: Session = Depends(get_db), owner_id: id = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id = owner_id.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    
    # response_post = schemas.PostResponse(
    #     id=new_post.id,
    #     title=new_post.title,
    #     content=new_post.content,
    #     published=new_post.published,
    #     user_id=owner_id.id
    #     )
    return  new_post


@router.get("/{id}", response_model=list[schemas.PostOut])
def get_postid(id:int, db: Session = Depends(get_db), user_id: id = Depends(oauth2.get_current_user)):
    get_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not exist")
    
    
    # response_post = schemas.PostResponse(
    #     id= get_post.id,
    #     title=get_post.title,
    #     content=get_post.content,
    #     published=get_post.published,
    #     user_id=get_post.user_id
    # )
    return [get_post]



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), user_id: id = Depends(oauth2.get_current_user)):
    
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()


    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not exist")


    if deleted_post.user_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

    db.delete(deleted_post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}")
def update_post(id: int, updated_post: schemas.PostBase, db: Session = Depends(get_db), user_id: id = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not exist")

    if post.user_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

    
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    db.refresh(post)
    db.close()

    # return post_query.first()
    # response_post = schemas.PostResponse(
    #     title=post_query.first().title,
    #     content=post_query.first().content,
    #     published=post_query.first().published,
    #     user_id=post_query.first().user_id    )
    return  post_query.first()

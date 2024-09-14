from typing import List
from fastapi import FastAPI, Depends, HTTPException

from schema import UserGet, PostGet, FeedGet
from table_user import User
from table_post import Post
from table_feed import Feed

from database import SessionLocal
from sqlalchemy import desc, func
from sqlalchemy.orm import Session


app = FastAPI()

def get_db():
    with SessionLocal() as db:
        return db
@app.get("/user/{id}", response_model=UserGet)
def get_user_table(id: int, db: Session = Depends(get_db)):
    result = db.query(User).filter(User.id == id).first()
    if not result:
        raise HTTPException(404, "not such user")
    return result


@app.get("/post/{id}", response_model=PostGet)
def get_post_table(id: int, db: Session = Depends(get_db)):
    result = db.query(Post).filter(Post.id == id).first()
    if not result:
        raise HTTPException(404, "not such post")
    return result


@app.get("/user/{id}/feed", response_model=List[FeedGet])
def get_action_user(id:int, limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(Feed).filter(Feed.user_id == id).order_by(desc(Feed.time)).limit(limit).all()
    if not result:
        raise HTTPException(200, [])
    return result


@app.get("/post/{id}/feed", response_model=List[FeedGet])
def get_action_post(id:int, limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(Feed).filter(Feed.post_id == id).order_by(desc(Feed.time)).limit(limit).all()
    if not result:
        raise HTTPException(200, [])
    return result

@app.get("/post/recommendations/", response_model=List[PostGet])
def get_top_liked_posts(limit: int=10, db: Session = Depends(get_db)):
    result = (
        db.query(Post)
        .select_from(Feed)
        .filter(Feed.action == "like")
        .join(Post)
        .group_by(Post.id)
        .order_by(desc(func.count(Feed.post_id)))
        .limit(limit)
        .all()
    )

    res_list = [PostGet(id=post.id, text=post.text, topic=post.topic) for post in result]
    return res_list

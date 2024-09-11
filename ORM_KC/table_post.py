from database import Base, SessionLocal
from sqlalchemy import Column, Integer, String, desc
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "post"
    __table_args__ = {"schema": "public"}
    id = Column(Integer, primary_key=True, name="id")

    text = Column(String, name="text")
    topic = Column(String, name="topic")


if __name__ == "__main__":
    session = SessionLocal()
    result = session.query(Post).filter(Post.topic == "business").order_by(desc(Post.id)).limit(10).all()
    res_list = [post.id for post in result]
    print(res_list)
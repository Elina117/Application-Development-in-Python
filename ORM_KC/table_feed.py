from database import Base, SessionLocal
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from table_user import User
from table_post import Post


class Feed(Base):
    __tablename__ = "feed_action"
    __table_args__ = {"schema":"public"}

    user_id = Column(Integer, ForeignKey("User.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("Post.id"), primary_key=True)
    action = Column(String)
    time = Column(DateTime)
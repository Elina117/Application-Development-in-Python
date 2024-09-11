from sqlalchemy import Column, Integer, String, func, desc
from database import Base, SessionLocal
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)

    gender = Column(Integer)
    age = Column(Integer)
    country = Column(String)
    city = Column(String)
    exp_group = Column(Integer)
    os = Column(String)
    source = Column(String)


if __name__ == "__main__":
    session = SessionLocal()
    result = ((session.query(
        User.country, User.os, func.count().label('count')
        ).filter(User.exp_group == 3)
        .group_by(User.country, User.os))
              .having(func.count() > 100)
              .order_by(desc(func.count()))
              .all())
    res_list = [(country, os, count) for country, os, count in result]
    print(res_list)

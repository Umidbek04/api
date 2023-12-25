from mysqlx import Column
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    content = Column(String(100), nullable=False)
    published = Column(Boolean, nullable=False, server_default="1")

    made_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")

    phone_number = Column(String(100), nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    made_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = 'votes'

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    




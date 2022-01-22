from datetime import timedelta
from typing import Any
from sqlalchemy import BigInteger, Column, ForeignKey, Interval, String
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
  id: Any
  __name__: Any

  @declared_attr
  def __tablename__(self) -> str:
    return self.__name__.lower()

class Guild(Base):
    __tablename__ = 'guilds'
    guild_id = Column(BigInteger, primary_key=True)
    guild_name = Column(String)
    notify_channel_id = Column(BigInteger, nullable=True)

class User(Base):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    user_name = Column(String)

class Joining(Base):
    __tablename__ = 'joining'
    guild_id = Column(BigInteger, ForeignKey('guilds.guild_id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)

class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_name = Column(String)
    user_id = Column(BigInteger, ForeignKey('users.user_id', onupdate='CASCADE', ondelete='CASCADE'))
    duration = Column(Interval, nullable=True, default=timedelta)

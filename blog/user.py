from sqlalchemy import (Column, DateTime, 
                        String, Integer, 
                        ForeignKey, func, Text)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

import bcrypt


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

    def check_password(self, raw_password):
        print(raw_password.encode('utf-8'), self.password.encode('utf-8'))
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    posted_at = Column(DateTime, default=func.now())
    author_id = Column(Integer, ForeignKey('user.id'))
    # Use cascade='delete,all' to propagate the deletion of a Department onto its Employees
    author = relationship(
        User,
        backref=backref('employees',
                        uselist=True,
                        cascade='delete,all'))


from sqlalchemy import create_engine

engine = create_engine('postgresql://sminc:southAndTea@/sminc', echo=True)

from sqlalchemy.orm import sessionmaker

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

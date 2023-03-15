
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column,String,Integer,Float,ForeignKey,DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import sessionmaker



engine = create_engine('sqlite:///quiz.db')
Base = declarative_base()



# we will create our users table

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(50),unique=True)
    name = Column(String(50))
    password = Column(String(64))
    group = Column(Integer,default=1)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)

class Quiz(Base):
    __tablename__ = 'quiz'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    a = Column(String)
    b = Column(String)
    c = Column(String)
    d = Column(String)
    answer = Column(String)

class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    option1 = Column(String)
    option2 = Column(String)
    option3 = Column(String)
    option4 = Column(String)
    answer = Column(String)

    def __repr__(self) -> str:
        return f"{self.id}|{self.name}|{self.group}"






if __name__ == "__main__":
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind = engine)
    session = Session()
    session.add_all([
        Quiz(question = 'What is the full form of DBMS?', a = 'Data of Binary Management System',b = 'Database Management System', c = 'Database Management Service', d = 'Data Backup Management System', answer = 'Database Management System'),
        Quiz(question = 'What is a database?', a = 'Organized collection of information that cannot be accessed, updated, and managed', b = 'Collection of data or information without organizing', c = 'Organized collection of data or information that can be accessed, updated, and managed', d = 'Organized collection of data that cannot be updated', answer = 'Organized collection of data or information that can be accessed, updated, and managed'),
        Quiz(question = 'What is DBMS?', a = 'DBMS is a collection of queries', b = 'DBMS is a high-level language',c = 'DBMS is a programming language', d = 'DBMS stores, modifies and retrieves data', answer = 'DBMS stores, modifies and retrieves data'),
        Quiz(question = 'How can we describe an array in the best possible way?', a = 'The Array shows a hierarchical structure.', b ='Arrays are immutable.', c ='Container that stores the elements of similar types', d ='The Array is not a data structure',answer='Container that stores the elements of similar types'),
    ])
    session.commit()
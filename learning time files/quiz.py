from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///quiz.db')
Base = declarative_base()

class Quiz(Base):
    __tablename__ = 'quiz'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    a = Column(String)
    b = Column(String)
    c = Column(String)
    d = Column(String)
    answer = Column(String)


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()
session.add_all([
    Quiz(question = 'What is the full form of DBMS?', a = 'Data of Binary Management System',b = 'Database Management System', c = 'Database Management Service', d = 'Data Backup Management System', answer = 'Database Management System'),
    Quiz(question = 'What is a database?', a = 'Organized collection of information that cannot be accessed, updated, and managed', b = 'Collection of data or information without organizing', c = 'Organized collection of data or information that can be accessed, updated, and managed', d = 'Organized collection of data that cannot be updated', answer = 'Organized collection of data or information that can be accessed, updated, and managed'),
    Quiz(question = 'What is DBMS?', a = 'DBMS is a collection of queries', b = 'DBMS is a high-level language',c = 'DBMS is a programming language', d = 'DBMS stores, modifies and retrieves data', answer = 'DBMS stores, modifies and retrieves data'),
    Quiz(question = 'How can we describe an array in the best possible way?', a = 'The Array shows a hierarchical structure.', b ='Arrays are immutable.', c ='Container that stores the elements of similar types', d ='The Array is not a data structure',answer='Container that stores the elements of similar types'),
    
    
    ]
)



session.commit()

Base.metadata.create_all(engine)
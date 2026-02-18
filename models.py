
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#defining the table 

class Employee(db.Model):
        #__tablename__ = 'importanttable'

    id = db.Column(db.Integer, primary_key=True)            
    emp_name = db.Column("name", db.String(100), nullable=False) # maps to DB column "name"
    emp_age = db.Column("age", db.Integer, nullable=False,default=0)        # maps to DB column "age"
    username= db.Column(db.String(50),nullable=False,unique=True)
    password= db.Column(db.String(50),nullable=False)
## to solve the issue nullable we used this before using above
#     username = db.Column(db.String(50), nullable=True, unique=True)
#     password = db.Column(db.String(50), nullable=True)

    created_at= db.Column(db.DateTime, default=datetime.now)
    updated_at= db.Column(db.DateTime, default=datetime.now , onupdate=True)
    

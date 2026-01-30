from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#defining the table 
class Employee(db.Model):
    #__tablename__ = 'importanttable'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    age = db.Column(db.Integer,nullable=False)




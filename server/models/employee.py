from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from models.init import db

class Employee(db.Model, SerializerMixin):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    approved = db.Column(db.Boolean, default=False) 
    role = db.Column(db.String, default='Employee')
    profile_picture = db.Column(db.String(), default="https://www.westernunion.com/staticassets/content/dam/wu/jm/responsive/send-money-in-person-from-jamaica-resp.png")
    approved_assets = db.relationship('ApprovedAsset', back_populates='employee', cascade=('all', 'delete-orphan'))
    requests = db.relationship('Request', back_populates='employee', cascade=('all','delete-orphan'))
    
    
    def __repr__(self):
        return f"<Employee {self.username}>"
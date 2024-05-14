from sqlalchemy_serializer import SerializerMixin
from models.init import db

class Admin(db.Model, SerializerMixin):
    __tablename__ = 'admin'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Increased length
    email = db.Column(db.String(255), unique=True, nullable=False)  # Increased length
    auth_code = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String, default='Admin')
    
    
    def __repr__(self):
        return f"<Admin {self.username}>"


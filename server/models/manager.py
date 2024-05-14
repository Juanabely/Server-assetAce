from sqlalchemy_serializer import SerializerMixin
from models.init import db

class Manager(db.Model, SerializerMixin):
    __tablename__ = 'managers'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255))  # Increased length
    email = db.Column(db.String(255), unique=True,  nullable=False) # Increased length
    approved = db.Column(db.Boolean, default=False) 
    profile_picture = db.Column(db.String, default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHdenPX0pPOYadxrz5aH1aGRApYCtQ7ctXP3P0P8XPrw&s")
    role = db.Column(db.String, default='Manager')
    
    
    def __repr__(self):
        return f"<Manager {self.username}>"


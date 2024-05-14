from sqlalchemy_serializer import SerializerMixin
from models.init import db

class Request(db.Model, SerializerMixin):
    __tablename__ = 'requests'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    status = db.Column(db.String(20), default='pending')
    
    reason = db.Column(db.String(255),  nullable=False) # Increased length
    quantity = db.Column(db.Boolean, default=False) 
    urgency = db.Column(db.String(100), default='moderate urgency')

    asset = db.relationship('Asset', back_populates='requests')  # Increased length
    employee = db.relationship('Employee', back_populates='requests')
    
    
    def __repr__(self):
        return f"<Request {self.username}>"


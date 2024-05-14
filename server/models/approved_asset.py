from sqlalchemy_serializer import SerializerMixin
from models.init import db

class ApprovedAsset(db.Model, SerializerMixin):
    __tablename__ = 'approved_assets'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    quantity = db.Column(db.Integer)
    employee = db.relationship('Employee', back_populates='approved_assets')
    asset = db.relationship('Asset', back_populates='approved_assets')
    # name = db.Column(db.String(20), unique=True)
    # category = db.Column(db.String(255), nullable=False)  # Increased length
    # condition = db.Column(db.String(255), nullable=False) # Increased length
    # imma = db.Column(db.Boolean, default=False) 

    
    
    def __repr__(self):
        return f"<Manager {self.quantity}>"


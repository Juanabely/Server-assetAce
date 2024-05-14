from sqlalchemy_serializer import SerializerMixin
from models.init import db

class Asset(db.Model, SerializerMixin):
    __tablename__ = 'assets'
    
    id = db.Column(db.Integer, primary_key=True)
    stock = db.Column(db.Integer)
    name = db.Column(db.String(100), unique=True)
    category = db.Column(db.String(255), nullable=False)  # Increased length
    condition = db.Column(db.String(255), nullable=False) # Increased length
    image_url = db.Column(db.String(700), default="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bGFwdG9wfGVufDB8fDB8fHww")
    
    approved_assets = db.relationship('ApprovedAsset', back_populates='asset', cascade=('all','delete-orphan')) 
    requests = db.relationship('Request',back_populates='asset')
    
    
    def __repr__(self):
        return f"<Asset {self.name}>"


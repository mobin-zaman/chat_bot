from db import db
from sqlalchemy.dialects.mysql import BIGINT


class Product(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    img_url = db.Column(db.String(255), nullable=False)
    category_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('category.id'), nullable=False)

    def __init__(self, name, description, price, img_url):
        self.name = name
        self.description = description
        self.price = price
        self.img_url = img_url

    def commit(self):
        """saves the object in database"""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Products {}{}{}{}>'.format(self.id, self.name, self.description, self.price)

    @classmethod
    def get_description(cls, id) -> "Product.description":
        return cls.query.get(id).description
    
    @classmethod
    def get_category_id(cls,id) -> "Product.category_id":
        return cls.query.get(id).category_id

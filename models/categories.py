from db import db
from sqlalchemy.dialects.mysql import BIGINT
from models.products import Product


class Category(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)
    img_url = db.Column(db.String(256), unique=False, nullable=False)
    # TODO: need to find out what does lazy=dynamic means
    products = db.relationship('Product', backref='products', lazy='dynamic')
    # FIXME: products of each categories should added as db.relationship

    def __init__(self, name, description, img_url):
        self.name = name
        self.description = description
        self.img_url = img_url

    def commit(self):
        """saves the object in database"""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Category {}>'.format(self.id, self.name, self.thumb_urls)

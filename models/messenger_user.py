from db import db

from sqlalchemy.dialects.mysql import BIGINT

class MessengerUser(db.Model):
    id=db.Column(BIGINT(unsigned=True),primary_key=True)
    sender_id=db.Column(db.String(255),nullable=False,unique=True)


    #TODO: needs to add other infos 

    def __init__(self,sender_id):
        self.sender_id=sender_id


        user=MessengerUser.query.filter_by(sender_id=self.sender_id).first()

        if user:
            print("already added")
        else:
            db.session.add(self)
            db.session.commit()
    
    @classmethod
    def get_id(cls,sender_id):
        user=cls.query.filter_by(sender_id=sender_id).first()
        return user.id


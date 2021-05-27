from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class MemberModel(db.Model):
    __tablename__ = "table"
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer(), unique=True)
    name = db.Column(db.String())
    relation = db.Column(db.String())
    image = db.Column(db.String(20), nullable = False)

    def __init__(self,member_id,name, relation, image):
        self.member_id = member_id
        self.name = name
        self.relation = relation
        self.image = image

    def __repr__(self):
        return f"{self.name}:{self.relation}:{self.image}"


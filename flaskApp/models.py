from views import db, app
from flask_login import UserMixin, LoginManager
login_manager = LoginManager()

@login_manager.user_load
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Document, UserMixin):
    id = db.IntegerField()
    username = db.StringField(required=True)
    email = db.StringField(max_length=120)
    password = db.StringField(max_length=50)
    image_file = db.ImageField(required = True)
    
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Members(db.Document):
    id = db.IntegerField()
    name = db.StringField(required=True)
    relation = db.StringField(required=True)
    image_file = db.ImageField(required=True)
from app import app
from models import db, User

with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"Username: {user.username}, Hashed Password: {user.password}")

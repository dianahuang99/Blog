"""Seed file to make sample data for pets db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
xuanyi = User(first_name='Xuan', last_name="Yi", image_url='https://kpopping.com/documents/20/1/1365/Wu_Xuanyi_Birthday_2021_1.jpeg?v=d965b')

meiqi = User(first_name='Mei', last_name="Qi", image_url='https://www.dailycpop.com/wp-content/uploads/2021/06/meng-meiqi.png')

mimi = User(first_name='Li', last_name="Ziting", image_url='https://pbs.twimg.com/media/DhUiHwwVAAAbMhD.jpg')

# Add new objects to session, so they'll persist
db.session.add(xuanyi)
db.session.add(meiqi)
db.session.add(mimi)

# Commit--otherwise, this never gets saved!
db.session.commit()

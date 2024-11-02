from . import db
from flask_login import UserMixin
from datetime import datetime

# User model for authentication
class User(db.Model, UserMixin):
    __tablename__ = 'user'  # Explicitly define table name

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)  # Email as the unique identifier
    username = db.Column(db.String(150), unique=True, nullable=False, index=True)  # Username field
    password = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Track user creation date
    posts = db.relationship('Post', backref='author', lazy=True)  # Relationship to posts
    images = db.relationship('Image', backref='uploader', lazy=True)  # Relationship to images

    def __repr__(self):
        return f'<User {self.email}>'  # Display email for clarity

# Post model for user posts in the forum
class Post(db.Model):
    __tablename__ = 'post'  # Explicitly define table name

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)  # Optional: add title field
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)  # Soft delete flag

    def __repr__(self):
        return f'<Post {self.title} by {self.author.email}>'  # Display author's email for clarity

# Image model for uploaded images
class Image(db.Model):
    __tablename__ = 'image'  # Explicitly define table name

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(100))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Optional: link images to user
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))  # Optional: link images to post

    def __repr__(self):
        return f'<Image {self.filename}>'

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    shares = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Milestone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=True) # 食材分類
    ingredients = db.Column(db.Text, nullable=False)
    utensils = db.Column(db.String(100), nullable=True) # 使用器具
    temp = db.Column(db.String(50), nullable=True) # 烹調溫度
    time = db.Column(db.String(50), nullable=True) # 烹調時間
    instructions = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=True) # 改成 Text 以支援 Base64 或長網址
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

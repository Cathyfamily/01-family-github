from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Stock, Milestone, Recipe
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-for-session'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# --- Authentication ---
APP_PASSWORD = 'family123'  # 預設單一登入密碼

@app.before_request
def require_login():
    allowed_routes = ['login', 'static']
    if request.endpoint not in allowed_routes and 'logged_in' not in session:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == APP_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('密碼錯誤，請再試一次。')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    stocks = Stock.query.all()
    milestones = Milestone.query.order_by(Milestone.date.desc()).all()
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return render_template('index.html', stocks=stocks, milestones=milestones, recipes=recipes)

# --- Stock Routes ---
@app.route('/add_stock', methods=['POST'])
def add_stock():
    symbol = request.form.get('symbol')
    name = request.form.get('name')
    shares = float(request.form.get('shares'))
    purchase_price = float(request.form.get('purchase_price'))
    
    new_stock = Stock(symbol=symbol, name=name, shares=shares, purchase_price=purchase_price)
    db.session.add(new_stock)
    db.session.commit()
    return redirect(url_for('index', tab='stocks'))

@app.route('/delete_stock/<int:id>', methods=['POST'])
def delete_stock(id):
    stock = Stock.query.get_or_404(id)
    db.session.delete(stock)
    db.session.commit()
    return redirect(url_for('index', tab='stocks'))

# --- Milestone Routes ---
@app.route('/add_milestone', methods=['POST'])
def add_milestone():
    title = request.form.get('title')
    description = request.form.get('description')
    date_str = request.form.get('date')
    image_url = request.form.get('image_url')
    
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    new_milestone = Milestone(title=title, description=description, date=date_obj, image_url=image_url)
    db.session.add(new_milestone)
    db.session.commit()
    return redirect(url_for('index', tab='milestones'))

@app.route('/delete_milestone/<int:id>', methods=['POST'])
def delete_milestone(id):
    milestone = Milestone.query.get_or_404(id)
    db.session.delete(milestone)
    db.session.commit()
    return redirect(url_for('index', tab='milestones'))

# --- Recipe Routes ---
@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    name = request.form.get('name')
    ingredients = request.form.get('ingredients')
    instructions = request.form.get('instructions')
    image_url = request.form.get('image_url')
    
    new_recipe = Recipe(name=name, ingredients=ingredients, instructions=instructions, image_url=image_url)
    db.session.add(new_recipe)
    db.session.commit()
    return redirect(url_for('index', tab='recipes'))

@app.route('/delete_recipe/<int:id>', methods=['POST'])
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('index', tab='recipes'))

if __name__ == '__main__':
    app.run(debug=True)

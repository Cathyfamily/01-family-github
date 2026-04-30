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
    new_milestone = Milestone(
        title=title, 
        description=description, 
        date=date_obj, 
        image_url=image_url # 接收 Base64 格式
    )
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
    recipe_type = request.form.get('type')
    ingredients = request.form.get('ingredients')
    utensils = request.form.get('utensils')
    temp = request.form.get('temp')
    time = request.form.get('time')
    instructions = request.form.get('instructions')
    image_url = request.form.get('image_url') # 接收 Base64 格式
    
    new_recipe = Recipe(
        name=name, 
        type=recipe_type,
        ingredients=ingredients, 
        utensils=utensils,
        temp=temp,
        time=time,
        instructions=instructions, 
        image_url=image_url
    )
    db.session.add(new_recipe)
    db.session.commit()
    return redirect(url_for('index', tab='recipes'))

@app.route('/delete_recipe/<int:id>', methods=['POST'])
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('index', tab='recipes'))

import subprocess
import shutil
import json

# --- Developer Tools (Progress Update) ---
def run_git_command(cmd, cwd):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.returncode == 0

@app.route('/dev')
def dev_panel():
    return render_template('dev.html')

@app.route('/dev/update', methods=['POST'])
def dev_update():
    category = request.form.get('category')
    description_raw = request.form.get('description')
    description = f"{category} {description_raw}"
    details = request.form.get('details') or ""
    
    if not description:
        flash('請輸入修改描述！')
        return redirect(url_for('dev_panel'))
        
    project_root = os.path.dirname(basedir)
    memory_dir = os.path.join(project_root, 'memory')
    checkpoints_dir = os.path.join(memory_dir, 'checkpoints')
    data_js_path = os.path.join(memory_dir, 'data.js')
    log_md_path = os.path.join(memory_dir, 'LOG.md')
    readme_path = os.path.join(project_root, 'README.md')
    
    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    timestamp_file = now.strftime("%Y%m%d_%H%M%S")
    
    try:
        # 1. Create ZIP
        zip_name = f"checkpoint_{timestamp_file}"
        zip_path = os.path.join(checkpoints_dir, zip_name)
        shutil.make_archive(zip_path, 'zip', basedir)
        zip_file = f"{zip_name}.zip"
        
        # 2. Update data.js
        if os.path.exists(data_js_path):
            with open(data_js_path, 'r', encoding='utf-8') as f:
                content = f.read()
                start = content.find('[')
                end = content.rfind(']') + 1
                data = json.loads(content[start:end])
        else:
            data = []
            
        data.append({
            "timestamp": timestamp_str,
            "description": description,
            "details": details,
            "checkpoint_file": zip_file
        })
        
        with open(data_js_path, 'w', encoding='utf-8') as f:
            f.write(f"window.memoryData = {json.dumps(data, ensure_ascii=False, indent=2)};")
            
        # 3. Update LOG.md
        with open(log_md_path, 'a', encoding='utf-8') as f:
            f.write(f"\n## {timestamp_str}\n*   **摘要**: {description}\n*   **詳情**: {details}\n*   **備份**: {zip_file}\n")
            
        # 4. Update README.md
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            new_lines = []
            skip = False
            for line in lines:
                if "## 📌 最後一次動作摘要" in line:
                    new_lines.append(line)
                    new_lines.append(f"> **{timestamp_str}**: {description}\n")
                    skip = True
                elif skip and line.startswith(">"): continue
                else:
                    skip = False
                    new_lines.append(line)
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
                
        # 5. Git Sync
        git_success = False
        if run_git_command("git add .", project_root) and \
           run_git_command(f'git commit -m "Checkpoint: {description}"', project_root) and \
           run_git_command("git push", project_root):
            git_success = True
            
        msg = f'進度更新成功！' + (' (已同步至 GitHub)' if git_success else ' (但 Git 同步失敗)')
        flash(msg)
        return redirect(url_for('dev_panel'))
        
    except Exception as e:
        flash(f'更新出錯：{str(e)}')
        return redirect(url_for('dev_panel'))

if __name__ == '__main__':
    app.run(debug=True)

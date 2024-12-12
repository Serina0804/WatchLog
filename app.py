from flask import Flask, render_template, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

print(f"Current working directory: {os.getcwd()}")

# データベースの代わりにリストを使用（簡易版）
# records = []

# データベースの設定
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///watchlog.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/ailab/WatchLog/watchlog.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# 基本的なデータベース設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/watchlog.db'
# 複数のデータベースを使用する場合の設定
app.config['SQLALCHEMY_BINDS'] = {
    'users': 'sqlite:////tmp/users.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    tag = db.Column(db.String(200), nullable=False)
    # user_id = db.Column(db.String(100), primary_key=True)
    # user_passward = db.Column(db.String(100), nullable=False)

class UserRecord(db.Model):
    __bind_key__ = 'users'
    user_id = db.Column(db.String(100), primary_key=True)
    user_password = db.Column(db.String(100), nullable=False)

# データベースの作成
if not os.path.exists('watchlog.db'):
    with app.app_context():
        db.drop_all()  # 既存のテーブルを削除
        db.create_all()  # 新しいテーブルを作成
        print("Database and tables recreated.")
else :
    print("db exit!")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # POSTリクエストの場合、ログイン処理を行う
        user_name = request.form['user_name']
        password = request.form['password']
        print(f"Logging in user: {user_name} with password: {password}")
        user = UserRecord.query.filter_by(user_id=user_name).first()
        if user and user.user_password == password:
            print("Login successful")
            return redirect(url_for('view_records'))
        else:
            print("Login failed")
            error_message = "ユーザー名またはパスワードが間違っています"
            return render_template('login.html', error=error_message)
    
    # GETリクエストの場合、ログイン画面を表示
    print(f"Database path: {os.path.abspath('watchlog.db')}")
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        print(f"Using database URI: {app.config['SQLALCHEMY_BINDS']}")
        user_name = request.form['user_name']
        password = request.form['password']
        print(user_name , password)
        # データベースからユーザーを検索
        user = UserRecord.query.filter_by(user_id=user_name).first()
        if user and user.user_password == password:  # ユーザーが存在しパスワードが一致する場合
            # ログイン成功
            print("login OK")
            return redirect(url_for('view_records'))
        else:
            # ログイン失敗
            error_message = "ユーザー名またはパスワードが間違っています"
            print("login error")
            return render_template('login.html', error=error_message)
        
    print(f"Using database URI: {app.config['SQLALCHEMY_BINDS']}")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        print(f"Using database URI: {app.config['SQLALCHEMY_BINDS']}")
        user_name = request.form['user_name']
        password = request.form['password']
        
        # ユーザーが既に存在するか確認
        existing_user = UserRecord.query.filter_by(user_id=user_name).first()
        if existing_user:
            return render_template('new_user.html', error="このユーザー名は既に使用されています")
        new_user = UserRecord(user_id=user_name, user_password=password)
        db.session.add(new_user)
        db.session.commit()
        print(f"Using database URI: {app.config['SQLALCHEMY_BINDS']}")
        print(f"Record added: {new_user.user_id}, {new_user.user_password}")
        return redirect(url_for('login_user'))
    return render_template('new_user.html')  # GETリクエストの場合

@app.route('/reset', methods=['POST'])
def reset_records():
    global records
    records = []  # リストを空にする
    return redirect(url_for('view_records'))


@app.route('/add', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        print(f"Using database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        title = request.form['title']
        rating = int(request.form['rating'])
        image = request.files['image']
        tag_number = int(request.form['tag'])
        if tag_number == 1 :
            tag = "漫画"
        elif tag_number == 2 :
            tag = "アニメ"
        elif tag_number == 3 :
            tag = "映画"
        elif tag_number == 4 :
            tag = "ドラマ"
        else :
            tag = "バラエティ"

        # 画像の保存
        upload_folder = 'static/uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        image_path = os.path.join(upload_folder, image.filename)
        image.save(image_path)

        # データベースに保存
        new_record = Record(title=title, rating=rating, image_path=image_path, tag = tag)
        db.session.add(new_record)
        db.session.commit()
        print(f"Using database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"Record added: {new_record.title}, {new_record.rating}, {new_record.image_path}, {new_record.tag}")

        return redirect(url_for('view_records'))
    print(f"Using database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    return render_template('add_record.html')


@app.route('/view')
def view_records():
    records = Record.query.all()  # データベースから全てのレコードを取得
    print(records)
    return render_template('view_records.html', records=records)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_record(id):
    record = Record.query.get(id)
    if record:
        # 画像ファイルの削除
        if os.path.exists(record.image_path):
            os.remove(record.image_path)

        db.session.delete(record)
        db.session.commit()
    return redirect(url_for('view_records'))


if __name__ == '__main__':
    
    print("Checking database creation...")
    if not os.path.exists('watchlog.db'):
        print("Database not found. Creating...")
        with app.app_context():
            db.create_all()
            print("Database created.")
    else:
        print("Database already exists.")
    if not os.path.exists('user.db'):
        print("Database not found. Creating...")
        with app.app_context():
            db.create_all()
            print("UserDatabase created.")
    else:
        print("Database already exists.")
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Expected database location: {os.path.abspath('watchlog.db')}")

    # Renderの環境変数PORTを取得し、デフォルト値は5000
    port = int(os.environ.get("PORT", 4000))
    # ホストを0.0.0.0に設定して、すべてのネットワークインターフェースからのリクエストを受け入れる
    app.run(host="0.0.0.0", port=port)
    # app.run(debug=True)

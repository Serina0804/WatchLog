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
db_path = '/tmp/watchlog.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# インスタンスフォルダを作成（デプロイ時に必要）
os.makedirs(app.instance_path, exist_ok=True)
db = SQLAlchemy(app)

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    tag = db.Column(db.String(200), nullable=False)
    
    
# データベースの作成
if not os.path.exists('watchlog.db'):
    with app.app_context():
        db.drop_all()  # 既存のテーブルを削除
        db.create_all()  # 新しいテーブルを作成
        print("Database and tables recreated.")

else :
    print("db exit!")

@app.route('/')
def home():
    print(f"Database path: {os.path.abspath('watchlog.db')}")
    return render_template('index.html')

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
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Expected database location: {os.path.abspath('watchlog.db')}")

    # Renderの環境変数PORTを取得し、デフォルト値は5000
    port = int(os.environ.get("PORT", 4000))
    # ホストを0.0.0.0に設定して、すべてのネットワークインターフェースからのリクエストを受け入れる
    app.run(host="0.0.0.0", port=port)
    # app.run(debug=True)

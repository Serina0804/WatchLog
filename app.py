from flask import Flask, render_template, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# データベースの代わりにリストを使用（簡易版）
# records = []

# データベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///watchlog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(200), nullable=False)

# データベースの作成
if not os.path.exists('watchlog.db'):
    with app.app_context():
        db.create_all()

@app.route('/')

def home():
    return render_template('index.html')

@app.route('/reset', methods=['POST'])
def reset_records():
    global records
    records = []  # リストを空にする
    return redirect(url_for('view_records'))


# @app.route('/add', methods=['GET', 'POST'])
# def add_record():
#     if request.method == 'POST':
#         title = request.form['title']
#         rating = request.form['rating']
#         image = request.files['image']
#         image_path = f'static/uploads/{image.filename}'
#         image.save(image_path)
#         records.append({'title': title, 'rating': rating, 'image': image_path})
#         print(records)
#         return redirect(url_for('view_records'))
#     return render_template('add_record.html')

@app.route('/add', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        title = request.form['title']
        rating = int(request.form['rating'])
        image = request.files['image']

        # 画像の保存
        upload_folder = 'static/uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        image_path = os.path.join(upload_folder, image.filename)
        image.save(image_path)

        # データベースに保存
        new_record = Record(title=title, rating=rating, image_path=image_path)
        db.session.add(new_record)
        db.session.commit()

        return redirect(url_for('view_records'))
    return render_template('add_record.html')


@app.route('/view')
def view_records():
    records = Record.query.all()  # データベースから全てのレコードを取得
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
    app.run(debug=True)

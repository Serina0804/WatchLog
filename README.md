# WatchLog
## 目次

1. [プロジェクトについて](#プロジェクトについて)
2. [環境](#環境)
3. [ディレクトリ構成](#ディレクトリ構成)
4. [開発環境構築](#開発環境構築)
5. [トラブルシューティング](#トラブルシューティング)


## プロジェクト名

WatchLog：映画、漫画、アニメ、ドラマ、バラエティなど見たものを管理するアプリ

<!-- プロジェクトについて -->

## プロジェクトについて

- 見た作品、読んだ作品の題名、写真をアップ。作品の種類とその評価を選んで登録すると一覧から見れます！

<p align="right">(<a href="#top">トップへ</a>)</p>

## 技術スタック

<!-- 言語、フレームワーク、ミドルウェア、インフラの一覧とバージョンを記載 -->

|   | 技術 |
| --------------------- | ---------- |
| フロントエンド                |  HTML, CSS     |
| バックエンド                |   Flask (Python), Gunicorn (デプロイ用)   |
| データベース |  SQLite  |
| 認証/セッション管理                 | Flask-Session, bcrypt (パスワードのハッシュ化)        |
| デプロイ/ホスティング               | Render    |
| パッケージ管理/依存管理                 | pip (requirements.txt)  |
<!-- | Next.js               | 13.4.6     |
| Terraform             | 1.3.6      | -->


<p align="right">(<a href="#top">トップへ</a>)</p>

## ディレクトリ構成

<!-- Treeコマンドを使ってディレクトリ構成を記載 -->

<!-- ❯ tree -a -I "node_modules|.next|.git|.pytest_cache|static" -L 2 -->
```
.
├── README.md                # プロジェクトの概要、技術スタック、セットアップ手順など
├── requirements.txt         # Pythonの依存関係
├── app.py                   # Flaskアプリケーションのエントリーポイント
├── watchlog.db              # SQLiteデータベースファイル
├── alembic.ini              # データベースマイグレーション用の設定ファイル
├── static/                  # 静的ファイル
│   ├── css/
│   │   └── styles.css       # スタイルシート
│   ├── js/                  # JavaScriptファイル用ディレクトリ（現在は空）
│   │   └── app.js
│   └── uploads/             # ユーザーがアップロードした画像を保存するディレクトリ
├── templates/               # HTMLテンプレートファイル
│   ├── add_record.html
│   ├── index.html
│   ├── login.html
│   ├── new_user.html
│   └── view_records.html
├── migrations/              # Alembicのマイグレーションファイル用ディレクトリ
├── tmp/                     # 一時ファイル用ディレクトリ
└── instance/                # Flaskアプリケーションのインスタンスフォルダ（設定や追加ファイルの保存用）
```


<p align="right">(<a href="#top">トップへ</a>)</p>

## 開発環境構築

<!-- コンテナの作成方法、パッケージのインストール方法など、開発環境構築に必要な情報を記載 -->


### 動作確認

- ローカル環境
    - http://127.0.0.1:4000 にアクセスできるか確認
    - アクセスできたら成功
- 一般環境
    - https://watchlog.onrender.com

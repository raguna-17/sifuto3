# 求人アプリ

FastAPI + SQLAlchemy + JWT認証を用いた、求人応募システムのバックエンドAPIです。  
ユーザーは企業情報と応募履歴を管理できます。

---

## 🚀 技術スタック

- Python 3.12
- FastAPI
- SQLAlchemy（Async ORM）
- PostgreSQL（想定）
- Alembic（マイグレーション）
- JWT認証（python-jose）
- パスワードハッシュ：argon2（passlib）
- Docker

---

## 🧱 アーキテクチャ

ドメイン単位で構成されたレイヤード構造

各ドメインは以下構成：

- router（APIエンドポイント）
- service（ビジネスロジック）
- model（DBモデル）
- schema（Pydantic）

---

## 🔐 認証

JWTトークン認証を採用

- ログイン時にアクセストークン発行
- `/users/me` で認証ユーザー取得
- パスワードはargon2でハッシュ化

### エンドポイント

| Method | Path | Description |
|------|------|-------------|
| POST | /users/register | ユーザー登録 |
| POST | /users/login | ログイン |
| GET | /users/me | 自分の情報取得 |

---

## 👤 ユーザー機能

- ユーザー登録 / ログイン
- 自分の情報取得

---

## 🏢 企業（Organizations）

ユーザーごとに企業情報を管理

### エンドポイント

| Method | Path | Description |
|------|------|-------------|
| POST | /organizations | 企業作成 |
| GET | /organizations | 一覧取得 |
| GET | /organizations/{id} | 詳細取得 |
| DELETE | /organizations/{id} | 削除 |

---

## 💼 応募（Job Applications）

企業への応募履歴を管理

### エンドポイント

| Method | Path | Description |
|------|------|-------------|
| POST | /job-applications | 応募作成 |
| GET | /job-applications | 自分の応募一覧 |
| GET | /job-applications/{id} | 応募詳細 |
| DELETE | /job-applications/{id} | 削除 |

---

## 🗄 データモデル

### User

- email
- hashed_password
- is_active
- created_at

リレーション：
- job_applications
- organizations

---

### Organization

- name
- industry
- user_id

リレーション：
- job_applications

---

### JobApplication

- user_id
- organization_id
- organization_name
- job_title
- created_at

---


---

## 📌 特徴

- ドメイン分離アーキテクチャ
- JWT認証
- 非同期SQLAlchemy構成
- ユーザー単位のデータ分離
- REST API設計
- テスト構成あり（pytest）

---

## 📂 フロントエンド連携

React（Vite）で構築

- auth / organizations / job_applications に分割
- 各featureごとにAPI層を分離

---

## 📈 今後の拡張案

- ページネーション
- 検索機能
- ロール管理（admin/user）
- Redisキャッシュ
- CI/CD導入

---

## 🧑‍💻 Author

Portfolio project

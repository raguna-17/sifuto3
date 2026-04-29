# 求人管理アプリ（Recruiting System）

## 概要

企業・求人・応募の採用プロセスを一元管理するWebアプリケーションです。
実務の採用管理フローを意識し、単なるCRUDではなく**業務ロジックの実装と設計**に重点を置いて開発しました。

---

## 実装した業務フロー

* 企業の作成・管理
* 求人の作成・管理
* 求人への応募
* 応募情報の管理（企業側・応募者側）

---

## 業務ロジックの実装（重要ポイント）

### 応募機能（job_applications）

実務を意識し、以下の制御を実装しています：

* 同一ユーザーによる重複応募を禁止
* 応募ステータスの管理
* ステータス遷移制御
* データ整合性をアプリケーションレベルで担保

#### ステータス遷移

* applied → interview / rejected
* interview → offer / rejected
* offer / rejected → 変更不可

不正な遷移はAPIレベルで制御しています。

---

### 認可制御

* 自分の応募のみ取得可能（応募者）
* 自社求人の応募のみ取得可能（企業側）

---

## アーキテクチャ設計

ドメイン単位で分割したレイヤードアーキテクチャを採用しています。

### ドメイン構成

* users
* organizations
* job_postings
* job_applications

### レイヤー構造

* Router：HTTPリクエスト処理
* Service：ビジネスロジック
* Repository：DBアクセス

---

## 設計上のポイント

* Service層に業務ロジックを集約し、API層から分離
* Repository層でDBアクセスを抽象化し、変更容易性を確保
* FastAPIのDependsによる依存性注入を活用
* ステータス遷移による業務フロー制御を実装

---

## API設計

RESTfulな設計を意識しています。

* `POST /job_applications/`
  → 応募作成

* `GET /job_applications/me`
  → 自分の応募一覧

* `GET /job_applications/job/{id}`
  → 求人ごとの応募一覧（企業側）

* `PUT /job_applications/{id}`
  → ステータス更新

---

## 技術スタック

### Backend

* FastAPI
* SQLAlchemy（Async）
* PostgreSQL
* Alembic
* Pydantic
* JWT認証（python-jose）
* Docker / Docker Compose

### Frontend

* React（Vite）
* JavaScript
* Axios

---

## コードの見どころ

### バックエンド（業務ロジック）

* `app/recruiting/job_applications/service.py`
* `app/recruiting/job_applications/repository.py`

応募処理・ステータス管理・認可制御など、業務ロジックを実装しています。

---

### フロントエンド（API連携）

* `frontend/src/features/job_postings/JobPostingPage.jsx`

求人一覧取得・作成・API連携の実装を確認できます。

---

## インフラ構成

* Dockerによる開発環境の統一
* 環境変数による設定管理（DB接続・CORS）
* PostgreSQLコンテナ
* FastAPIコンテナ
* Alembicによるマイグレーション管理


---
## 🧪 テスト

Pytestを用いてAPIテストを実装しています。

ユーザー登録
ログイン
認証フロー

正常系・異常系の両方をカバーし、リファクタリングや機能追加に耐えられる構成としています。
---

## 起動方法

```bash
docker compose up --build
```

---

## 今後の改善予定

* 応募検索・フィルタ機能
* UI/UX改善
* テストコードの拡充
* 権限管理の強化（ロール設計）

---

## 開発背景

求人サービスを利用する中で、
「企業・求人・応募の流れを自分で設計・実装したい」と考えたことがきっかけです。

業務フローを意識し、実務に近い形で設計しました。

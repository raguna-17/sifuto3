# EC App

FastAPI + React + PostgreSQL を用いて開発した EC サービスです。

JWT 認証、権限制御、注文トランザクション、状態遷移制御などを実装し、
単なる CRUD ではなく、業務システムを意識したバックエンド設計を行いました。

Docker による開発環境統一、Alembic によるマイグレーション管理にも対応しています。

---

# Demo

## Demo Video

動画を見る

---

# Features

## Authentication

- JWT Authentication
- Access Token / Refresh Token 分離
- Token Type Validation
- Password Hashing（Argon2）
- 権限制御（Admin / User）

## Product

- 商品一覧取得
- 商品詳細取得
- 商品作成（Admin）
- 在庫管理
- 論理削除

## Cart

- カート追加
- カート一覧取得
- カート削除

## Order

- 注文作成
- 注文履歴取得
- 注文詳細取得
- 注文ステータス更新
- 状態遷移制御
- 管理者削除

---

# Business Logic

実務を意識し、以下の業務ロジックを実装しています。

- 在庫チェック
- 注文トランザクション管理
- 不正ステータス遷移防止
- Token Type Validation
- 管理者権限制御

## Transaction Management

注文作成では、
在庫確認と注文生成を単一トランザクションとして扱っています。

```python id="u21mfa"
try:
    ...
    await db.commit()

except Exception:
    await db.rollback()

事前検証を行い、
データ整合性を維持しています。

if product.stock < item["quantity"]:
    raise ValueError("insufficient stock")
Order Status Transition

注文ステータスは不正遷移を防ぐため、
遷移可能状態を制御しています。

allowed_transitions = {
    OrderStatus.PENDING: [
        OrderStatus.PAID,
        OrderStatus.CANCELLED,
    ],
    OrderStatus.PAID: [
        OrderStatus.SHIPPED
    ],
}
Architecture

ドメイン単位で分割したレイヤードアーキテクチャを採用しています。

Domain Structure
product
cart
order
Layer Structure
router      # API endpoint
service     # business logic
repository  # DB access
model       # ORM model
schema      # Pydantic schema
Design Principles
Service 層へ業務ロジックを集約
Repository 層で DB アクセスを抽象化
Transaction 境界を Service 層で管理
状態遷移ルールを集約し、不正更新を防止

FastAPI の Depends を利用し、
認証・認可制御を実装しています。

API Design

RESTful API を意識して設計しています。

POST /auth/login
POST /orders/
GET /orders/me
PUT /orders/{id}/status
POST /cart/
Tech Stack
Backend
FastAPI
SQLAlchemy（Async）
PostgreSQL
Alembic
JWT（python-jose）
Passlib / Argon2
Pytest
Docker
Frontend
React（Vite）
React Router
Axios
Testing

pytest + httpx による API テストを実装しています。

Test Examples
ログイン認証
注文作成
在庫不足
注文詳細取得
ステータス更新
不正状態遷移
管理者削除
Coverage
TOTAL 69.2%
13 passed

主要ユースケースを中心に、
正常系・異常系の両方をテストしています。

Infrastructure
Docker による開発環境統一
PostgreSQL コンテナ
FastAPI コンテナ
Alembic によるマイグレーション管理
環境変数による設定管理
Development
Start
docker compose up --build
Migration
alembic upgrade head
Test
pytest --cov
Future Improvements
Refresh Token Rotation
Redis Cache
CI/CD
Stripe 決済対応
RBAC 拡張
AWS Deploy
Motivation

単なる CRUD 実装ではなく、

認証
権限制御
トランザクション
状態遷移
保守性

を意識し、
業務システムを想定した設計・実装を行いました。
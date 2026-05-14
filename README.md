# EC Backend + Frontend Project

FastAPI + React を使用したシンプルなECサイトサンプルです。  
ユーザー認証、商品管理、カート機能、注文機能を備えています。

---

## 技術スタック

### Backend
- FastAPI
- SQLAlchemy (Async)
- PostgreSQL / SQLite
- JWT認証 (python-jose)
- Passlib (argon2)

### Frontend
- React (Vite)
- Axios
- React Router

---

## 機能一覧

### 認証
- ユーザー登録
- ログイン
- JWT認証

### 商品
- 商品一覧取得
- 商品詳細取得
- 商品作成（管理用想定）

### カート
- カート追加
- 数量変更
- 削除
- カート全削除
- カート取得

### 注文
- カート内容から注文作成
- 注文履歴取得
- 注文詳細取得
- 注文キャンセル（pendingのみ）

---

## システム構成

### カート → 注文フロー

カートに入っている商品をもとに注文を作成します。

フロントエンドから以下の流れで処理されます：

1. カート取得 (`GET /cart/`)
2. 注文作成 (`POST /orders/`)
3. カート削除 (`DELETE /cart/`)
4. 注文一覧へ遷移 (`GET /orders/`)

---

## API仕様

### 認証
- `POST /users/register`
- `POST /users/login`

---

### カート
- `GET /cart/`
- `POST /cart/`
- `PATCH /cart/{product_id}`
- `DELETE /cart/{product_id}`
- `DELETE /cart/`

---

### 注文
- `POST /orders/`
- `GET /orders/`
- `GET /orders/{order_id}`
- `DELETE /orders/{order_id}`

#### 管理用
- `GET /orders/admin/all`
- `PATCH /orders/admin/{order_id}/status`
- `DELETE /orders/admin/{order_id}`

---

## 注文作成仕様

注文作成時はサーバー側で以下を計算します：

- 商品価格取得
- quantity × price による total_price計算
- user_idをJWTから取得
- statusは `pending`

フロント側は `product_id` と `quantity` のみ送信します。

---

## 認証仕様

JWTトークンを使用しています。

- アクセストークン: localStorage に保存
- Authorizationヘッダーに付与

---

## データ設計概要

### Order
- id
- user_id
- product_id
- quantity
- total_price
- status
- created_at

---

## 注意事項

- カートはユーザーごとに管理されます
- 注文作成後もカートは自動削除されません（フロント側で削除）
- MVP構成のため在庫管理・決済機能は未実装です

---

## 今後の改善ポイント

- カート→注文のバルクAPI化
- 在庫管理
- 支払いフロー追加
- トランザクション管理強化
- OrderItemテーブル分離（正規化）

---

## 起動方法

### Backend
```bash
uvicorn app.main:app --reload
# 面接管理アプリ（Interview Management App）

## 概要

就職活動における企業への応募状況や面接スケジュールを一元管理できるWebアプリです。
従来のスプレッドシートやメモでは、複数企業への応募進捗が把握しづらく、面接日程の管理も煩雑になりがちでした。本アプリを使うことで、進捗の可視化やスケジュール管理を効率化し、応募や面接準備に集中できる環境を提供します。

---


## デモ
フロントエンド：
https://kyusyoku-furonto.onrender.com


動作イメージ動画：
https://www.youtube.com/shorts/ugAJGbqNh-8


## 技術スタック

### Backend

* FastAPI
* SQLAlchemy（Async対応）
* PostgreSQL
* Alembic（マイグレーション）
* JWT認証（python-jose）
* Argon2（パスワードハッシュ）

### Frontend
* React
* Vite（高速ビルドツール）
* javaScript
* Axios（API通信）
* React Router（画面遷移管理）

### その他

* Docker / Docker Compose
* Pytest（テスト）

---

## 主な機能

### ユーザー機能

* ユーザー登録
* ログイン（JWT認証）
* 認証ユーザー取得（/me）

### 企業管理

* 企業の登録・一覧取得

### 応募管理

* 応募情報の登録
* ステータス管理（応募中・面接中など）
* 面接日程の管理

---

## 認証・セキュリティ

* JWTベースの認証を採用
* パスワードはArgon2でハッシュ化
* トークンからユーザーIDを取得しDBで検証

---

## データベース設計

### エンティティ

* User
* Company
* Application

### リレーション

* User : Application = 1 : N
* Company : Application = 1 : N

### 制約

* (user_id, company_id, position) のユニーク制約
  → 同一ユーザーが同一企業・同一職種へ重複応募することを防止

---

## API設計

* Pydanticスキーマで入力・出力を分離
* ORMモデルとAPIレスポンスを分離
* ネスト構造で関連データを返却（Application → Company）

## エラーハンドリング
* HTTPステータスコードを適切に返却
* バリデーションエラーは詳細メッセージを返却
* 認証エラーは401で統一

---

## アーキテクチャ

```
Router → Service → DB
```

* Router：リクエスト/レスポンスの処理
* Service：ビジネスロジック
* Model：データ構造

責務を分離することで可読性・保守性・再利用性を向上


## フロントエンドとの連携
* REST APIとしてバックエンドを提供
* フロントエンドとは完全に分離した構成
* CORS設定により安全に通信

---

## テスト

Pytestを用いてAPIのテストを実施しており、特にユーザー登録・ログイン・認証フローを重点的に検証しています。正常系だけでなく異常系も網羅することで、リファクタリングや機能追加にも耐えられる安定した品質を確保しています。

---

## セットアップ

```bash
# 起動
docker-compose up --build

# マイグレーション
alembic upgrade head
```

---

## 工夫した点

* JWT認証を自前実装し、認証フローを明確化
* Service層を導入しビジネスロジックを分離
* ユニーク制約によりデータ整合性を担保
* 非同期処理（AsyncSession）によるパフォーマンス向上
* テストコードを整備し品質を担保
* フロントエンドと責務を明確に分離
* Dockerで環境差異を排除、Renderへデプロイ
---

## 今後の改善点

* テストカバレッジの向上（特に企業・応募機能）
* エラーハンドリングの詳細化
* UI/UXの改善
* 権限管理の追加

📄 Job Application Management API

企業への応募状況を一元管理できるWebアプリケーションです。
実際の転職・就職活動における情報管理を想定し、応募・企業・ユーザー情報を統合的に扱える設計としています。

バックエンドとフロントエンドを分離した構成により、拡張性と保守性を重視したプロダクト設計を行っています。

🎯 プロジェクト概要

本アプリケーションは、以下の課題解決を目的としています：

応募状況が複数サービスに分散し管理が煩雑になる問題
進捗状況（応募・面接・内定など）の可視化不足
就職・転職活動の情報整理コストの増大

これらを解決するため、応募情報を中心に一元管理できるシステムを構築しました。

🚀 技術スタック
バックエンド
Python 3.12
FastAPI
SQLAlchemy（Async ORM）
PostgreSQL（想定）
Alembic（マイグレーション管理）
JWT認証（python-jose）
Argon2（パスワードハッシュ）
Docker / Docker Compose
フロントエンド
React（Vite）
Axios
React Router
🧱 アーキテクチャ設計

ドメイン駆動を意識したレイヤード構成を採用しています。

レイヤー構成
router：APIエンドポイント定義
service：ビジネスロジック
model：DBモデル定義
schema：入出力スキーマ
ドメイン構造
app/
├── users
├── organizations
├── job_applications
├── core
└── db / dependencies

各ドメインごとに責務を分離し、保守性・拡張性を高めています。

🔐 認証設計

JWTベースのステートレス認証を採用しています。

認証フロー
ログイン時にJWTトークンを発行
トークンからユーザーIDを取得
DBと照合し認証を検証
セキュリティ設計
パスワードはArgon2でハッシュ化
トークンベース認証によるスケーラビリティ確保
👤 ユーザー機能
Method	Path	Description
POST	/users/register	ユーザー登録
POST	/users/login	ログイン
GET	/users/me	認証ユーザー取得
🏢 企業管理（Organizations）
Method	Path	Description
POST	/organizations	企業作成
GET	/organizations	一覧取得
GET	/organizations/{id}	詳細取得
DELETE	/organizations/{id}	削除
💼 応募管理（Job Applications）
Method	Path	Description
POST	/job-applications	応募作成
GET	/job-applications	応募一覧取得
GET	/job-applications/{id}	応募詳細取得
DELETE	/job-applications/{id}	削除
🗄 データモデル設計
User
email
hashed_password
is_active
created_at
Organization
name
industry
user_id
JobApplication
user_id
organization_id
organization_name
job_title
created_at
📌 設計上の特徴
ドメイン単位での責務分離（レイヤードアーキテクチャ）
非同期処理（AsyncSession）によるパフォーマンス最適化
JWTによるステートレス認証
ユーザー単位でのデータ分離
REST API設計の採用
Service層によるビジネスロジック分離
ユニーク制約によるデータ整合性担保
📂 フロントエンド構成

React（Vite）によるSPA構成です。

features（機能単位設計）
auth：ログイン・ユーザー登録・認証管理
organizations：企業情報管理
job_applications：応募情報管理

各ドメインごとに api.js と画面コンポーネントを分離し、バックエンドAPIと疎結合な設計としています。

その他構成
components：再利用UI（Button / Input / Modal など）
layouts：Header / Sidebar / Layout構成
pages：ルーティング単位のページ
🧭 ユーザー体験（UX設計）

本アプリは「就職・転職活動の進捗管理の効率化」を目的としています。

ユーザーフロー
ユーザー登録・ログイン
企業情報の登録
応募情報の作成
ステータス管理（応募中・面接中・内定など）
応募状況の一覧確認
UX設計の特徴
応募状況を一覧で可視化
企業と応募情報の紐付けによる情報整理
最小ステップで操作可能なUI設計
SPA構成による高速な画面遷移
想定ユースケース
複数企業への応募管理
面接・選考状況の整理
就職・転職活動の進捗トラッキング
🧪 テスト

pytestを用いてAPIテストを実装しています。

ユーザー登録
ログイン
認証フロー

正常系・異常系の両方をカバーし、リファクタリングや機能追加に耐えられる構成としています。

📈 今後の改善・拡張
ページネーションの導入
検索機能の追加
ロール管理（admin / user）
Redisキャッシュ導入
CI/CD構築
エラーハンドリングの標準化
UI/UX改善

EC API（FastAPI + 業務整合性設計）
概要

本プロジェクトはEC業務フロー（商品管理・注文・在庫制御）を再現したバックエンドシステムです。
単なるCRUDではなく、「在庫整合性・状態遷移・並行性」を含む業務ロジック設計に重点を置いています。

業務フロー設計
基本フロー

Product → Order → OrderItem

商品選択
注文作成
注文明細生成
在庫減算
コア設計
① 在庫制御（整合性設計）

注文作成時に以下を保証：

在庫チェック
在庫不足時は注文拒否
注文確定時に在庫減算

👉 すべてService層で制御し、ビジネスロジックを集約

② 注文ステータス管理
PENDING → PAID → SHIPPED
        → CANCELLED
状態遷移はService層で制御
不正遷移は拒否
allowed_transitions による明示的制御

👉 if文ベースの自由更新を禁止し、業務ルールを強制

③ カート非依存設計（シンプルECモデル）

本システムではカートを持たず、注文時に直接明細を生成する設計を採用。

👉 「注文＝業務の確定状態」として扱うことで整合性を簡略化

④ データ整合性設計
Order / OrderItem をトランザクション単位で生成
在庫更新と注文作成を同一フローで処理
SQLAlchemy AsyncSession による非同期トランザクション管理
アーキテクチャ
レイヤー構造
router（API層）
service（業務ロジック）
repository（DBアクセス）

👉 ビジネスロジックは service に完全集約


API設計
注文系
POST /orders/（注文作成）
GET /orders/（自分の注文一覧）
GET /orders/{id}（注文詳細）
管理系
PATCH /orders/admin/{id}/status
DELETE /orders/admin/{id}
認証・認可
JWT認証（access token）
USER / ADMIN ロール制御
管理APIはADMINのみアクセス可能
テスト設計

pytest による統合テストを実装

テスト対象
注文作成ロジック
在庫不足エラー
ステータス遷移制御
認可制御（USER / ADMIN）
注文削除フロー
特徴
APIレベルのE2Eテスト構成
業務ルール（状態遷移・在庫制御）を重点検証
正常系・異常系の両方をカバー
技術スタック
FastAPI（async）
SQLAlchemy（AsyncSession）
PostgreSQL
Alembic
JWT（python-jose）
Docker / docker-compose
pytest
設計上のポイント（重要）
① 業務ロジックのService集約
routerは薄く維持
serviceにドメインロジック集中
② 状態遷移の明示的制御
allowed_transitions による制御
不正遷移をAPIレベルで拒否
③ トランザクション設計
注文作成と在庫更新を同一処理内で実行
整合性を保証
今後の改善
在庫ロック（SELECT FOR UPDATE）による競合対策強化
リアルタイム在庫反映
非同期メッセージキュー導入（注文処理分離）
管理ダッシュボード追加
負荷試験・同時注文テスト強化
開発意図

ECの本質である「在庫と注文の整合性問題」をテーマに設計。
CRUDではなく、業務システムとしての状態管理・制約設計を重視している。




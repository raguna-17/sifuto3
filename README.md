# シフト管理・自動割り当てシステム API

シフト希望・制約条件・人員要件をもとに、ユーザーを自動で割り当てるバックエンドシステム。

手動調整と自動生成の両方に対応し、管理者は生成結果を確認したうえで確定できる構成になっている。

## 概要

本システムは以下の課題を解決するために設計されている：

* シフト調整の属人化
* 人手による割り当てミス
* 希望と実際の乖離
* 人員不足・過剰配置の発生

これをスコアベースの割り当てアルゴリズムで自動化する。

## 📺 Demo Video

このプロジェクトの動作デモです。

## 👉 :https://www.youtube.com/watch?v=chMBNJy8fHg


## システム構成(バックエンド:FastAPI)


## レイヤー構成：

* API Layer（Router）
* Service Layer（ビジネスロジック）
* Domain Model（SQLAlchemy）
* Scheduler Engine（割り当てアルゴリズム）

## 特徴：

* すべての業務ロジックはService層に集約
* Routerは薄いAPI定義のみ
* ドメインごとに責務分離
* フロントエンド（React）

※バックエンド利用のための管理UIとして実装

## 主な機能：

* シフト生成（管理者）
* 生成結果の編集
* 確定保存
* ユーザー一覧取得
* ドメイン設計
* ShiftSlot（シフト枠）

勤務枠を表すエンティティ。

制約：

* 開始時刻 < 終了時刻
* 過去日時は禁止
* 最大期間制限あり
* required_staff_count による定員管理
* 重複作成防止
* ShiftPreference（希望）

ユーザーのシフト希望を表現する。

優先度：

* REQUIRED（必須）
* PREFERRED（希望）
* NEUTRAL（通常）
* AVOID（避けたい）
* UNAVAILABLE（不可）

制約：

* ユーザー × シフト枠で1件のみ
* 更新時も重複チェックを維持
* ShiftAssignment（割り当て結果）

実際に確定したシフト割り当て。

制約：

* 同一ユーザーの重複割り当て禁止
* シフト枠の定員制限あり
* 手動・自動割り当て両対応
* スケジューリングアルゴリズム


## 📌 概要

ユーザーの希望と制約をスコアリングし、各シフト枠に対して最適な人員を割り当てるシステム。

---

## 🧮 スコア定義


* REQUIRED : +100
* PREFERRED : +10
* NEUTRAL : +1
* AVOID : -20
* UNAVAILABLE : -999


---

## 🔁 処理フロー

- 全ユーザー・全シフト枠を取得
- 各ユーザーに対してスコア計算
- スコア順にソート
- `required_staff_count` まで割り当て
- 重複割り当てを防止

---

## ⚙️ モード

### ▶ generate（ドライラン）
- 仮のシフト生成
- 確認用（DB保存なし）

### ▶ confirm（確定）
- 生成結果をDBへ保存
- 実データとして反映

---

## 🌐 API一覧

### 🔐 認証

* POST /login
* POST /register


### 📅 シフト枠

* GET /shift-slots
* POST /shift-slots
* GET /shift-slots/{id}


### 🙋 希望登録

* POST /shift-preferences
* GET /shift-preferences


### 👤 割り当て

* GET /shift-assignments
* POST /shift-assignments/bulk/{user_id}
* GET /shift-assignments/me


### 🧠 スケジューラ

* POST /scheduler/generate
* POST /scheduler/confirm


---

## 🔄 シフト生成フロー

- 管理者がシフト生成を実行
- スコアベースで仮割り当て生成
- フロントで編集可能な形式で表示
- 管理者が修正
- 確定保存でDBへ反映

---

## 🧰 技術スタック


- FastAPI
- SQLAlchemy (Async)
- PostgreSQL
- Alembic
- Docker / Docker Compose
- React（管理UI）
- Axios


---

## 🧱 設計上の特徴

- ドメインごとのService分離
- スコアベースの割り当てアルゴリズム
- 明示的な例外設計（業務エラーの表現）
- generate / confirm の二段階設計
- トランザクション安全性を考慮したDB操作
- UTC統一による日時バグ対策

---

## 🧩 このシステムが解決する問題

従来の手動シフト管理では：

* 調整コストが高い
* 属人性が高い
* 希望反映が困難
* 人的ミスが発生

本システムはこれを：

「ルールベース + スコアリング」による再現可能な自動割り当てで解決する。

## まとめ

このプロジェクトは単なるCRUD APIではなく、

「制約条件付きリソース割り当て問題を解くドメインシステム」

として設計されている。
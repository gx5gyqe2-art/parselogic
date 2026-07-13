# readeffect — OPCG カードデータ取り込み

ワンピースカードゲーム公式サイトのカード一覧HTMLを解析して、カードデータJSONと
画像を生成・取得するツール群。

## ファイル

| ファイル | 役割 |
| --- | --- |
| `readdata.py` | HTML解析の本体。フルビルド（全HTMLから作り直し）と、再利用可能なパース関数を提供 |
| `update_cards.py` | **差分取り込み**。新カードのHTMLを渡して既存マスターへマージ |
| `storeimage.py` | 画像ダウンローダ（700件ごとにサブフォルダ分割） |
| `opcg_cards.json` | **マスター**: 全カードデータ（唯一の正）|
| `opcg_images.json` | **マスター**: 全カードの画像URL（`opcg_cards.json` と番号が一致）|
| `opcg_images_new.json` | 差分取り込みが出力する「今回取得すべき画像だけ」のリスト（gitignore）|
| `old/` | 過去の生HTMLダンプ・旧出力の保管 |

## 使い方

### A. フルビルド（ゼロから作り直す）

色別HTMLダンプ（`red.html` など）をカレントに置いて実行:

```bash
python readdata.py
# -> opcg_cards.json / opcg_images.json を全量で再生成
```

### B. 差分取り込み（新弾の追加）★

新規追加カードのHTMLを渡すと、既存 `opcg_cards.json` に**新カードだけ追加**される。

```bash
python update_cards.py 新弾.html
```

- 未登録の番号 → 末尾に追加（`id` は連番の続き）
- 既存番号でもブロックアイコンが新しい**再録**なら、その場で更新（`id` は維持）
- 既存と同じ（または古い）版は skip（何度流しても結果が変わらない=冪等）
- `opcg_images_new.json` に「新規 or 画像URLが変わった分」だけを書き出す

### 画像の取得

```bash
# 新カードのみ取得（差分取り込み直後）
python storeimage.py opcg_images_new.json

# 全量から不足分のみ取得（引数なし。既存ファイルはスキップ）
python storeimage.py
```

画像は `opcg_images.json` 上の並び順で 700 件ごとに `card_images/1/`, `card_images/2/`,
… へ振り分ける。差分取得でもシャード位置は全量ビルドと一致する。

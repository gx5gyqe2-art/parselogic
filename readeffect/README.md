# readeffect — OPCG カードデータ取り込み

ワンピースカードゲーム公式サイトのカード一覧HTMLを解析して、カードデータJSONと
画像を生成・取得するツール群。

## ファイル

| ファイル | 役割 |
| --- | --- |
| `readdata.py` | HTML解析の本体。フルビルド（全HTMLから作り直し）と、再利用可能なパース関数を提供 |
| `update_cards.py` | **差分取り込み**。同階層のHTMLを自動読み込みし、マージ＋新カード画像取得まで1コマンドで実行 |
| `storeimage.py` | 画像ダウンローダ（700件ごとにサブフォルダ分割） |
| `opcg_cards.json` | **マスター**: 全カードデータ（唯一の正）|
| `opcg_images.json` | **マスター**: 全カードの画像URL（`opcg_cards.json` と番号が一致）|
| `opcg_images_new.json` | 差分取り込みが出力する「今回取得すべき画像だけ」のリスト（gitignore）|
| `old/` | 過去の生HTMLダンプ・旧出力の保管 |

## ⚠ 入力は必ず「HTMLソース」（テキスト保存は不可）

差分取り込みのパーサは `<dl class="modalCol">` などのHTMLタグを前提にしている。

- ✅ **ページのソースHTML**（`modalCol` や画像URL `data-src` を含む）→ 正しく読める
- ❌ **テキスト保存 / リーダー表示のコピー** → タグ・画像URL・属性が消え、**0枚**しか
  読めない（「差分なし」になる典型原因）

取り込むカードを人の目で絞りたい場合は、HTMLソースの中の不要な
`<dl class="modalCol"> … </dl>` ブロックを削れば、残したカードだけが取り込まれる。

## 使い方

### A. フルビルド（ゼロから作り直す）

色別HTMLダンプ（`red.html` など）をカレントに置いて実行:

```bash
python readdata.py
# -> opcg_cards.json / opcg_images.json を全量で再生成
```

### B. 差分取り込み（新弾の追加）★ ＝ 1コマンドで完結

新規追加カードのHTMLを **`readeffect/` 直下に置いて** 実行するだけ。
マージ → 差分抽出 → **新カードの画像取得まで自動で行う**。

```bash
cd readeffect
python update_cards.py            # 同じ階層の *.html を全て自動読み込み
```

- HTMLは引数指定も可能（`python update_cards.py 新弾.html`）。無指定なら同階層の `*.html` を全読み込み
- 未登録の番号 → 末尾に追加（`id` は連番の続き）
- 既存番号でもブロックアイコンが新しい**再録**なら、その場で更新（`id` は維持）
- 既存と同じ（または古い）版は skip（何度流しても結果が変わらない=冪等）
- `opcg_images_new.json`（新規＋画像URLが変わった分）を書き出し、その分だけを `card_images/` へ取得
- 画像取得を止めたいときは `--no-image` を付ける（マージのみ）

> 注: `old/` は過去ダンプの保管場所で **自動読み込みの対象外**（毎回2MB級の色別ダンプを
> 読み直さないため）。差分取り込みする新弾HTMLは `readeffect/` 直下に置く。

### 画像だけを別途取得したい場合

```bash
python storeimage.py opcg_images_new.json   # 差分（新カード）のみ
python storeimage.py                        # 全量から不足分のみ（既存はスキップ）
```

画像は `opcg_images.json` 上の並び順で 700 件ごとに `card_images/1/`, `card_images/2/`,
… へ振り分ける。差分取得でもシャード位置は全量ビルドと一致する。

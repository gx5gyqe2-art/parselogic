"""差分取り込み: 新カードのHTMLを既存マスターへマージし、新カード画像まで取得する。

使い方:
    python update_cards.py                # 同じ階層(カレント)の *.html を全て自動読み込み
    python update_cards.py 新弾.html      # ファイルを明示指定することも可能
    python update_cards.py --no-image     # 画像の取得はスキップ（マージのみ）

やること（1コマンドで完結）:
  1) 既存 opcg_cards.json / opcg_images.json を読み込む（無ければ空から開始）。
  2) HTMLを解析し、
       - 未登録の番号 -> 新カードとして末尾に追加（idは連番の続き）
       - 既存番号でも block_rank（ブロックアイコン）が新しい再録 -> その場で更新（idは維持）
     を行う。
  3) 画像は「新規 or URLが変わった（リーダーのパラレル差し替え等）」ものだけを
     opcg_images_new.json に書き出し、その分だけを card_images/ へダウンロードする。
     opcg_images.json 本体もマージ後の全量で更新する。

出力:
    opcg_cards.json        マージ後の全カード（マスター更新）
    opcg_images.json       マージ後の全画像URL（マスター更新）
    opcg_images_new.json   今回追加/変更された画像URLだけの差分
    card_images/           新カード分の画像（--no-image 指定時は取得しない）
"""
import glob
import json
import os
import sys

from readdata import (
    parse_html_files,
    dedup_cards,
    block_rank,
    select_images,
    ordered_card,
)
import storeimage

CARDS_PATH = "opcg_cards.json"
IMAGES_PATH = "opcg_images.json"
NEW_IMAGES_PATH = "opcg_images_new.json"


def load_json(path, default):
    if not os.path.exists(path):
        print(f"注意: {path} が見つからないため、空から開始します。")
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main(argv):
    no_image = "--no-image" in argv
    args = [a for a in argv if a != "--no-image"]

    # 引数でHTMLを明示指定していればそれを、無ければ同じ階層の *.html を全て自動読み込み
    html_files = [a for a in args if a.lower().endswith(".html")]
    if not html_files:
        html_files = sorted(glob.glob("*.html"))
    if not html_files:
        print("HTMLが見つかりません。カレントに *.html を置くか、引数でファイルを指定してください。")
        return 1
    for f in html_files:
        if not os.path.exists(f):
            print(f"エラー: HTMLが見つかりません: {f}")
            return 1
    print(f"読み込み対象HTML: {[os.path.basename(f) for f in html_files]}")

    # 既存マスターの読み込み
    master = load_json(CARDS_PATH, [])
    base_images = load_json(IMAGES_PATH, {})

    existing_by_num = {c["number"]: c for c in master}
    max_id = max((c.get("id", 0) for c in master), default=0)

    # 新HTMLを解析（出現順の生カード）→ 番号ごとに新しい再録を優先して集約
    new_all_cards = parse_html_files(html_files)
    new_unique = dedup_cards(new_all_cards)

    added, updated, skipped = [], [], []
    for num, raw in new_unique.items():
        if num not in existing_by_num:
            max_id += 1
            card = ordered_card(num, raw, max_id)
            master.append(card)
            existing_by_num[num] = card
            added.append(num)
        else:
            ex = existing_by_num[num]
            if block_rank(raw) > block_rank(ex):
                # 再録（より新しいブロックアイコン）: idを維持して中身を差し替え
                idx = master.index(ex)
                card = ordered_card(num, raw, ex["id"])
                master[idx] = card
                existing_by_num[num] = card
                updated.append(num)
            else:
                skipped.append(num)

    # 画像: 既存マップを土台に、新HTML分の選定をマージ
    merged_images = select_images(new_all_cards, base=base_images)
    # 差分（新規 or URL変更）だけを抽出
    delta_images = {num: url for num, url in merged_images.items()
                    if base_images.get(num) != url}

    # 書き出し
    with open(CARDS_PATH, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=2)
    with open(IMAGES_PATH, "w", encoding="utf-8") as f:
        json.dump(merged_images, f, ensure_ascii=False, indent=2)
    with open(NEW_IMAGES_PATH, "w", encoding="utf-8") as f:
        json.dump(delta_images, f, ensure_ascii=False, indent=2)

    print("-" * 30)
    print(f"新規追加     : {len(added)} 件 {added if added else ''}")
    print(f"再録で更新   : {len(updated)} 件 {updated if updated else ''}")
    print(f"変更なしskip : {len(skipped)} 件")
    print(f"取得対象画像 : {len(delta_images)} 件 -> {NEW_IMAGES_PATH}")
    print(f"マスター件数 : {len(master)} 件 -> {CARDS_PATH}")

    # 新カード分の画像をそのまま取得（storeimage を内部呼び出し＝保存処理を統一）
    if delta_images and not no_image:
        print("-" * 30)
        print("新カードの画像を取得します...")
        storeimage.download_images(full_path=IMAGES_PATH, only_path=NEW_IMAGES_PATH)
    elif no_image:
        print(f"(--no-image 指定のため画像取得はスキップ / 後で: python storeimage.py {NEW_IMAGES_PATH})")
    else:
        print("取得すべき新規画像はありません。")

    print("完了しました!")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

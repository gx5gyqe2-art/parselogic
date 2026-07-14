import json
import glob
import os
from html.parser import HTMLParser

class CardAndImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards = []
        self.image_urls = {} # {カード番号: 画像URL}
        self.current_card = {}

        self.in_modal_col = False
        self.current_target_class = None
        self.in_label_tag = False

        self.label_buffer = ""
        self.value_buffer = ""

        self.class_map = {
            'power': 'パワー', 'attribute': '属性', 'counter': 'カウンター',
            'color': '色', 'feature': '特徴', 'text': '効果(テキスト)',
            'trigger': '効果(トリガー)', 'cost': 'コスト', 'block_icon': 'ブロックアイコン'
        }

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = attrs_dict.get('class', '').split()

        if tag == 'dl' and 'modalCol' in classes:
            self.in_modal_col = True
            self.current_card = {}
            return

        if not self.in_modal_col: return

        # 画像URLの抽出
        if tag == 'img' and 'lazy' in classes:
            img_src = attrs_dict.get('data-src') or attrs_dict.get('src')
            if img_src:
                full_url = "https://www.onepiece-cardgame.com" + img_src.replace('..', '')
                self.current_card['image_url'] = full_url

        if tag == 'div':
            # HTMLクラス "block" を内部識別子 block_icon にマッピング
            if 'block' in classes and 'block_icon' in self.class_map:
                self.current_target_class = 'block_icon'
                self.label_buffer = ""
                self.value_buffer = ""
                return
            if 'cardName' in classes:
                self.current_target_class = 'cardName'
                self.value_buffer = ""
                return
            if 'infoCol' in classes:
                 self.current_target_class = 'infoCol'
                 self.value_buffer = ""
                 return
            for cls_key in self.class_map.keys():
                if cls_key in classes:
                    self.current_target_class = cls_key
                    self.label_buffer = ""
                    self.value_buffer = ""
                    return

        if tag == 'h3' and self.current_target_class:
            self.in_label_tag = True

        if tag == 'img' and self.current_target_class == 'attribute':
            self.value_buffer += attrs_dict.get('alt', '')

        if tag == 'br' and self.current_target_class and not self.in_label_tag:
            self.value_buffer += " / "

    def handle_data(self, data):
        if not self.current_target_class: return
        if self.in_label_tag:
            self.label_buffer += data
        else:
            self.value_buffer += data

    def handle_endtag(self, tag):
        if tag == 'h3':
            self.in_label_tag = False
            return

        if tag == 'div' and self.current_target_class:
            if self.current_target_class == 'cardName':
                self.current_card['name'] = self.value_buffer.strip()
            elif self.current_target_class == 'infoCol':
                full_text = self.value_buffer.replace("\n", "").strip()
                parts = [p.strip() for p in full_text.split('|')]
                if len(parts) >= 1: self.current_card['number'] = parts[0]
                if len(parts) >= 3:
                    raw_type = parts[2]
                    type_map = {"LEADER": "リーダー", "CHARACTER": "キャラクター", "EVENT": "イベント", "STAGE": "ステージ"}
                    self.current_card['種類'] = type_map.get(raw_type, raw_type)
            elif self.current_target_class in self.class_map:
                final_val = self.value_buffer.strip()
                json_key = self.class_map[self.current_target_class]
                if self.current_target_class == 'cost' and "ライフ" in self.label_buffer:
                    json_key = "ライフ"
                if final_val and final_val != "-":
                     self.current_card[json_key] = " ".join(final_val.split())

            self.current_target_class = None
            self.label_buffer = ""
            self.value_buffer = ""

        if tag == 'dl' and self.in_modal_col:
            num = self.current_card.get('number')
            if num:
                 self.cards.append(self.current_card)
                 # クラス内では一旦すべて保持しておきます（選定はmainで行うため）
                 self.image_urls[num] = self.current_card.get('image_url')
            self.in_modal_col = False


# ---------------------------------------------------------------------------
# 共通ロジック（フルビルド main() と差分取り込み update_cards.py の両方で使う）
# ---------------------------------------------------------------------------

# 出力カードのキー並び（number / name の後ろに続く順序）
KEYS_ORDER = ["種類", "コスト", "ライフ", "色", "ブロックアイコン", "属性",
              "パワー", "カウンター", "効果(テキスト)", "効果(トリガー)", "特徴"]


def parse_html_files(files):
    """HTMLファイル群を解析し、出現順の生カードリストを返す（重複除去なし）。"""
    all_cards = []
    for f in files:
        print(f"解析中: {os.path.basename(f)}")
        parser = CardAndImageParser()
        with open(f, 'r', encoding='utf-8') as file_obj:
            parser.feed(file_obj.read())
        all_cards.extend(parser.cards)
    return all_cards


def block_rank(card):
    """ブロックアイコン（再録の新しさ）を数値化。'X'や未設定は最古扱い。"""
    try:
        return int(card.get("ブロックアイコン", ""))
    except (ValueError, TypeError):
        return -1


def select_images(all_cards, base=None):
    """カード出現順から画像URLを選定して {番号: URL} を返す。

    基本は先勝ち（通常版を維持）。「リーダー」のみ後発URL（パラレル）で上書き。
    base を渡すと既存の画像マップを土台にマージする（差分取り込み用）。
    """
    images = dict(base) if base else {}
    for card in all_cards:
        num = card.get('number')
        url = card.get('image_url')
        c_type = card.get('種類')  # "リーダー", "キャラクター" etc

        if not num or not url:
            continue

        # まだ未登録 -> 登録（基本の通常版）
        if num not in images:
            images[num] = url
        # 既に登録済み -> リーダーのみ後発URL（パラレル）で上書き
        elif c_type == "リーダー":
            images[num] = url
    return images


def dedup_cards(all_cards):
    """同一番号は block_rank の大きい（新しい再録）版を優先して {番号: card} を返す。"""
    unique = {}
    for c in all_cards:
        num = c.get("number")
        if not num:
            continue
        if num not in unique or block_rank(c) > block_rank(unique[num]):
            unique[num] = c
    return unique


def ordered_card(num, data, card_id):
    """パーサの生データを出力形式（id/number/name + KEYS_ORDER）に整形する。"""
    ordered = {"id": card_id, "number": num, "name": data.get("name", "")}
    for k in KEYS_ORDER:
        if k in data:
            ordered[k] = data[k]
    return ordered


def main():
    # cwd（Pythonistaでは別の場所になりがち）に依存せず、スクリプトの場所を基準にする
    here = os.path.dirname(os.path.abspath(__file__))
    html_files = sorted(glob.glob(os.path.join(here, "*.html")))
    if not html_files:
        print("HTMLファイルが見つかりません。")
        return

    # 解析（出現順の生カードリスト）
    all_cards = parse_html_files(html_files)

    # 画像URLの選定
    all_images = select_images(all_cards)

    # カード詳細データの重複除去（再録は新しい版を優先）
    unique_cards = dedup_cards(all_cards)

    # 1. カード詳細データ保存
    final_cards = [ordered_card(num, data, i)
                   for i, (num, data) in enumerate(unique_cards.items(), 1)]

    with open(os.path.join(here, 'opcg_cards.json'), 'w', encoding='utf-8') as f:
        json.dump(final_cards, f, ensure_ascii=False, indent=2)

    # 2. 画像URLリスト保存
    with open(os.path.join(here, 'opcg_images.json'), 'w', encoding='utf-8') as f:
        json.dump(all_images, f, ensure_ascii=False, indent=2)

    print("-" * 20)
    print(f"カードデータ: opcg_cards.json")
    print(f"画像URLリスト: opcg_images.json")
    print(f"完了しました!")

if __name__ == "__main__":
    main()

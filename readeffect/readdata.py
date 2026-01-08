import json
import glob
import os
from html.parser import HTMLParser

class CardAndImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards = []
        self.image_urls = {} # {カード番号: 画像URL}
        self.current_card = {}
        
        self.in_modal_col = False
        self.current_target_class = None
        self.in_label_tag = False
        
        self.label_buffer = ""
        self.value_buffer = ""
        
        self.class_map = {
            'power': 'パワー', 'attribute': '属性', 'counter': 'カウンター',
            'color': '色', 'feature': '特徴', 'text': '効果(テキスト)',
            'trigger': '効果(トリガー)', 'cost': 'コスト' 
        }

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = attrs_dict.get('class', '').split()
        
        if tag == 'dl' and 'modalCol' in classes:
            self.in_modal_col = True
            self.current_card = {}
            return

        if not self.in_modal_col: return

        # 画像URLの抽出 (frontColクラス内のimgタグから取得)
        if tag == 'img' and 'lazy' in classes:
            # 公式サイトは通常 data-src に実際の画像パスが入っています
            img_src = attrs_dict.get('data-src') or attrs_dict.get('src')
            if img_src:
                # 相対パスを絶対URLに変換したい場合はドメインを付与
                full_url = "https://www.onepiece-cardgame.com" + img_src.replace('..', '')
                self.current_card['image_url'] = full_url

        if tag == 'div':
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

        if tag == 'br' and self.current_target_class:
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
                    type_map = {"LEADER": "リーダー", "CHARACTER": "キャラクター", "EVENT": "イベント", "STAGE": "ステージ"}
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
                 # 画像URLリスト用に保存
                 if 'image_url' in self.current_card:
                     self.image_urls[num] = self.current_card['image_url']
            self.in_modal_col = False

def main():
    html_files = glob.glob("*.html")
    if not html_files:
        print("HTMLファイルが見つかりません。")
        return

    all_cards = []
    all_images = {}

    for f in html_files:
        print(f"解析中: {os.path.basename(f)}")
        parser = CardAndImageParser()
        with open(f, 'r', encoding='utf-8') as file_obj:
            parser.feed(file_obj.read())
        all_cards.extend(parser.cards)
        all_images.update(parser.image_urls)

    # 重複除去
    unique_cards = {}
    for c in all_cards:
        num = c.get("number")
        if num and num not in unique_cards:
            unique_cards[num] = c

    # 1. カード詳細データ保存 (画像URLは含めない)
    final_cards = []
    keys_order = ["種類", "コスト", "ライフ", "色", "属性", "パワー", "カウンター", "効果(テキスト)", "効果(トリガー)", "特徴"]
    for i, (num, data) in enumerate(unique_cards.items(), 1):
        ordered = {"id": i, "number": num, "name": data.get("name", "")}
        for k in keys_order:
            if k in data: ordered[k] = data[k]
        final_cards.append(ordered)

    with open('opcg_cards_refined.json', 'w', encoding='utf-8') as f:
        json.dump(final_cards, f, ensure_ascii=False, indent=2)

    # 2. 画像URLリストのみを別ファイルで保存
    with open('opcg_images.json', 'w', encoding='utf-8') as f:
        json.dump(all_images, f, ensure_ascii=False, indent=2)

    print("-" * 20)
    print(f"カードデータ: opcg_cards_refined.json")
    print(f"画像URLリスト: opcg_images.json")
    print(f"完了しました!")

if __name__ == "__main__":
    main()

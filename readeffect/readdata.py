import json
import glob
import os
from html.parser import HTMLParser

class CardParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards = []
        self.current_card = {}
        
        # 処理中の状態を管理するフラグ
        self.in_modal_col = False
        self.current_target_class = None
        self.in_label_tag = False
        
        # 文字列を一時的にためておく場所
        self.label_buffer = ""
        self.value_buffer = ""
        
        # HTMLのクラス名と、出力するJSONのキー名の対応表
        # ここに定義されている項目のみを抽出します
        self.class_map = {
            'power': 'パワー',
            'attribute': '属性',
            'counter': 'カウンター',
            'color': '色',
            'feature': '特徴',
            'text': '効果(テキスト)',
            'trigger': '効果(トリガー)',
            'cost': 'コスト' 
        }

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = attrs_dict.get('class', '').split()
        
        # カード全体のブロック開始
        if tag == 'dl' and 'modalCol' in classes:
            self.in_modal_col = True
            self.current_card = {}
            return

        if not self.in_modal_col: return

        # 各項目のブロック開始
        if tag == 'div':
            # 1. カード名
            if 'cardName' in classes:
                self.current_target_class = 'cardName'
                self.value_buffer = ""
                return
            
            # 2. 基本情報(番号や種類が入っている場所)
            if 'infoCol' in classes:
                 self.current_target_class = 'infoCol'
                 self.value_buffer = ""
                 return

            # 3. ステータス項目(パワー、コスト、属性など)
            for cls_key in self.class_map.keys():
                if cls_key in classes:
                    self.current_target_class = cls_key
                    self.label_buffer = "" # ラベル用バッファをリセット
                    self.value_buffer = "" # 値用バッファをリセット
                    return
        
        # ラベル部分(h3タグ)の開始
        if tag == 'h3' and self.current_target_class:
            self.in_label_tag = True
            
        # 画像(属性アイコン)の処理
        if tag == 'img' and self.current_target_class == 'attribute':
            val = attrs_dict.get('alt', '')
            self.value_buffer += val

        # 改行の処理
        if tag == 'br' and self.current_target_class:
            self.value_buffer += " / "

    def handle_data(self, data):
        if not self.current_target_class: return
        
        # 【重要】h3タグの中にいる時はラベルとして、それ以外は値として保存
        if self.in_label_tag:
            self.label_buffer += data
        else:
            self.value_buffer += data

    def handle_endtag(self, tag):
        # ラベル終了
        if tag == 'h3':
            self.in_label_tag = False
            return

        # 項目終了:データを確定して保存
        if tag == 'div' and self.current_target_class:
            
            # A. カード名
            if self.current_target_class == 'cardName':
                self.current_card['name'] = self.value_buffer.strip()
            
            # B. 基本情報
            elif self.current_target_class == 'infoCol':
                full_text = self.value_buffer.replace("\n", "").strip()
                parts = [p.strip() for p in full_text.split('|')]
                if len(parts) >= 1: self.current_card['number'] = parts[0]
                if len(parts) >= 3: 
                    raw_type = parts[2]
                    # 英語表記を日本語へ変換
                    type_map = {"LEADER": "リーダー", "CHARACTER": "キャラクター", "EVENT": "イベント", "STAGE": "ステージ"}
                    self.current_card['種類'] = type_map.get(raw_type, raw_type)
            
            # C. ステータス項目
            elif self.current_target_class in self.class_map:
                final_val = self.value_buffer.strip()
                
                # 保存するキー名を決定
                json_key = self.class_map[self.current_target_class]
                
                # 特例:コスト欄に「ライフ」と書いてあったらキーを「ライフ」に変更
                if self.current_target_class == 'cost' and "ライフ" in self.label_buffer:
                    json_key = "ライフ"
                
                # 値があり、かつ "-" でなければ保存
                if final_val and final_val != "-":
                     # 余計な空白を削除して整形
                     cleaned_val = " ".join(final_val.split())
                     self.current_card[json_key] = cleaned_val

            # 処理が終わったらリセット
            self.current_target_class = None
            self.label_buffer = ""
            self.value_buffer = ""
        
        # カード情報の終了
        if tag == 'dl' and self.in_modal_col:
            if self.current_card.get('number'):
                 self.cards.append(self.current_card)
            self.in_modal_col = False

def main():
    # フォルダ内のHTMLファイルを検索
    html_files = glob.glob("*.html")
    if not html_files:
        print("HTMLファイルが見つかりません。")
        return

    print(f"対象ファイル数: {len(html_files)}")
    all_cards = []

    for f in html_files:
        print(f"解析中: {os.path.basename(f)}")
        parser = CardParser()
        try:
            with open(f, 'r', encoding='utf-8') as file_obj:
                content = file_obj.read()
                parser.feed(content)
            all_cards.extend(parser.cards)
        except Exception as e:
            print(f"エラー発生: {e}")

    # 重複除去(カード番号をキーにする)
    unique_cards = {}
    for c in all_cards:
        num = c.get("number")
        if num and num not in unique_cards:
            unique_cards[num] = c

    # 出力データの整形
    final_list = []
    keys_order = ["種類", "コスト", "ライフ", "色", "属性", "パワー", "カウンター", "効果(テキスト)", "効果(トリガー)", "特徴"]

    for i, (num, data) in enumerate(unique_cards.items(), 1):
        ordered = {
            "id": i,
            "number": num,
            "name": data.get("name", "")
        }
        for k in keys_order:
            if k in data:
                ordered[k] = data[k]
        final_list.append(ordered)

    # JSONファイルとして保存
    output_filename = 'opcg_cards_refined.json'
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)

    print("-" * 20)
    print("完了しました!")
    print(f"合計 {len(final_list)} 枚")
    print(f"保存先: {output_filename}")

if __name__ == "__main__":
    main()

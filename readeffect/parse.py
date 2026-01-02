import json
import re
import unicodedata
from opcg_const import RAW_PATTERNS  # 定義ファイルからインポート

def verify_opcg_grammar_v25_0(cards):
    
    normalized_patterns = []
    # RAW_PATTERNS を使用して正規化処理を行う
    for pat, tag in RAW_PATTERNS:
        normalized_patterns.append((unicodedata.normalize('NFKC', pat), tag))

    # 文字列長順にソート（最長一致させるため）
    sorted_patterns = sorted(normalized_patterns, key=lambda x: len(x[0]), reverse=True)

    total_cards = 0
    pure_success = 0
    error_logs = []

    for card in cards:
        text = card.get('効果(テキスト)')
        if not text or text == '-': continue
        
        # テキストの正規化
        text = unicodedata.normalize('NFKC', text)
        replacements = {'1':'1', '2':'2', '3':'3', '4':'4', '5':'5', 
                        '6':'6', '7':'7', '8':'8', '9':'9', '10':'10',
                        '➀':'1', '➁':'2', '➂':'3', '➃':'4', '➄':'5', 
                        '➅':'6', '➆':'7', '➇':'8', '➈':'9', '➉':'10'}
        for k, v in replacements.items():
            text = text.replace(k, v)
        
        total_cards += 1
        working_text = text
        
        # 定義されたパターンで置換を実行
        for pat, tag in sorted_patterns:
            working_text = re.sub(pat, tag, working_text)
        
        clean_template = re.sub(r'\s+', ' ', working_text).strip()
        has_japanese = bool(re.search(r'[ぁ-んァ-ン一-龥]', clean_template))
        
        if not has_japanese:
            pure_success += 1
        else:
            error_logs.append({'name': card.get('name'), 'res': clean_template})

    output = f"Total: {total_cards} | Success: {pure_success} | Coverage: {pure_success/total_cards*100:.2f}%\n"
    output += "-" * 40 + "\n"
    for log in error_logs[:15]:
        output += f"[{log['name']}]\n Res: '{log['res']}'\n" + "-"*20 + "\n"
    return output

if __name__ == "__main__":
    with open('opcg_cards.json', 'r', encoding='utf-8') as f:
        cards = json.load(f)
    print(verify_opcg_grammar_v25_0(cards))

import json
import os
import urllib.request
import time

def download_images(json_path, save_dir='card_images'):
    # 1. JSONファイルを読み込む
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            image_data = json.load(f)
    except Exception as e:
        print(f"JSONの読み込みに失敗しました: {e}")
        return

    # 2. 保存用フォルダを作成
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"フォルダ '{save_dir}' を作成しました。")

    total = len(image_data)
    print(f"合計 {total} 件のダウンロードを開始します...")

    # 3. 各URLをダウンロード
    success_count = 0
    for i, (card_num, url) in enumerate(image_data.items(), 1):
        # ファイル名を決定 (例: EB01-021.png)
        # クエリパラメータ(?以降)を除去して拡張子を取得
        clean_url = url.split('?')[0]
        ext = os.path.splitext(clean_url)[1]
        if not ext:
            ext = '.png' # デフォルト
        
        file_name = f"{card_num}{ext}"
        save_path = os.path.join(save_dir, file_name)

        # すでにファイルが存在する場合はスキップ(再開時などに便利)
        if os.path.exists(save_path):
            print(f"[{i}/{total}] スキップ: {file_name} (存在します)")
            continue

        try:
            # ダウンロード実行
            print(f"[{i}/{total}] ダウンロード中: {file_name}...", end='\r')
            urllib.request.urlretrieve(url, save_path)
            success_count += 1
            # サーバーに負荷をかけすぎないよう、わずかに待機
            time.sleep(0.1) 
        except Exception as e:
            print(f"\n[{i}/{total}] 失敗: {file_name} - {e}")

    print(f"\n" + "-"*20)
    print(f"完了しました!")
    print(f"成功: {success_count} 件")
    print(f"保存先: {os.path.abspath(save_dir)}")

if __name__ == "__main__":
    # JSONファイル名を指定して実行
    download_images('opcg_images.json')

import json
import os
import urllib.request
import time

def download_images(json_path, save_dir='card_images'):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            image_data = json.load(f)
    except Exception as e:
        print(f"JSONの読み込みに失敗しました: {e}")
        return

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"フォルダ '{save_dir}' を作成しました。")

    total = len(image_data)
    print(f"合計 {total} 件のダウンロードを開始します（上書き・700件分割モード）...")

    success_count = 0
    files_per_dir = 700  # 1つのフォルダに入れるファイル数

    for i, (card_num, url) in enumerate(image_data.items(), 1):
        # サブディレクトリ番号を算出 (1, 2, 3...)
        sub_dir_num = (i - 1) // files_per_dir + 1
        current_save_dir = os.path.join(save_dir, str(sub_dir_num))

        # サブディレクトリがなければ作成
        if not os.path.exists(current_save_dir):
            os.makedirs(current_save_dir)

        clean_url = url.split('?')[0]
        ext = os.path.splitext(clean_url)[1]
        if not ext:
            ext = '.png'
        
        file_name = f"{card_num}{ext}"
        # 保存パスにサブディレクトリを含める
        save_path = os.path.join(current_save_dir, file_name)

        # 同名ファイルスキップ処理は無効化(上書きモード)
        # if os.path.exists(save_path):
        #     print(f"[{i}/{total}] スキップ: {file_name} (存在します)")
        #     continue

        try:
            print(f"[{i}/{total}] ダウンロード中: {sub_dir_num}/{file_name}...", end='\r')
            urllib.request.urlretrieve(url, save_path)
            success_count += 1
            time.sleep(0.1) 
        except Exception as e:
            print(f"\n[{i}/{total}] 失敗: {file_name} - {e}")

    print(f"\n" + "-"*20)
    print(f"完了しました!")
    print(f"成功: {success_count} 件")
    print(f"保存先: {os.path.abspath(save_dir)}")

if __name__ == "__main__":
    download_images('opcg_images.json')

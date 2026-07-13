import json
import os
import sys
import urllib.request
import time


def load_map(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def download_images(full_path="opcg_images.json", only_path=None,
                    save_dir="card_images", skip_existing=True):
    """画像をダウンロードする。

    full_path : シャード（700件分割）の並び基準となる全量マップ。
    only_path : 指定するとそのファイルに載っている番号だけを取得（= 新カードのみ）。
                差分取得では URL が変わっている可能性があるため常に上書きする。
    skip_existing : 全量取得（only_path 未指定）時、既存ファイルはスキップして冪等にする。
    """
    try:
        full = load_map(full_path)
    except Exception as e:
        print(f"JSONの読み込みに失敗しました({full_path}): {e}")
        return

    only = None
    if only_path:
        try:
            only = set(load_map(only_path).keys())
        except Exception as e:
            print(f"差分リストの読み込みに失敗しました({only_path}): {e}")
            return
        print(f"差分モード: {only_path} の {len(only)} 件のみ取得します。")

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"フォルダ '{save_dir}' を作成しました。")

    files_per_dir = 700  # 1つのフォルダに入れるファイル数
    total_targets = len(only) if only is not None else len(full)
    print(f"対象 {total_targets} 件のダウンロードを開始します（700件分割モード）...")

    success_count = 0
    skip_count = 0
    done = 0

    for i, (card_num, url) in enumerate(full.items(), 1):
        # シャード番号は全量マップ上の位置で決める（差分でも配置が全量ビルドと一致する）
        sub_dir_num = (i - 1) // files_per_dir + 1

        # 取得対象か判定
        if only is not None and card_num not in only:
            continue

        current_save_dir = os.path.join(save_dir, str(sub_dir_num))
        if not os.path.exists(current_save_dir):
            os.makedirs(current_save_dir)

        clean_url = url.split('?')[0]
        ext = os.path.splitext(clean_url)[1]
        if not ext:
            ext = '.png'

        file_name = f"{card_num}{ext}"
        save_path = os.path.join(current_save_dir, file_name)

        # 全量モードでは既存はスキップ（冪等 = 実質「不足分のみ取得」）。
        # 差分モードでは URL 差し替えの可能性があるため上書きする。
        if only is None and skip_existing and os.path.exists(save_path):
            skip_count += 1
            continue

        done += 1
        try:
            print(f"[{done}/{total_targets}] ダウンロード中: {sub_dir_num}/{file_name}...", end='\r')
            urllib.request.urlretrieve(url, save_path)
            success_count += 1
            time.sleep(0.1)
        except Exception as e:
            print(f"\n失敗: {file_name} - {e}")

    print("\n" + "-" * 20)
    print(f"完了しました!")
    print(f"成功: {success_count} 件 / スキップ(既存): {skip_count} 件")
    print(f"保存先: {os.path.abspath(save_dir)}")


if __name__ == "__main__":
    # 引数に差分リスト（opcg_images_new.json 等）を渡すと新カードのみ取得。
    # 引数なしなら全量から不足分のみ取得。
    only_arg = sys.argv[1] if len(sys.argv) > 1 else None
    download_images(only_path=only_arg)

"""公式サイトからカード一覧HTMLを直接取得して差分取り込みまで行う（iPhone/Pythonista対応）。

なぜ必要か:
  ページを「テキスト保存」すると HTMLタグ・画像URL・属性アイコンが失われ、
  readdata.py のパーサ（<dl class="modalCol"> を前提）が1枚も読めない。
  このスクリプトは公式サイトへ直接リクエストして「本物のHTML」を取得するので、
  手動保存の失敗が起きない。

使い方（Pythonista 3 でもPCでも）:
  1) まず一度そのまま Run する。SERIES が空なので、取り込み可能な
     「シリーズ名 → コード」一覧が表示される。
  2) 取り込みたい新弾のコードを下の SERIES に書いて、もう一度 Run。
     例: SERIES = ["550116"]   # ブースターパック 決戦の刻【OP-16】
     取得 → 既存マスターへ差分マージ → 新カード画像の取得までを自動で行う。

  複数まとめても可: SERIES = ["550116", "550030"]

取得したHTMLは update_cards.py と同じフォルダに series_<コード>.html として保存される。
"""
import os
import re
import sys
import html as htmllib
import urllib.request
import urllib.parse

# ★ここに取り込みたいシリーズコードを入れて Run（空なら一覧表示のみ）
SERIES = []

# 画像取得までは不要でマージだけしたいときは True
NO_IMAGE = False

BASE_URL = "https://www.onepiece-cardgame.com/cardlist/"
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"

# cwd（Pythonistaでは別の場所になりがち）に依存しないため、スクリプトの場所を基準にする
HERE = os.path.dirname(os.path.abspath(__file__))


def _clean(s):
    s = re.sub(r'<br[^>]*>', ' ', s)
    s = re.sub(r'<[^>]+>', '', s)
    return htmllib.unescape(s).strip()


def fetch_series_list():
    """取り込み可能な (コード, 名前) の一覧を公式サイトから取得する。"""
    req = urllib.request.Request(BASE_URL, headers={"User-Agent": UA})
    page = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    opts = re.findall(r'<option value="(\d+)"[^>]*>(.*?)</option>', page, re.S)
    return [(code, _clean(name)) for code, name in opts]


def fetch_series_html(code):
    """1シリーズ分のHTMLを取得し、HERE/series_<code>.html に保存してパスを返す。"""
    data = urllib.parse.urlencode({"series": code, "freeword": ""}).encode()
    req = urllib.request.Request(
        BASE_URL, data=data,
        headers={"User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded"})
    html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
    n = html.count("modalCol")
    path = os.path.join(HERE, f"series_{code}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"取得: series={code}  カード枠(modalCol)={n}  -> {os.path.basename(path)}")
    if n == 0:
        print(f"  ⚠ カードが0枠です。コード {code} が正しいか確認してください。")
    return path


def main():
    if not SERIES:
        print("SERIES が空です。下記から取り込みたいコードを SERIES に設定して再実行してください。\n")
        try:
            for code, name in fetch_series_list():
                print(f"  {code}  {name}")
        except Exception as e:
            print(f"シリーズ一覧の取得に失敗しました: {e}")
            return 1
        print('\n例: SERIES = ["550116"]  # OP-16')
        return 0

    paths = []
    for code in SERIES:
        try:
            paths.append(fetch_series_html(str(code)))
        except Exception as e:
            print(f"取得失敗 series={code}: {e}")
    if not paths:
        print("取得できたHTMLがありません。")
        return 1

    # 取得したHTMLをそのまま差分取り込みへ（マージ＋新カード画像取得）
    import update_cards
    argv = list(paths)
    if NO_IMAGE:
        argv.append("--no-image")
    print("-" * 30)
    return update_cards.main(argv)


if __name__ == "__main__":
    sys.exit(main())

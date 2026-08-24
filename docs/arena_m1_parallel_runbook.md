# アリーナ A/B 測定（マクロ手化 P1・配分箱）6ワーカー並列 runbook

対象リポジトリ: `gx5gyqe2-art/opcg-sim-backend`
測定ブランチ: `claude/cpu-spec-improvements-yw91jd`（HEAD `f62615ff` = `--cand-macro` フラグと `macro_moves` seam を含む）
候補ネット: 同梱の `opcg_sim/data/learned/gen15_{value,policy}.npz`（追加の復元不要）

## 割り当て

| シャード | 条件 | seed-base | ペア数 | 退避ブランチ |
|---|---|---|---|---|
| k=1 | random | 781000 | 32 | `claude/arena-m1-shard1` |
| k=2 | random | 782000 | 32 | `claude/arena-m1-shard2` |
| k=3 | random | 783000 | 32 | `claude/arena-m1-shard3` |
| k=4 | fixed  | 784000 | 32 | `claude/arena-m1-shard4` |
| k=5 | fixed  | 785000 | 32 | `claude/arena-m1-shard5` |
| k=6 | fixed  | 786000 | 32 | `claude/arena-m1-shard6` |

`plan_bands(pairs=32, bands=2, seed_base=S, stride=100000)` は `S..S+15` と `S+100000..S+100015` を返す。
seed-base の間隔 1000 に対し帯幅は 16 なので、6シャードの seed 集合は互いに素＝重複計算は起きない。

## 事前検証で判明した落とし穴（実行前に必ず対処）

1. **台帳が gitignore される。** `.gitignore:21` の `arena_*.jsonl` が `arena_m1.jsonl` に一致する。
   退避コミットを `git add -A` で作ると**何も staged されず commit が空振りし、push が一度も走らない**
   （`&&` 連鎖なので無言で落ちる）。巻き戻り復帰が効かなくなるため `git add -f arena_m1.jsonl` を使う。
2. **shallow clone には `origin/<branch>` が無い。** `git checkout -B <br> origin/<br>` /
   `git show origin/<br>:file` は `not a commit` で失敗する。`git fetch origin <br>` 後に `FETCH_HEAD` を使う。
3. **numpy が未導入のことがある。** `python3 -c "import numpy"` を確認し、無ければ `python3 -m pip install numpy`。
4. **リモートブランチの削除は proxy に 403 で弾かれる。** 検証用ブランチを作ったら消せない前提で名前を選ぶ。

## 実測コスト（4コアコンテナ・1ペアのスモーク）

1ペア ≈ 300s（single-thread）。`--workers 4` で 8ペア/サイクル ≈ 10分、32ペアで 40〜50分。

## 実行スクリプト（`/home/user/run_arena.sh`・K と COND のみ差し替え）

```bash
#!/bin/bash
K=1
COND=random
SEED=$((780000 + K*1000))
BR=claude/arena-m1-shard$K
OUT=/home/user/arena_m1.jsonl
cd /home/user/opcg-sim-backend
export PYTHONPATH=tests:tests/harness:tests/scripts OPCG_LOG_SILENT=1
# 巻き戻り復帰: 自分のブランチに退避済み台帳があれば先に回収（seed単位で再開される）
git fetch -q origin $BR 2>/dev/null && git show FETCH_HEAD:arena_m1.jsonl > $OUT 2>/dev/null
CAND=opcg_sim/data/learned/gen15_value.npz,opcg_sim/data/learned/gen15_policy.npz
for i in $(seq 1 20); do
  python3 tests/scripts/arena_resume.py --candidate $CAND --cand-macro \
    --leaders $COND --decks synth --pairs 32 --bands 2 --max-pairs 8 --workers 4 \
    --seed-base $SEED --out $OUT > /home/user/arena_cycle.log 2>&1
  tail -2 /home/user/arena_cycle.log
  cd /home/user/opcg-sim-backend
  git worktree remove /tmp/ar_wt --force 2>/dev/null
  git branch -D $BR 2>/dev/null
  git worktree add -q -B $BR /tmp/ar_wt HEAD 2>/dev/null && {
    cp $OUT /tmp/ar_wt/arena_m1.jsonl
    ( cd /tmp/ar_wt && git add -f arena_m1.jsonl && git commit -q -m "arena m1 shard$K: checkpoint" 2>/dev/null \
      && git push -qf origin $BR )
    cd /home/user/opcg-sim-backend
  }
  grep -q "ARENA_RESUME_FINAL" /home/user/arena_cycle.log && break
done
echo ARENA_SHARD_DONE
```

## 巻き戻り復帰

台帳 jsonl は seed が鍵なので、何度再起動しても消化済みペアはスキップされる。
コンテナが巻き戻ったら「セットアップ → 同じスクリプトを再起動」だけで続きから進む（seed 範囲の変更は不要）。
`ARENA_RESUME_FINAL` が出たら完走。`void`（対局不成立）は消化済みとして数えるが勝率の母数からは外れ、
`final_result` の `void` フィールドに件数が載る。

## 回収と判定

依頼元セッションが 6 ブランチの `arena_m1.jsonl` を回収し、random 3 シャード（96ペア）と
fixed 3 シャード（96ペア）をそれぞれ統合して `arena_parallel._pair_level_ci` でペア水準 95%CI を出す。
判定規約は `arena_gate` と同一（`wr>=0.55` かつ CI 下限 `>0.50` で promoted）。

## 実行結果（2026-08-24・全6シャード完走）

判定単位は条件別（random 96ペア / fixed 96ペア）。候補席のみ `--cand-macro`（macro_moves + box_battle
+ battle_readout + quiesce）、基準席は出荷既定。デッキ `synth`、ペア内で席とリーダーを入替（CRN）。

```
random (shard1-3)  pairs= 95/96 games=190 void=1 wins= 95.0 wr=0.5000 ci95=[0.4252,0.5748] elo=  -0.0 promoted=False
fixed  (shard4-6)  pairs= 96/96 games=192 void=0 wins= 98.0 wr=0.5104 ci95=[0.4489,0.5720] elo=   7.2 promoted=False
all    (shard1-6)  pairs=191/192 games=382 void=1 wins=193.0 wr=0.5052 ci95=[0.4570,0.5535] elo=   3.6 promoted=False
```

シャード別（n=32 は振れが大きく、単独では判断材料にならない）:

| シャード | 条件 | pairs | void | wr | ci95 | elo |
|---|---|---|---|---|---|---|
| k=1 | random | 31/32 | 1 | 0.4839 | [0.3515, 0.6162] | -11.2 |
| k=2 | random | 32/32 | 0 | 0.5938 | [0.4659, 0.7216] | +65.9 |
| k=3 | random | 32/32 | 0 | 0.4219 | [0.2966, 0.5472] | -54.7 |
| k=4 | fixed  | 32/32 | 0 | 0.5000 | [0.4016, 0.5984] | -0.0 |
| k=5 | fixed  | 32/32 | 0 | 0.5781 | [0.4694, 0.6869] | +54.7 |
| k=6 | fixed  | 32/32 | 0 | 0.4531 | [0.3422, 0.5641] | -32.7 |

**結論: 両条件とも promoted=False。マクロ手化 P1（配分箱）に勝率上の効果は検出されなかった。**
両条件の CI が 0.50 をまたぎ、点推定も 0.500 / 0.510 と五分。96ペアでの検出限界は
CI 幅から片側およそ ±0.06（≒ ±43 Elo）なので、「効果ゼロ」ではなく「この規模では
±43 Elo より小さい差しか無い」が正しい読み。P0 の計器が示した読みの浪費（細部窓 42.3%・
ドン順序重複 中央値 5.3x）は、配分箱の導入だけでは勝率に転換していない。

void 1件（shard1 / seed 881007 / OP07-019 vs OP09-001）は `PairTimeout: pair exceeded 900s`。
`--pair-timeout` の保険が働いた形で、手数上限では捕まらない戦闘箱の組合せ爆発の疑い。

### 運用上の記録: ワーカーの脱落と引き継ぎ

6ワーカーのうち 3本（shard2/4/5）が各 24/32 の時点で `API Error: 529 Overloaded` で
落ちて disconnected になった。チェックポイント退避が効いていたため、依頼元セッションが
残り 8ペア×3シャードを引き継いで消化・push し、計算のやり直しは発生しなかった。
shard3 は `git push` が権限で拒否され退避できない状態になったため、依頼元セッションで
並走させて完走させた（seed が鍵で決定論なので二重実行でも結果は同一）。

**退避が機能しているかを最初のサイクル直後に必ず検証すること**（`git ls-remote` の SHA が
base から変わっているか）。これを確認していなければ、`git add -A` の空振りに気づかないまま
数十分ぶんの計算を失っていた。

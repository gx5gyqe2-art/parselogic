# 純正Nループ 第1波・棋譜生成 ワーカー台帳

opcg-sim-backend の `claude/cpu-spec-improvements-yw91jd` にある
`tests/scripts/n_record_gen.py` を分担実行するワーカーセッションの一覧。

## 共通実行条件

```
OPCG_LOG_SILENT=1 PYTHONPATH=tests python tests/scripts/n_record_gen.py \
  --games 60 --seed-base {BASE} --workers 4 --sims 64 --shard-games 10 --out n1_records
```

- 1ワーカーあたり 60局、seed帯は `{BASE} = 300000 + N*1000`（重複なし）
- 成果物 push 先: `gx5gyqe2-art/opcg-sim-backend` の `claude/n1-w{NN}`
- ワーカーはコード変更・PR作成・他ブランチへの push・`make test` を行わない

## 起動状況

指示は w01〜w64 の 64ワーカーだったが、トークン消費の懸念により
**w32 で起動を打ち切り**（w33・w34 は起動要求が拒否、w35〜w64 は未起動）。
起動済みは 32ワーカー = 1,920局、seed帯 301000〜332000。

| ワーカー | seed-base | push先ブランチ | セッションID |
| --- | --- | --- | --- |
| w01 | 301000 | claude/n1-w01 | session_01ECHMrzVW2KVXiABt1ESiXi |
| w02 | 302000 | claude/n1-w02 | session_012T2SQwgSjuqFCsCLtde1Hg |
| w03 | 303000 | claude/n1-w03 | session_01145tuDptt5PymW42dFbY9V |
| w04 | 304000 | claude/n1-w04 | session_01A6hkjTmKqN6hM7EBYaspsU |
| w05 | 305000 | claude/n1-w05 | session_01Fy7T7QAw31PNpwWnXe2HqV |
| w06 | 306000 | claude/n1-w06 | session_01PETRipEpctxp6UyudLRAuw |
| w07 | 307000 | claude/n1-w07 | session_01PnDkcRYNt5bxwQ2Hp26L9k |
| w08 | 308000 | claude/n1-w08 | session_015ANZBjpgyKg9DVp2nRDej3 |
| w09 | 309000 | claude/n1-w09 | session_01K5RaxB7JhUWsEARUKiUMA2 |
| w10 | 310000 | claude/n1-w10 | session_01NsnLNsrpDCMVDP9VdLGnXd |
| w11 | 311000 | claude/n1-w11 | session_014gatTB7sdiEoNihvCKPCEq |
| w12 | 312000 | claude/n1-w12 | session_01WGik4H5YULBBWbh2TcDxsk |
| w13 | 313000 | claude/n1-w13 | session_016YFQsFLKXeWVwdoEx9fjPX |
| w14 | 314000 | claude/n1-w14 | session_01FN3W7ap7t1pnGc8MGRskDo |
| w15 | 315000 | claude/n1-w15 | session_01WQp3532PhhzRXy4BADgpUL |
| w16 | 316000 | claude/n1-w16 | session_013yy7E4xzFamWMy4WP1vsT1 |
| w17 | 317000 | claude/n1-w17 | session_01S4rmJtapWZJS1NwyjpzxAW |
| w18 | 318000 | claude/n1-w18 | session_01XV9SfoBg5R6vqLMnVDxzBm |
| w19 | 319000 | claude/n1-w19 | session_019hD9GLaH8a9wL97XM7cjpM |
| w20 | 320000 | claude/n1-w20 | session_01MEcrHsJQtPTJeXNg8kSauu |
| w21 | 321000 | claude/n1-w21 | session_014HgAs5PR17QuVtsS9Kvefo |
| w22 | 322000 | claude/n1-w22 | session_014wP6As7qPC3gX596LHg5t3 |
| w23 | 323000 | claude/n1-w23 | session_01D8p57nhEZazHhevQqnVdT9 |
| w24 | 324000 | claude/n1-w24 | session_01T9JNBSf5uQJxpnWo7nBbJT |
| w25 | 325000 | claude/n1-w25 | session_019VmsbqXzXR8oCFJBcTCUdK |
| w26 | 326000 | claude/n1-w26 | session_01GkVN9iaABc241LGwpcmkLQ |
| w27 | 327000 | claude/n1-w27 | session_0128WqLk9tSeyQREG1ZPDD44 |
| w28 | 328000 | claude/n1-w28 | session_01Fe3yYxXiEYvjmHhRWCA6GG |
| w29 | 329000 | claude/n1-w29 | session_01XRSm6QNqpKZrHqNTqiGErk |
| w30 | 330000 | claude/n1-w30 | session_01NSgDrBBXnzPJTk9zRd3ViP |
| w31 | 331000 | claude/n1-w31 | session_01AmgtiZCy3EP6HiUxvo22Kw |
| w32 | 332000 | claude/n1-w32 | session_01Y3HqU6JDZzHU3Fb2HzjLeK |

## 第1波の結果（2026-08-26 12:45 UTC 時点・全完了）

起動した 32ワーカーすべてが 60局を完走し、`claude/n1-w01`〜`w32` へ push 済み。

- 総局数: 1,920局
- 総行数: 279,188 行（うち main_rows 184,457 行）
- 棄却: 3 行（w13 / w18 / w19 が各1）
- ワーカーあたり行数: 最小 8,288 / 最大 9,505 / 平均 8,725

| ワーカー | rows | main_rows | dropped |
| --- | ---: | ---: | ---: |
| w01 | 8717 | 5671 | 0 |
| w02 | 8482 | 5620 | 0 |
| w03 | 8437 | 5656 | 0 |
| w04 | 8445 | 5550 | 0 |
| w05 | 9069 | 6052 | 0 |
| w06 | 8660 | 5710 | 0 |
| w07 | 8688 | 5724 | 0 |
| w08 | 8924 | 5864 | 0 |
| w09 | 9505 | 6148 | 0 |
| w10 | 8673 | 5757 | 0 |
| w11 | 8615 | 5625 | 0 |
| w12 | 8664 | 5773 | 0 |
| w13 | 8466 | 5636 | 1 |
| w14 | 8420 | 5611 | 0 |
| w15 | 9038 | 5958 | 0 |
| w16 | 8288 | 5502 | 0 |
| w17 | 8875 | 5813 | 0 |
| w18 | 9135 | 6011 | 1 |
| w19 | 8516 | 5597 | 1 |
| w20 | 8954 | 5876 | 0 |
| w21 | 8534 | 5687 | 0 |
| w22 | 8430 | 5592 | 0 |
| w23 | 8535 | 5577 | 0 |
| w24 | 9114 | 6086 | 0 |
| w25 | 8464 | 5665 | 0 |
| w26 | 8369 | 5625 | 0 |
| w27 | 8720 | 5789 | 0 |
| w28 | 8317 | 5479 | 0 |
| w29 | 9176 | 5954 | 0 |
| w30 | 9016 | 5998 | 0 |
| w31 | 8924 | 5893 | 0 |
| w32 | 9018 | 5958 | 0 |

再起動を要したワーカーは無し。

## 第2波（N2）の状況

seed帯 401000〜408000 の 8ワーカーによる第2波は**未起動**。
本セッションからの `create_session` / `create_trigger` が承認待ちで通らないため、
専用オーケストレータの起動を保留中。前提条件は確認済み:

- `claude/n1-results` に `n1_results/n1_net.npz`（約107KB）が実在
- seed帯 401000〜408000 は第1波（301000〜332000）と非重複

## 未起動分（再開する場合）

w33〜w64（seed帯 333000〜364000）。同じ規則で `{BASE} = 300000 + N*1000`
を割り当てれば、起動済み帯と重複しない。

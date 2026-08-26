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

## 未起動分（再開する場合）

w33〜w64（seed帯 333000〜364000）。同じ規則で `{BASE} = 300000 + N*1000`
を割り当てれば、起動済み帯と重複しない。

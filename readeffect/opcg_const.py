# ==========================================
# OPCG パターン定義ファイル (v25.0)
# ==========================================
# 形式: (正規表現パターン, 中間言語タグ)
# 追加時はリストの末尾でも構いません（ロジック側で自動的に文字数順にソートされます）

RAW_PATTERNS = [
    # --- 1. システム・超長文 (最優先) ---
    (r'相手の場のドン!!の枚数が自分の場のドン!!の枚数より多い場合', ' [CND_DON_OPP_GT] '),
    (r'自分の場のドン!!が相手の場のドン!!の枚数以下の?場合', ' [CND_DON_SELF_LE] '),
    (r'登場したターンに(キャラクター|キャラ)?へアタックできる', ' [STAT_CAN_ATK_TURN] '),
    (r'ルール上、このカードはカード名を「.*?」としても扱う', ' [STAT_ALIAS] '),
    (r'ルール上、このカードはデッキに何枚でも入れることができる', ' [RULE_UNLIMITED_DECK] '),
    (r'ルール上、', ' [RULE_GENERIC] '), 
    (r'。そうした場合、', ' [SEP_CHAIN] '),
    (r'そうしなかった場合、', ' [CND_IF_NOT_DONE] '), # 追加
    (r'そうしなかった場合', ' [CND_IF_NOT_DONE] '), # 追加
    (r'指定の数', ' [VAL_SPECIFIED] '),
    (r'公開したカード', ' [OBJ_REVEALED] '),
    (r'このバトル中', ' [DUR_BATTLE] '),
    (r'このターン中', ' [DUR_TURN] '),
    (r'そのターン中', ' [DUR_TURN] '),
    (r'次の相手のターン終了時まで', ' [DUR_NEXT_OPP_TURN_END] '),
    (r'次の自分のターン開始時まで', ' [DUR_NEXT_SELF_TURN_START] '),
    (r'次の自分のターン終了時まで', ' [DUR_NEXT_SELF_TURN_END] '),
    (r'次の相手のリフレッシュフェイズで', ' [DUR_NEXT_OPP_REFRESH] '),
    (r'次の相手のエンドフェイズ終了時まで', ' [DUR_NEXT_OPP_END_PHASE] '),
    
    # --- 2. 補足説明 ---
    (r'\(相手のアタックの後、このカードをレストにし、アタックの対象をこのカードにできる\)', ' [DESC_BLOCKER] '),
    (r'\(このカードがダメージを与えた場合、トリガーは発動せずそのカードはトラッシュに置かれる\)', ' [DESC_BANISH] '),
    (r'\(このカードが与えるダメージは2になる\)', ' [DESC_DBL_ATK] '),
    (r'\(このカードは登場したターンにアタックできる\)', ' [DESC_RUSH] '),
    (r'\(このカードはブロックされない\)', ' [DESC_UNBLOCKABLE] '),
    (r'\(このカードは登場したターンにキャラへアタックできる\)', ' [DESC_RUSH_CHR] '),
    (r'\(コストエリアのドン!!を、指定の数レストにできる\)', ' [DESC_DON_COST] '),

    # --- 3. キーワード能力 ---
    (r'【ブロッカー】', ' [KWD_BLOCKER] '),
    (r'【速攻】', ' [KWD_RUSH] '),
    (r'【速攻:キャラ】', ' [KWD_RUSH_CHR] '),
    (r'【バニッシュ】', ' [KWD_BANISH] '),
    (r'【ダブルアタック】', ' [KWD_DOUBLE_ATTACK] '),
    (r'【トリガー】', ' [KWD_TRIGGER] '),
    (r'【ブロック不可】', ' [KWD_UNBLOCKABLE] '),
    (r'【突進】', ' [KWD_CHARGE] '), 

    # --- 4. タイミング・条件ブロック ---
    (r'【KO時】', ' [TRG_ON_KO] '), 
    (r'【自分のターン終了時】', ' [TRG_TURN_END_SELF] '),
    (r'【相手のターン終了時】', ' [TRG_TURN_END_OPP] '),
    (r'【ターン終了時】', ' [TRG_TURN_END] '),
    (r'【登場時】', ' [TRG_SUMMON] '),
    (r'【アタック時】', ' [TRG_ATK] '),
    (r'【相手のアタック時】', ' [TRG_OPP_ATK] '),
    (r'【ブロック時】', ' [TRG_BLOCK] '),
    (r'【起動メイン】', ' [ACT_MAIN] '),
    (r'【メイン】', ' [ACT_MAIN] '),
    (r'【カウンター】', ' [ACT_COUNTER] '),
    (r'【ドン!!-?(\d+)】', ' [COST_DON_MINUS] '),
    (r'【ドン!![×xX](\d+)】', ' [CND_DON_EQUIP] '),
    (r'【ターン(\d+)回】', ' [LMT_TURN_X] '),
    (r'【相手のターン中】', ' [CND_OPP_TURN] '),
    (r'【自分のターン中】', ' [CND_SELF_TURN] '),
    
    # --- 5. 数値・比較条件・状態 ---
    (r'KOされる場合、代わりに', ' [CND_REPLACE_KO] '),
    (r'場を離れる場合、代わりに', ' [CND_REPLACE_LEAVE] '),
    (r'効果でKOされない', ' [STAT_NO_KO_BY_EFFECT] '),
    (r'バトルでKOされない', ' [STAT_NO_KO_BY_BATTLE] '),
    (r'KOされず', ' [STAT_NO_KO_AND] '),
    (r'KOされた時', ' [TRG_WHEN_KO] '),
    (r'KOされる場合', ' [CND_IF_KO] '),
    (r'KOする', ' [ACT_KO] '), 
    (r'KOしてもよい', ' [ACT_KO_OPT] '),

    (r'が\d+枚以下の?場合', ' [CND_COUNT_LE] '),
    (r'が\d+枚以上の?場合', ' [CND_COUNT_GE] '),
    (r'コスト\d+以下の?', ' [FIL_COST_LE] '),
    (r'コスト\d+以上の?', ' [FIL_COST_GE] '),
    (r'コスト\d+の', ' [FIL_COST_EQ] '),
    (r'コスト\d+から\d+の', ' [FIL_COST_RANGE] '),
    (r'コスト\d+', ' [FIL_COST_VAL] '), 
    (r'パワー\d+以下の?', ' [FIL_POW_LE] '),
    (r'パワー\d+以上の?', ' [FIL_POW_GE] '),
    (r'パワー[+-]\d+', ' [ACT_BUFF_POW] '),
    (r'カウンター[+-]\d+', ' [ACT_BUFF_COUNTER] '),
    (r'コスト[+-]\d+', ' [ACT_BUFF_COST] '),
    (r'枚になるように', ' [VAL_BECOME] '), 
    (r'なるように', ' [VAL_BECOME_GENERIC] '), 
    (r'同じ枚数', ' [VAL_SAME_AMOUNT] '),
    (r'同じパワー', ' [VAL_SAME_POWER] '),
    (r'好きな枚数', ' [VAL_ANY_AMOUNT] '),
    (r'任意の', ' [VAL_ANY] '), 

    (r'多色', ' [CND_MULTI_COLOR] '),
    (r'だった場合', ' [CND_WAS] '),
    (r'ある場合', ' [CND_EXISTS] '),
    (r'ない場合', ' [CND_NOT_EXISTS] '),
    (r'以外の?', ' [CND_EXCEPT] '), 
    (r'の場合', ' [CND_IF] '),
    (r'場合', ' [CND_IF_GENERIC] '),
    (r'なら', ' [CND_IF_S] '), 
    (r'のみ', ' [CND_ONLY] '), 
    (r'いない', ' [CND_NOT_EXIST] '),
    (r'い', ' [CND_EXIST_SHORT] '), 
    (r'より少ない', ' [CND_LESS_THAN] '), 
    (r'合計', ' [VAL_TOTAL] '), 
    (r'数分', ' [VAL_AMOUNT] '), 
    (r'数', ' [VAL_COUNT] '), 
    
    # --- 6. 固有名詞・特徴・属性 ---
    (r'特徴《.*?》', ' [OBJ_TRAIT] '),
    (r'《.*?》', ' [OBJ_TRAIT_VAL] '), 
    (r'属性\s?\(.*?\)', ' [OBJ_ATTR] '),
    (r'「.*?」', ' [OBJ_NAME] '),
    (r'『.*?』', ' [OBJ_NAME_PARTIAL] '),
    (r'特徴', ' [OBJ_TRAIT_GENERIC] '),

    # --- 7. 色・エリア・用語 ---
    (r'コストエリア', ' [LOC_COST_AREA] '),
    (r'赤', ' [COLOR_RED] '),
    (r'緑', ' [COLOR_GREEN] '),
    (r'青', ' [COLOR_BLUE] '),
    (r'紫', ' [COLOR_PURPLE] '),
    (r'黒', ' [COLOR_BLACK] '),
    (r'黄', ' [COLOR_YELLOW] '),
    
    # --- 8. 指示代名詞・用語・カード種類 ---
    (r'このカード', ' [REF_THIS_CARD] '),
    (r'このキャラ(クター)?', ' [REF_THIS_CHR] '),
    (r'このリーダー', ' [REF_THIS_LDR] '),
    (r'この', ' [REF_THIS] '),
    (r'そのカード', ' [REF_THAT_CARD] '),
    (r'そのキャラ(クター)?', ' [REF_THAT_CHR] '),
    (r'その', ' [REF_THAT] '),
    
    (r'イベント', ' [TYPE_EVENT] '),
    (r'ステージ', ' [TYPE_STAGE] '),
    (r'キャラカード', ' [OBJ_CHR_CARD] '),
    (r'リーダーカード', ' [OBJ_LDR_CARD] '),
    (r'カード', ' [OBJ_CARD] '),
    (r'すべて', ' [SEL_ALL] '),
    (r'アクティブ', ' [STAT_ACTIVE] '),
    (r'レスト', ' [STAT_REST] '),
    (r'自身', ' [REF_ITSELF] '),
    (r'元々の?', ' [MOD_BASE] '),
    (r'効果のない', ' [FIL_NO_EFFECT] '),
    (r'効果を持たない', ' [FIL_NO_EFFECT] '),
    (r'にある', ' [LOC_IN] '),
    (r'残り', ' [OBJ_REMAINDER] '),
    (r'場', ' [LOC_FIELD] '),
    (r'一番上', ' [LOC_TOPMOST] '), 
    (r'上', ' [LOC_TOP] '), 
    (r'下', ' [LOC_BOTTOM] '), 
    (r'効果', ' [NOUN_EFFECT] '), 
    (r'パワー', ' [NOUN_POWER] '), 
    (r'バトル', ' [NOUN_BATTLE] '), 
    (r'コスト', ' [NOUN_COST] '), # 追加
    (r'何', ' [QT_ANY] '), 
    (r'以上', ' [CMP_GE] '), 
    (r'以下', ' [CMP_LE] '), 
    (r'アタックによって', ' [CND_BY_ATTACK] '), 
    (r'アタック', ' [NOUN_ATTACK] '), 
    (r'ダメージを与えた時', ' [TRG_DEAL_DAMAGE] '), 
    (r'ダメージ', ' [NOUN_DAMAGE] '), 
    
    (r'終了時', ' [TRG_END_PHASE] '), 
    (r'開始時', ' [TRG_START_PHASE] '), 
    (r'ターン開始時', ' [TRG_TURN_START] '), 
    (r'いる', ' [CND_EXIST] '), 
    (r'お互い', ' [REF_BOTH] '), 
    (r'ドローフェイズ', ' [PHASE_DRAW] '), 
    (r'うち', ' [SEL_AMONG] '), 

    # --- 9. アクション・動詞句 (活用形網羅) ---
    (r'公開することで', ' [COST_REVEAL] '), 
    (r'公開す', ' [ACT_REVEAL_PRE] '), 
    (r'持ち', ' [CND_HAS_SEQ] '), 
    (r'なければ', ' [CND_UNLESS] '), 
    (r'アタックすることができない', ' [STAT_CANNOT_ATTACK_FULL] '), 
    (r'場を離れた時', ' [TRG_LEAVE_FIELD] '), 
    (r'場を離れ', ' [CND_LEAVE_FIELD] '), 
    (r'されない', ' [STAT_NO_PASSIVE] '), 
    (r'裏向きにする', ' [ACT_TURN_FACEDOWN] '), 
    (r'裏向き', ' [STAT_FACEDOWN] '), 
    (r'表向き', ' [STAT_FACEUP] '), 
    (r'与えてもよい', ' [ACT_DEAL_DAMAGE_OPT] '), 
    (r'によって', ' [CND_BY] '), 
    (r'戻す', ' [ACT_RETURN] '), 
    (r'しか', ' [CND_ONLY_S2] '), 
    (r'ず', ' [CND_NOT] '), 
    (r'なった', ' [ACT_BECAME] '), # 追加
    (r'なっ', ' [ACT_BECAME_SEQ] '), # 追加
    (r'なる', ' [ACT_BECOME] '), 
    
    (r'ることができる', ' [STAT_POSSIBLE_CAN] '), 
    
    # 戻す
    (r'持ち主の手札に戻すことができる', ' [ACT_BOUNCE_OWNER_OPT] '),
    (r'持ち主の手札に戻す', ' [ACT_BOUNCE_OWNER] '),
    (r'持ち主の手札に戻し', ' [ACT_BOUNCE_OWNER_SEQ] '),
    (r'手札に戻すことができる', ' [ACT_BOUNCE_OPT] '),
    (r'手札に戻す', ' [ACT_BOUNCE] '),
    (r'手札に戻し', ' [ACT_BOUNCE_SEQ] '),
    (r'デッキの下に戻すことができる', ' [ACT_DECK_BTM_RETURN_OPT] '),
    (r'デッキの下に戻す', ' [ACT_DECK_BTM_RETURN] '),
    (r'デッキに戻し', ' [ACT_DECK_RETURN_SEQ] '),
    (r'戻った時', ' [TRG_RETURNED] '),
    (r'戻された時', ' [TRG_RETURNED_PASSIVE] '),

    # 加える
    (r'手札に加えることができる', ' [ACT_SEARCH_OPT] '),
    (r'手札に加える', ' [ACT_SEARCH] '),
    (r'手札に加え', ' [ACT_SEARCH_SEQ] '),
    (r'ライフの上に加える', ' [ACT_LIFE_ADD_TOP] '),
    (r'ライフの上に表向きで加える', ' [ACT_LIFE_ADD_TOP_FACEUP] '),
    (r'ライフの上に裏向きで加える', ' [ACT_LIFE_ADD_TOP_FACEDOWN] '),
    (r'ライフの上か下に表向きで加える', ' [ACT_LIFE_ADD_TOPBTM_FACEUP] '),
    (r'ライフの上か下に裏向きで加える', ' [ACT_LIFE_ADD_TOPBTM_FACEDOWN] '),
    (r'加える', ' [ACT_ADD_GENERIC] '),
    (r'加え', ' [ACT_ADD_SEQ] '), # 追加

    # 置く
    (r'デッキの下に置くことができる', ' [ACT_DECK_BTM_OPT] '),
    (r'デッキの下に置く', ' [ACT_DECK_BTM] '),
    (r'デッキの下に置き', ' [ACT_DECK_BTM_SEQ] '),
    (r'デッキの上か下に置く', ' [ACT_DECK_TOPBTM] '),
    (r'デッキの上か下に置き', ' [ACT_DECK_TOPBTM_SEQ] '),
    (r'デッキの上に置く', ' [ACT_DECK_TOP] '),
    (r'デッキの上に置き', ' [ACT_DECK_TOP_SEQ] '),
    (r'好きな順番でデッキの下に置く', ' [ACT_REORDER_BTM] '),
    (r'好きな順番でデッキの下に置き', ' [ACT_REORDER_BTM_SEQ] '),
    (r'トラッシュに置くことができる', ' [ACT_TRASH_PUT_OPT] '),
    (r'トラッシュに置く', ' [ACT_TRASH_PUT] '),
    (r'トラッシュに置き', ' [ACT_TRASH_PUT_SEQ] '),
    (r'ライフの上か下に置く', ' [ACT_LIFE_TOPBTM_PUT] '),
    (r'置いてもよい', ' [ACT_PUT_OPT] '), 
    (r'置く', ' [ACT_PUT] '),
    (r'置き', ' [ACT_PUT_SEQ] '),
    (r'置い', ' [ACT_PUT_SEQ_TE] '), 

    # 登場・追加
    (r'アクティブで追加する', ' [ACT_ADD_ACTIVE] '),
    (r'レストで追加する', ' [ACT_ADD_REST] '),
    (r'レストで登場させる', ' [ACT_SUMMON_REST] '),
    (r'登場させる', ' [ACT_SUMMON] '),
    (r'登場し', ' [ACT_SUMMON_SEQ_TE] '), 
    (r'登場させ', ' [ACT_SUMMON_SEQ] '),
    (r'登場したターンの場合', ' [CND_SUMMONED_TURN] '),
    (r'登場できない', ' [STAT_CANNOT_SUMMON] '),
    (r'追加する', ' [ACT_ADD_DON] '),

    # その他基本動作
    (r'勝利する', ' [ACT_WIN] '), 
    (r'敗北する', ' [ACT_LOSE] '), 
    (r'発動した時', ' [TRG_ACTIVATED] '), 
    (r'発動できる', ' [ACT_CAN_ACTIVATE] '),
    (r'発動する', ' [ACT_ACTIVATE] '),
    (r'発動できない', ' [STAT_CANNOT_ACTIVATE] '),
    
    (r'引いてい', ' [ACT_DRAW_PROG] '), 
    (r'引いた時', ' [TRG_DRAWN] '), 
    (r'引く', ' [ACT_DRAW] '),
    (r'引き', ' [ACT_DRAW_SEQ] '),
    
    (r'捨てる', ' [ACT_DISCARD] '),
    (r'捨て', ' [ACT_DISCARD_SEQ] '),
    
    (r'見て', ' [ACT_LOOK] '),
    (r'見る', ' [ACT_LOOK_END] '),
    
    (r'選んだ', ' [CND_SELECTED] '), 
    (r'選ぶ', ' [ACT_SELECT] '),
    (r'選び', ' [ACT_SELECT_SEQ] '),
    
    (r'レストにする', ' [ACT_REST_DO] '),
    (r'レストにできる', ' [ACT_REST_OPT] '),
    (r'レストにし', ' [ACT_REST_SEQ] '),
    (r'レストになった時', ' [TRG_BECAME_REST] '),
    (r'レストにできない', ' [STAT_CANNOT_REST] '),
    (r'レストされない', ' [STAT_NO_REST] '),
    
    (r'アクティブにする', ' [ACT_ACTIVE_DO] '),
    (r'アクティブにならない', ' [STAT_NO_ACTIVE_PHASE] '),
    
    (r'入れ替える', ' [ACT_SWAP] '),
    (r'無効にする', ' [ACT_NEGATE] '),
    (r'無効になる', ' [STAT_INVALID] '),
    (r'シャッフルする', ' [ACT_SHUFFLE] '), 
    
    (r'公開し', ' [ACT_REVEAL_SEQ] '),
    (r'公開する', ' [ACT_REVEAL] '),
    
    (r'好きな順番', ' [ACT_REORDER_SEQ] '),
    (r'並び替え', ' [ACT_REORDER] '),
    (r'並び変え', ' [ACT_REORDER] '), 
    
    (r'ことができる', ' [STAT_POSSIBLE_CAN] '),
    (r'ことができ', ' [STAT_POSSIBLE_CAN_SEQ] '),
    (r'こと', ' [NOUN_THING] '),
    (r'ができる', ' [STAT_POSSIBLE] '),
    (r'できる', ' [STAT_POSSIBLE] '),
    (r'てもよい', ' [STAT_OPTIONAL] '), 
    
    (r'アタックできない', ' [STAT_CANNOT_ATTACK] '),
    (r'アタックできる', ' [STAT_CAN_ATTACK] '),
    (r'アタックした時', ' [TRG_ATTACKED] '),
    (r'アタックする際', ' [CND_ATTACKING] '),
    
    (r'得て', ' [ACT_GAIN_SEQ] '),
    (r'得る', ' [ACT_GAIN] '),
    (r'付与する', ' [ACT_ATTACH] '),
    (r'受ける', ' [ACT_TAKE_DAMAGE] '),
    (r'受け', ' [ACT_TAKE_DAMAGE_SEQ] '), 
    (r'与えた時', ' [TRG_DEALT] '), 
    (r'与え', ' [ACT_DEAL_SEQ] '), 
    (r'も入れる事', ' [ACT_INCLUDE_THING] '), 
    (r'入れる', ' [ACT_INCLUDE] '), 
    (r'事', ' [NOUN_THING] '), 
    (r'し、', ' [SEP_AND_DO] '), 
    (r'た時', ' [TRG_GENERIC] '), 
    (r'られ', ' [PASSIVE_SEQ] '), 

    # --- 10. ライフ関連 ---
    (r'ライフの上か下に', ' [LOC_LIFE_TOPBTM] '),
    (r'ライフの上から', ' [LOC_LIFE_TOP] '),
    (r'ライフの下に', ' [LOC_LIFE_BTM] '),
    (r'ライフ', ' [LOC_LIFE] '),

    # --- 11. ターゲット・対象の組み合わせ ---
    (r'リーダーか', ' [TGT_LDR_OR] '),
    (r'リーダーが', ' [TGT_LDR_SUB] '),
    (r'キャラ(クター)?', ' [TGT_CHR] '),
    (r'リーダー', ' [TGT_LDR] '),
    (r'ドン!!デッキ', ' [LOC_DON_DECK] '),
    (r'ドン!!', ' [OBJ_DON] '),
    (r'ドン !!', ' [OBJ_DON] '), 

    # --- 12. 場所・人称 ---
    (r'トラッシュ', ' [LOC_TRASH] '),
    (r'手札', ' [LOC_HAND] '),
    (r'デッキ', ' [LOC_DECK] '),
    (r'自分', ' [REF_SELF] '),
    (r'相手', ' [REF_OPP] '),
    (r'持ち主', ' [REF_OWNER] '),
    
    # --- 13. 助詞・接続詞・記号 ---
    (r'かつ', ' [SEP_AND_ALSO] '), 
    (r'枚までを', ' [P_OBJ_UPTO] '),
    (r'までを', ' [P_UPTO_OBJ] '),
    (r'枚まで', ' [P_UPTO] '),
    (r'まで', ' [P_LIMIT] '),
    (r'枚を', ' [P_OBJ_FIX] '),
    (r'枚につき', ' [P_PER] '),
    (r'ずつ', ' [P_EACH] '),
    (r'枚', ' [CTR_CARD] '),
    (r'つ', ' [CTR_GENERIC] '),
    (r'を持つ', ' [P_HAS] '),
    (r'持たない', ' [P_NOT_HAS] '), 
    (r'を含む', ' [P_CONTAINS] '),
    (r'に、', ' [P_DAT_SEP] '),
    (r'に', ' [P_DAT] '),
    (r'を、', ' [P_OBJ_SEP] '),
    (r'を', ' [P_OBJ] '),
    (r'が', ' [P_SUB] '),
    (r'は、', ' [P_TOP_SEP] '),
    (r'は', ' [P_TOP] '),
    (r'の', ' [P_POS] '),
    (r'で', ' [P_BY] '),
    (r'と', ' [P_WITH] '),
    (r'か', ' [P_OR] '),
    (r'から', ' [P_FROM] '),
    (r'へ', ' [P_TO] '),
    (r'も', ' [P_ALSO] '), 
    (r'または', ' [SEP_OR] '),
    (r'その後', ' [SEP_NEXT] '),
    (r'代わりに', ' [SEP_REPLACE] '),
    (r'。', ' [SEP_END] '),
    (r'、', ' [SEP_AND] '),
    (r'/', ' [SEP_SLASH] '),
    (r'/', ' [SEP_SLASH] '),
    (r':', ' [SEP_COLON] '), 
    (r'・', ' [SEP_BULLET] '), 
    (r'~', ' [SEP_RANGE] '), 
    
    # --- 14. 記号 ---
    (r'\(', ' [BRKT_OPEN] '),
    (r'\)', ' [BRKT_CLOSE] '),
    (r'「', ' [QT_OPEN] '),
    (r'」', ' [QT_CLOSE] '),
        # --- 追加: 登場・移動関連のアクション(活用形・受動態) ---
    (r'登場させることができる', ' [ACT_SUMMON_CAUS_OPT] '),
    (r'登場させる', ' [ACT_SUMMON_CAUS] '),
    (r'登場させた時', ' [TRG_SUMMONED_CAUS] '),
    (r'登場させた', ' [ACT_SUMMONED_CAUS] '),
    (r'登場できる', ' [STAT_CAN_SUMMON] '),
    (r'登場する', ' [ACT_SUMMON_DO] '),
    (r'登場し', ' [ACT_SUMMON_SEQ] '),
    (r'デッキに戻した', ' [ACT_DECK_RETURNED] '),
    (r'戻した', ' [ACT_RETURNED] '),
    (r'捨てた', ' [ACT_DISCARDED] '),
    (r'加わった時', ' [TRG_JOINED] '),
    (r'加わった', ' [ACT_JOINED] '),
    (r'加わる', ' [ACT_JOIN_DO] '),
    (r'置かれる', ' [ACT_PUT_PASSIVE] '),
    (r'入れ替えた', ' [ACT_SWAPPED] '),
    (r'入れ替える', ' [ACT_SWAP] '),
    
    # --- 追加: バトル・アタック関連のアクション ---
    (r'アタックすることができる', ' [STAT_CAN_ATTACK_FULL] '),
    (r'アタックする', ' [ACT_ATTACK_DO] '),
    (r'アタックした', ' [ACT_ATTACKED] '),
    (r'バトルした', ' [ACT_BATTLED] '),
    (r'バトルを行う', ' [ACT_BATTLE_DO] '),
    
    # --- 追加: 状態・条件・否定 ---
    (r'自分の手札が', ' [CND_SELF_HAND_SUB] '),
    (r'引くことができない', ' [STAT_CANNOT_DRAW] '),
    (r'場を離れない', ' [STAT_NO_LEAVE] '),
    (r'付与されている', ' [CND_ATTACHED] '),
    (r'異なる色', ' [CND_DIFF_COLOR] '),
    (r'KOされる', ' [CND_KO_PASSIVE] '),
    (r'せず', ' [CND_NOT_DO_SEQ] '), # 「発動せず」などの否定接続
    
    # --- 追加: 具体的語彙・文脈語 ---
    (r'枚引く', ' [ACT_DRAW_QTY] '),
    (r'離れ', ' [CND_LEAVE_SEQ] '), # 「場を離れ、~」の移動条件
    (r'支払う', ' [ACT_PAY] '),
    (r'少なく', ' [VAL_LESS] '),
    (r'与える', ' [ACT_DEAL] '),
    (r'他の', ' [REF_OTHER] '),
    (r'手札から', ' [P_FROM_HAND] '),
    (r'リフレッシュフェイズ', ' [PHASE_REFRESH] '),
    (r'裏向きにできる', ' [ACT_FACEDOWN_OPT] '),
    
    # --- 追加: 構造・キーワード ---
    (r'【', ' [BRKT_KWD_OPEN] '), # キーワード能力の開始記号
    (r'】', ' [BRKT_KWD_CLOSE] '), # キーワード能力の終了記号
    (r'速攻', ' [KWD_RUSH_TEXT] '), # テキスト内で言及されるキーワード名
        # --- 15. 残存日本語・文法補完 (カバレッジ100%用) ---
    # 文脈のあるフレーズ (優先度高)
    (r'このターン終了時', ' [TRG_THIS_TURN_END] '),
    (r'なった時', ' [TRG_BECAME] '),
    (r'バトルしている', ' [CND_BATTLING] '),
    (r'加えられない', ' [STAT_CANNOT_ADD] '),
    (r'ルール上', ' [RULE_GENERIC] '), # 念のため再定義
    
    # 否定形・進行形・接続
    (r'できない', ' [STAT_CANNOT] '),
    (r'できない', ' [STAT_CANNOT] '),
    (r'している', ' [STAT_PROG] '),
    (r'して', ' [ACT_DO_SEQ] '),
    (r'次に、?', ' [ADV_NEXTly] '),
    (r'次', ' [NOUN_NEXT] '),
    (r'それぞれ', ' [ADV_EACH] '),
    
    # 動詞・アクション
    (r'支払う', ' [ACT_PAY] '),
    (r'少なくなる', ' [ACT_DECREASE] '),
    (r'追加し', ' [ACT_ADD_SEQ] '),
    (r'入れ替える', ' [ACT_SWAP] '),
    
    # 名詞・コスト表記
    (r'ターン', ' [NOUN_TURN] '),
    (r'カウンター', ' [NOUN_COUNTER] '), # カウンター+1000等に影響しないよう末尾推奨
    (r'リフレッシュフェイズ', ' [PHASE_REFRESH] '),
    (r'ドン!!-?(\d+)', ' [COST_DON_MINUS_ACT] '), # 括弧なしのコスト表記対応
    
    # 最終的な掃除 (優先度低)
    (r'時', ' [TRG_WHEN] '), # 孤立した「時」
    (r'元々', ' [MOD_BASE_RAW] '),
    (r'回復する', ' [ACT_RECOVER] '),
        # --- 16. 完結編:補助動詞結合・受動態・残りカス掃除 ---
    
    # 「~する」+「ことができる」の結合問題解消 (最重要: 「す」が消えます)
    (r'することができる', ' [STAT_CAN_DO] '),
    (r'することができない', ' [STAT_CANNOT_DO] '),
    (r'ことができない', ' [STAT_CANNOT_FULL] '),
    
    # 受動態・~される (エース、ガープ等)
    (r'付与された', ' [TRG_ATTACHED] '),
    (r'付与され', ' [CND_ATTACHED_SEQ] '),
    (r'アタックされた', ' [TRG_ATTACKED_PASSIVE] '),
    (r'された', ' [PASSIVE_PAST] '),
    (r'され', ' [PASSIVE_SEQ] '),
    
    # 状態変化・設定 (アイン等)
    (r'にする', ' [ACT_SET_TO] '), # 「パワーを0にする」対応
    
    # 特定用語・アクション
    (r'プレイ', ' [ACT_PLAY] '), # シャンクス等 (「登場」と区別される用語)
    (r'メインフェイズ', ' [PHASE_MAIN] '), # 黄ルフィ等
    (r'ゲーム', ' [NOUN_GAME] '), # ロジャー (特殊勝利)
    
    # 期間の微調整
    (r'ターン中', ' [DUR_TURN_GENERIC] '), # 「登場したターン中」等
    
    # その他マイナーな残り
    (r'中', ' [DUR_DURING] '),
    (r'際', ' [TRG_WHEN_DOING] '),
        # --- 17. 最終仕上げ:複合動詞・過去形結合 ---
    (r'公開することができる', ' [ACT_REVEAL_OPT] '),
    (r'登場した', ' [ACT_SUMMONED] '),
    (r'レストにした', ' [ACT_RESTED] '),
    
    # 念のための補強
    (r'公開する', ' [ACT_REVEAL_DO] '), 
    (r'入れ替えた', ' [ACT_SWAPPED] '),
        # --- 18. ラストスパート:未定義の活用形・接続語・名詞 ---
    
    # 付与のバリエーション (最重要)
    (r'付与することができる', ' [ACT_ATTACH_OPT] '),
    (r'付与される', ' [ACT_ATTACH_PASSIVE] '), # ロジャー等の「付与され+る」対策
    (r'付与されている', ' [CND_ATTACHED_PROG] '),
    (r'付与した', ' [ACT_ATTACHED] '),
    (r'付与し', ' [ACT_ATTACH_SEQ] '),
    
    # 過去形・完了形
    (r'KOした', ' [ACT_KOED] '),
    (r'置いた', ' [ACT_PUT_PAST] '),
    
    # アクション・能動態
    (r'シャッフルできる', ' [ACT_SHUFFLE_CAN] '),
    (r'無効にし', ' [ACT_NEGATE_SEQ] '),
    (r'飛ばされる', ' [ACT_SKIPPED] '), # ロジャー「ドローフェイズは飛ばされる」
    
    # 接続・比較・数量
    (r'さらに', ' [SEP_FURTHERMORE] '),
    (r'より', ' [CMP_THAN] '), # 「~枚より」
    (r'少ない', ' [CMP_FEW] '),
    
    # 特定フレーズ・名詞
    (r'効果がない', ' [FIL_NO_EFFECT_PRED] '), # ウタ「効果がない」
    (r'ドン!!フェイズ', ' [PHASE_DON] '),
    (r'フェイズ', ' [NOUN_PHASE] '), # 汎用の「フェイズ」
        # --- 19. グランドフィナーレ:特定の用語・ルール・記号 ---
    
    # 条件の結合順序修正 (最優先)
    (r'少ない場合', ' [CND_COUNT_LESS_IF] '), # 「ない場合」に吸われるのを防ぐ
    
    # 宣言・カード名・対象 (ビッグマム・五老星・オカマ道)
    (r'宣言した', ' [ACT_DECLARED] '),
    (r'宣言し', ' [ACT_DECLARE_SEQ] '),
    (r'宣言する', ' [ACT_DECLARE_DO] '),
    (r'カード名', ' [NOUN_CARD_NAME] '),
    (r'異なる', ' [CND_DIFFERENT] '),
    (r'同じ', ' [CND_SAME] '),
    (r'対象', ' [NOUN_TARGET] '),
    (r'変更する', ' [ACT_CHANGE] '),
    
    # その他
    (r'追加で', ' [ADV_ADDITIONALLY] '), # 紫ルフィ「ターンを追加で得る」
    (r'後', ' [NOUN_AFTER] '),
    (r'回', ' [CTR_TIMES] '),
    (r',', ' [SEP_COMMA] '), # ジャッジ等のテキストに含まれるカンマ
        # --- 20. 最終解決:残り3枚の完全消去 ---
    
    # [ナミ] 対策
    (r'いて', ' [CND_EXIST_TE] '),
    (r'て', ' [SEP_TE] '), # 万が一の汎用助詞
    
    # [バッファロー] 対策
    (r'戻し', ' [ACT_RETURN_SEQ_GEN] '),
    
    # [ゼット] 対策
    (r'する', ' [ACT_DO_GEN] '),
]

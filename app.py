import streamlit as st

st.set_page_config(page_title="Pro Odds Analyzer V7", page_icon="⚽", layout="centered")

st.title("⚽ เครื่องมือวิเคราะห์บอลคู่ (Pro V7 - Per-Row Matchup)")
st.caption("รองรับราคาผสมในคู่เดียว: เจ้าบ้านต่อ, เสมอ (0), หรือทีมเยือนต่อ แยกอิสระ 3 แถว")

def process_handicap_rows(fav_sides, handicaps, left_odds, right_odds, l_name, r_name):
    weights = [0.50, 0.25, 0.25]
    total_l = 0.0
    total_r = 0.0
    rows = []
    
    for i in range(3):
        side = fav_sides[i]
        h_str = str(handicaps[i])
        l = left_odds[i]
        r = right_odds[i]
        
        prob_l = (1.0 / l) * 100.0 if l > 0 else 0.0
        prob_r = (1.0 / r) * 100.0 if r > 0 else 0.0
        margin = (prob_l + prob_r) - 100.0
        
        fair_l = (prob_l / (prob_l + prob_r)) * 100.0 if (prob_l + prob_r) > 0 else 50.0
        fair_r = (prob_r / (prob_l + prob_r)) * 100.0 if (prob_l + prob_r) > 0 else 50.0
        
        bonus_l = 3.0 if (0 < l <= 1.78) else 0.0
        bonus_r = 3.0 if (0 < r <= 1.78) else 0.0
        
        norm_l = (fair_l + bonus_l)
        norm_r = (fair_r + bonus_r)
        sum_norm = norm_l + norm_r
        norm_l = (norm_l / sum_norm) * 100.0 if sum_norm > 0 else 50.0
        norm_r = (norm_r / sum_norm) * 100.0 if sum_norm > 0 else 50.0
        
        total_l += norm_l * weights[i]
        total_r += norm_r * weights[i]
        
        # ป้ายกำกับแต้มต่อตามแถว
        if side == "เจ้าบ้านต่อ":
            lbl_l = f"ต่อ {h_str}"
            lbl_r = f"รอง {h_str}"
        elif side == "ทีมเยือนต่อ":
            lbl_l = f"รอง {h_str}"
            lbl_r = f"ต่อ {h_str}"
        else:
            lbl_l = "เสมอ 0"
            lbl_r = "เสมอ 0"
            
        rows.append({
            "side": side,
            "handicap": h_str,
            "lbl_l": lbl_l,
            "lbl_r": lbl_r,
            "l_prob": norm_l,
            "r_prob": norm_r,
            "margin": margin
        })
        
    return rows, total_l, total_r

def process_ou_rows(rates, overs, unders):
    weights = [0.50, 0.25, 0.25]
    total_o = 0.0
    total_u = 0.0
    
    for i in range(3):
        o = overs[i]
        u = unders[i]
        
        prob_o = (1.0 / o) * 100.0 if o > 0 else 0.0
        prob_u = (1.0 / u) * 100.0 if u > 0 else 0.0
        
        fair_o = (prob_o / (prob_o + prob_u)) * 100.0 if (prob_o + prob_u) > 0 else 50.0
        fair_u = (prob_u / (prob_o + prob_u)) * 100.0 if (prob_o + prob_u) > 0 else 50.0
        
        total_o += fair_o * weights[i]
        total_u += fair_u * weights[i]
        
    return total_o, total_u

# --- 1. ระบุชื่อทีม ---
st.subheader("📌 1. ระบุชื่อทีม")
c_t1, c_t2 = st.columns(2)
with c_t1:
    team_home = st.text_input("ทีมเหย้า (ฝั่งซ้าย)", value="โอลิมปิคโคเปนฮาเก้น")
with c_t2:
    team_away = st.text_input("ทีมเยือน (ฝั่งขวา)", value="เซลต้าบีโก้")

st.markdown("---")

# --- 2. แฮนดิแคป (แยกแถวอิสระ) ---
st.subheader("🎯 2. ราคาต่อรอง แฮนดิแคป (กำหนดฝั่งต่อแยกแต่ละแถว)")
side_opts = ["เจ้าบ้านต่อ", "ทีมเยือนต่อ", "เสมอ (0)"]

col_h1, col_h2, col_h3 = st.columns(3)

with col_h1:
    st.markdown("**แถว 1 (ราคาหลัก)**")
    side_1 = st.selectbox("ฝั่งต่อ (1)", side_opts, index=1, key="side1")
    h_rate1 = st.text_input("แต้มต่อ (1)", value="0.5", key="hr1")
    h_l1 = st.number_input(f"น้ำ {team_home} (1)", value=2.11, step=0.01, key="hl1")
    h_r1 = st.number_input(f"น้ำ {team_away} (1)", value=1.83, step=0.01, key="hr_1")

with col_h2:
    st.markdown("**แถว 2 (ราคารอง 1)**")
    side_2 = st.selectbox("ฝั่งต่อ (2)", side_opts, index=1, key="side2")
    h_rate2 = st.text_input("แต้มต่อ (2)", value="0.5-1", key="hr2")
    h_l2 = st.number_input(f"น้ำ {team_home} (2)", value=1.82, step=0.01, key="hl2")
    h_r2 = st.number_input(f"น้ำ {team_away} (2)", value=2.10, step=0.01, key="hr_2")

with col_h3:
    st.markdown("**แถว 3 (ราคารอง 2)**")
    side_3 = st.selectbox("ฝั่งต่อ (3)", side_opts, index=1, key="side3")
    h_rate3 = st.text_input("แต้มต่อ (3)", value="0-0.5", key="hr3")
    h_l3 = st.number_input(f"น้ำ {team_home} (3)", value=2.46, step=0.01, key="hl3")
    h_r3 = st.number_input(f"น้ำ {team_away} (3)", value=1.60, step=0.01, key="hr_3")

st.markdown("---")

# --- 3. สูง-ต่ำ ---
st.subheader("⚽ 3. ราคาสูง-ต่ำ (3 แถว)")
col_u1, col_u2, col_u3 = st.columns(3)

with col_u1:
    st.markdown("**สูงต่ำ แถว 1**")
    ou_rate1 = st.text_input("เรต สูงต่ำ (1)", value="2-2.5", key="our1")
    ou_o1 = st.number_input("น้ำ สูง (1)", value=1.83, step=0.01, key="ouo1")
    ou_u1 = st.number_input("น้ำ ต่ำ (1)", value=2.06, step=0.01, key="ouu1")

with col_u2:
    st.markdown("**สูงต่ำ แถว 2**")
    ou_rate2 = st.text_input("เรต สูงต่ำ (2)", value="2.5", key="our2")
    ou_o2 = st.number_input("น้ำ สูง (2)", value=2.12, step=0.01, key="ouo2")
    ou_u2 = st.number_input("น้ำ ต่ำ (2)", value=1.78, step=0.01, key="ouu2")

with col_u3:
    st.markdown("**สูงต่ำ แถว 3**")
    ou_rate3 = st.text_input("เรต สูงต่ำ (3)", value="2", key="our3")
    ou_o3 = st.number_input("น้ำ สูง (3)", value=1.59, step=0.01, key="ouo3")
    ou_u3 = st.number_input("น้ำ ต่ำ (3)", value=2.42, step=0.01, key="ouu3")

st.markdown("---")

if st.button("🚀 ประมวลผลและชี้เป้าทีเด็ด (Pro V7)", use_container_width=True):
    fav_sides = [side_1, side_2, side_3]
    h_handicaps = [h_rate1, h_rate2, h_rate3]
    h_left = [h_l1, h_l2, h_l3]
    h_right = [h_r1, h_r2, h_r3]
    
    h_rows, total_l, total_r = process_handicap_rows(fav_sides, h_handicaps, h_left, h_right, team_home, team_away)
    ou_score_o, ou_score_u = process_ou_rows([ou_rate1, ou_rate2, ou_rate3], [ou_o1, ou_o2, ou_o3], [ou_u1, ou_u2, ou_u3])
    
    diff = abs(total_l - total_r)
    confidence = min(88.0, 50.0 + (diff * 1.6))
    
    # เลือกฝั่งที่ได้เปรียบ
    winner_team = team_home if total_l > total_r else team_away
    main_row = h_rows[0]
    
    if total_l > total_r:
        recommended_action = f"{main_row['lbl_l']} {team_home}"
        reason = f"ค่าน้ำเอื้อฝั่ง [{team_home}] อย่างมีนัยสำคัญ ได้เปรียบทั้งแต้มต่อและราคาจ่าย"
    else:
        recommended_action = f"{main_row['lbl_r']} {team_away}"
        reason = f"ค่าน้ำเอื้อฝั่ง [{team_away}] อย่างมีนัยสำคัญ ได้เปรียบทั้งแต้มต่อและราคาจ่าย"
        
    ou_winner = "สูง" if ou_score_o > ou_score_u else "ต่ำ"
    ou_prob = min(88.0, 50.0 + (abs(ou_score_o - ou_score_u) * 1.5))
    
    st.subheader("🏆 ผลสรุปฟันธงระดับมืออาชีพ (Pro V7)")
    
    if confidence >= 75.0:
        st.success(f"🎯 **คำแนะนำ:** **วาง {recommended_action}**")
        badge = "🟢 เล่นได้ทั้งบอลเต็งและสเต็ป (เกรด A)"
    elif confidence >= 68.0:
        st.info(f"🎯 **คำแนะนำ:** **วาง {recommended_action}**")
        badge = "🔵 เหมาะสำหรับบอลเต็งเดี่ยวเท่านั้น (เกรด B)"
    else:
        st.warning(f"⚠️ **คำแนะนำ:** **วาง {recommended_action}** (ความได้เปรียบไม่ขาด)")
        badge = "🟡 ตลาดก้ำกึ่ง ห้ามใส่สเต็ปเด็ดขาด"
        
    st.markdown(f"👉 **ราคาที่แนะนำของแถวหลัก:** **{recommended_action}**")
    st.markdown(f"📈 **ระดับความมั่นใจ:** **`{confidence:.1f}%`** ({badge})")
    st.caption(f"💡 **เหตุผลเชิงลึก:** {reason} | ทิศทางสกอร์รวม: {ou_winner} ({ou_prob:.1f}%)")

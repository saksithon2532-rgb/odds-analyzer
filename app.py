
import streamlit as st

st.set_page_config(page_title="Pro Odds Analyzer V6", page_icon="⚽", layout="centered")

st.title("⚽ เครื่องมือวิเคราะห์บอลคู่ (Pro V6 - Fixed Matchup)")
st.caption("แก้ไขตรรกะทีมต่อ/รองให้ถูกต้อง 100% ทั้งกรณีเหย้าต่อและเยือนต่อ")

# ฟังก์ชันคำนวณความได้เปรียบของราคา
def process_market(handicaps, left_odds, right_odds, l_name, r_name):
    weights = [0.50, 0.25, 0.25]
    total_l = 0
    total_r = 0
    rows = []
    
    for i in range(3):
        h = str(handicaps[i])
        l = left_odds[i]
        r = right_odds[i]
        
        prob_l = (1 / l) * 100 if l > 0 else 0
        prob_r = (1 / r) * 100 if r > 0 else 0
        margin = (prob_l + prob_r) - 100
        
        fair_l = (prob_l / (prob_l + prob_r)) * 100 if (prob_l + prob_r) > 0 else 50
        fair_r = (prob_r / (prob_l + prob_r)) * 100 if (prob_r + prob_r) > 0 else 50
        
        bonus_l = 3.0 if (0 < l <= 1.78) else 0.0
        bonus_r = 3.0 if (0 < r <= 1.78) else 0.0
        
        adj_l = fair_l + bonus_l
        adj_r = fair_r + bonus_r
        
        norm_l = (adj_l / (adj_l + adj_r)) * 100 if (adj_l + adj_r) > 0 else 50
        norm_r = (adj_r / (adj_l + adj_r)) * 100 if (adj_l + adj_r) > 0 else 50
        
        total_l += norm_l * weights[i]
        total_r += norm_r * weights[i]
        
        adv = f"{l_name} ({h})" if norm_l > norm_r else f"{r_name} ({h})"
        rows.append({
            "handicap": h,
            "l_odds": l,
            "r_odds": r,
            "l_prob": norm_l,
            "r_prob": norm_r,
            "adv": adv,
            "margin": margin
        })
        
    return rows, total_l, total_r

def parse_rate(rate_str, default_val=1.0):
    try:
        cleaned = str(rate_str).split('/')[0].split('-')[0].strip()
        return float(cleaned)
    except:
        return default_val

# --- 1. ระบุชื่อทีม ---
st.subheader("📌 1. ระบุชื่อทีม")
c_t1, c_t2 = st.columns(2)
with c_t1:
    team_home = st.text_input("ทีมเหย้า (ซ้าย)", value="โอลิมปิคโคเปนฮาเก้น")
with c_t2:
    team_away = st.text_input("ทีมเยือน (ขวา)", value="เซลต้าบีโก้")

fav_side = st.radio("ทีมไหนเป็นฝ่ายต่อ?", [f"เจ้าบ้าน ({team_home}) ต่อ", f"ทีมเยือน ({team_away}) ต่อ"], horizontal=True)
home_is_fav = (fav_side == f"เจ้าบ้าน ({team_home}) ต่อ")

st.markdown("---")

# --- 2. แฮนดิแคป ---
st.subheader("🎯 2. ราคาต่อรอง แฮนดิแคป (3 แถว)")
col_h1, col_h2, col_h3 = st.columns(3)
with col_h1:
    h_rate1 = st.text_input("แต้มต่อ แถว 1 (หลัก)", value="0.5")
    h_l1 = st.number_input(f"น้ำ {team_home} (1)", value=2.11, step=0.01)
    h_r1 = st.number_input(f"น้ำ {team_away} (1)", value=1.83, step=0.01)
with col_h2:
    h_rate2 = st.text_input("แต้มต่อ แถว 2 (รอง 1)", value="0.5-1")
    h_l2 = st.number_input(f"น้ำ {team_home} (2)", value=1.82, step=0.01)
    h_r2 = st.number_input(f"น้ำ {team_away} (2)", value=2.10, step=0.01)
with col_h3:
    h_rate3 = st.text_input("แต้มต่อ แถว 3 (รอง 2)", value="0-0.5")
    h_l3 = st.number_input(f"น้ำ {team_home} (3)", value=2.46, step=0.01)
    h_r3 = st.number_input(f"น้ำ {team_away} (3)", value=1.60, step=0.01)

st.markdown("---")

# --- 3. สูง-ต่ำ ---
st.subheader("⚽ 3. ราคาสูง-ต่ำ (3 แถว)")
col_u1, col_u2, col_u3 = st.columns(3)
with col_u1:
    ou_rate1 = st.text_input("เรต สูงต่ำ แถว 1", value="2-2.5")
    ou_o1 = st.number_input("น้ำ สูง (1)", value=1.83, step=0.01)
    ou_u1 = st.number_input("น้ำ ต่ำ (1)", value=2.06, step=0.01)
with col_u2:
    ou_rate2 = st.text_input("เรต สูงต่ำ แถว 2", value="2.5")
    ou_o2 = st.number_input("น้ำ สูง (2)", value=2.12, step=0.01)
    ou_u2 = st.number_input("น้ำ ต่ำ (2)", value=1.78, step=0.01)
with col_u3:
    ou_rate3 = st.text_input("เรต สูงต่ำ แถว 3", value="2")
    ou_o3 = st.number_input("น้ำ สูง (3)", value=1.59, step=0.01)
    ou_u3 = st.number_input("น้ำ ต่ำ (3)", value=2.42, step=0.01)

st.markdown("---")

if st.button("🚀 ประมวลผลและชี้เป้าทีเด็ด", use_container_width=True):
    h_handicaps = [h_rate1, h_rate2, h_rate3]
    h_left = [h_l1, h_l2, h_l3]
    h_right = [h_r1, h_r2, h_r3]
    h_rows, h_score_l, h_score_r = process_market(h_handicaps, h_left, h_right, team_home, team_away)
    
    ou_rates = [ou_rate1, ou_rate2, ou_rate3]
    ou_left = [ou_o1, ou_o2, ou_o3]
    ou_right = [ou_u1, ou_u2, ou_u3]
    ou_rows, ou_score_o, ou_score_u = process_market(ou_rates, ou_left, ou_right, "สูง", "ต่ำ")
    
    base_ou = parse_rate(ou_rate1, default_val=2.5)
    ou_diff = abs(ou_score_o - ou_score_u)
    ou_winner = "สูง" if ou_score_o > ou_score_u else "ต่ำ"
    ou_prob = min(88.0, 50.0 + (ou_diff * 1.5))
    
    # กำหนดฝั่งต่อและรองที่แท้จริง
    fav_team = team_home if home_is_fav else team_away
    und_team = team_away if home_is_fav else team_home
    fav_score = h_score_l if home_is_fav else h_score_r
    und_score = h_score_r if home_is_fav else h_score_l
    
    diff = abs(fav_score - und_score)
    confidence = min(88.0, 50.0 + (diff * 1.6))
    
    if fav_score > und_score:
        recommended = f"ต่อ {fav_team}"
        pick_rate = f"เรต {h_rate1}"
        reason = f"ค่าน้ำไหลเอื้อฝั่งทีมต่อ [{fav_team}] ชัดเจน"
    else:
        recommended = f"รอง {und_team}"
        pick_rate = f"เรต {h_rate1}"
        reason = f"ค่าน้ำฝั่งทีมต่อเสียเปรียบ แนะนำถือหางทีมรอง [{und_team}] ได้เปรียบแต้มต่อ"
        
    st.subheader("🏆 ผลสรุปฟันธงระดับมืออาชีพ (Pro V6)")
    
    if confidence >= 75.0:
        st.success(f"🎯 **คำแนะนำ:** {recommended}")
        badge = "🟢 เล่นได้ทั้งบอลเต็งและสเต็ป"
    elif confidence >= 68.0:
        st.info(f"🎯 **คำแนะนำ:** {recommended}")
        badge = "🔵 เหมาะสำหรับบอลเต็งเดี่ยวเท่านั้น"
    else:
        st.warning(f"⚠️ **คำแนะนำ:** {recommended} (เลี่ยงได้ควรเลี่ยง)")
        badge = "🟡 ตลาดก้ำกึ่ง ไม่คุ้มความเสี่ยง ห้ามใส่สเต็ปเด็ดขาด"
        
    st.markdown(f"👉 **ราคาที่แนะนำ:** **{pick_rate}**")
    st.markdown(f"📈 **ระดับความมั่นใจ:** **`{confidence:.1f}%`** ({badge})")
    st.caption(f"💡 **เหตุผลเชิงลึก:** {reason} | ทิศทางสกอร์รวม: {ou_winner} ({ou_prob:.1f}%)")

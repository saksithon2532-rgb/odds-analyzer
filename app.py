import streamlit as st

st.set_page_config(page_title="Pro Odds & Over/Under Analyzer V3", page_icon="⚽", layout="centered")

st.title("⚽ เครื่องมือวิเคราะห์บอลคู่: แฮนดิแคป + สูงต่ำ (Pro V3)")
st.caption("ระบบผสานสองตลาด ตรวจจับราคาควบลูก ออโต้เรตปลอดภัย และเตือนตลาดขัดแย้ง (Smart Safe Pick)")

# ฟังก์ชันแปลงราคาแต้มต่อ/สูงต่ำให้เป็นตัวเลขทศนิยมแม่นยำ
def parse_rate(rate_str, default_val=1.0):
    try:
        s = str(rate_str).strip().replace('/', '-')
        if '-' in s:
            parts = s.split('-')
            v1 = float(parts[0])
            v2 = float(parts[1])
            return (v1 + v2) / 2.0
        return float(s)
    except:
        return default_val

# ฟังก์ชันคำนวณค่าน้ำรายตลาด
def process_market(handicaps, left_odds, right_odds, l_name, r_name, is_ou=False):
    weights = [0.50, 0.25, 0.25]
    total_l = 0
    total_r = 0
    rows = []
    
    for i in range(3):
        h_str = str(handicaps[i])
        h_val = parse_rate(h_str, 0.0)
        l = left_odds[i]
        r = right_odds[i]
        
        prob_l = (1 / l) * 100 if l > 0 else 0
        prob_r = (1 / r) * 100 if r > 0 else 0
        margin = (prob_l + prob_r) - 100
        
        fair_l = (prob_l / (prob_l + prob_r)) * 100 if (prob_l + prob_r) > 0 else 50
        fair_r = (prob_r / (prob_l + prob_r)) * 100 if (prob_l + prob_r) > 0 else 50
        
        # จับสัญญาณบีบค่าน้ำต่ำ (Juice Trap)
        bonus_l = 3.5 if (0 < l <= 1.78) else 0.0
        bonus_r = 3.5 if (0 < r <= 1.78) else 0.0
        
        adj_l = fair_l + bonus_l
        adj_r = fair_r + bonus_r
        
        norm_l = (adj_l / (adj_l + adj_r)) * 100 if (adj_l + adj_r) > 0 else 50
        norm_r = (adj_r / (adj_r + adj_r)) * 100 if (adj_l + adj_r) > 0 else 50
        
        total_l += norm_l * weights[i]
        total_r += norm_r * weights[i]
        
        adv = f"{l_name} ({h_str})" if norm_l > norm_r else f"{r_name} ({h_str})"
        rows.append({
            "handicap_str": h_str,
            "handicap_val": h_val,
            "l_odds": l,
            "r_odds": r,
            "l_prob": norm_l,
            "r_prob": norm_r,
            "adv": adv,
            "margin": margin
        })
        
    return rows, total_l, total_r

# --- ส่วนรับข้อมูล ---
st.subheader("📌 1. ระบุชื่อทีม")
c_t1, c_t2 = st.columns(2)
with c_t1:
    team_home = st.text_input("ทีมเหย้า (ต่อ/ซ้าย)", value="atletico madrid")
with c_t2:
    team_away = st.text_input("ทีมเยือน (รอง/ขวา)", value="โอซาซูน่า")

st.markdown("---")

# 1. แฮนดิแคป (Handicap)
st.subheader("🎯 2. ราคาต่อรอง แฮนดิแคป (3 แถว)")
col_h1, col_h2, col_h3 = st.columns(3)
with col_h1:
    h_rate1 = st.text_input("แต้มต่อ แถว 1 (หลัก)", value="1-1.5")
    h_l1 = st.number_input(f"น้ำ {team_home} (1)", value=1.89, step=0.01)
    h_r1 = st.number_input(f"น้ำ {team_away} (1)", value=2.04, step=0.01)
with col_h2:
    h_rate2 = st.text_input("แต้มต่อ แถว 2 (รอง 1)", value="1.5")
    h_l2 = st.number_input(f"น้ำ {team_home} (2)", value=2.19, step=0.01)
    h_r2 = st.number_input(f"น้ำ {team_away} (2)", value=1.77, step=0.01)
with col_h3:
    h_rate3 = st.text_input("แต้มต่อ แถว 3 (รอง 2)", value="1")
    h_l3 = st.number_input(f"น้ำ {team_home} (3)", value=1.63, step=0.01)
    h_r3 = st.number_input(f"น้ำ {team_away} (3)", value=2.41, step=0.01)

st.markdown("---")

# 2. สูง-ต่ำ (Over / Under)
st.subheader("⚽ 3. ราคาสูง-ต่ำ (Over / Under 3 แถว)")
col_u1, col_u2, col_u3 = st.columns(3)
with col_u1:
    ou_rate1 = st.text_input("เรต สูงต่ำ แถว 1 (หลัก)", value="2.5-3")
    ou_o1 = st.number_input("น้ำ สูง (Over 1)", value=2.01, step=0.01)
    ou_u1 = st.number_input("น้ำ ต่ำ (Under 1)", value=1.98, step=0.01)
with col_u2:
    ou_rate2 = st.text_input("เรต สูงต่ำ แถว 2 (รอง 1)", value="2.5")
    ou_o2 = st.number_input("น้ำ สูง (Over 2)", value=1.78, step=0.01)
    ou_u2 = st.number_input("น้ำ ต่ำ (Under 2)", value=2.15, step=0.01)
with col_u3:
    ou_rate3 = st.text_input("เรต สูงต่ำ แถว 3 (รอง 2)", value="3")
    ou_o3 = st.number_input("น้ำ สูง (Over 3)", value=2.41, step=0.01)
    ou_u3 = st.number_input("น้ำ ต่ำ (Under 3)", value=1.61, step=0.01)

st.markdown("---")

if st.button("🚀 ประมวลผลและชี้เป้าทีเด็ด", use_container_width=True):
    h_handicaps = [h_rate1, h_rate2, h_rate3]
    h_left = [h_l1, h_l2, h_l3]
    h_right = [h_r1, h_r2, h_r3]
    h_rows, h_score_l, h_score_r = process_market(h_handicaps, h_left, h_right, team_home, team_away)
    
    ou_rates = [ou_rate1, ou_rate2, ou_rate3]
    ou_left = [ou_o1, ou_o2, ou_o3]
    ou_right = [ou_u1, ou_u2, ou_u3]
    ou_rows, ou_score_o, ou_score_u = process_market(ou_rates, ou_left, ou_right, "สูง", "ต่ำ", is_ou=True)
    
    base_h = parse_rate(h_rate1, 1.0)
    base_ou = parse_rate(ou_rate1, 2.5)
    
    # ค้นหาเรตที่ปลอดภัยที่สุดตามหลักคณิตศาสตร์
    lowest_h_row = min(h_rows, key=lambda x: x['handicap_val'])   # ต่อน้อยสุด
    highest_h_row = max(h_rows, key=lambda x: x['handicap_val'])  # รองเยอะสุด
    lowest_ou_row = min(ou_rows, key=lambda x: x['handicap_val'])  # สูงต่ำเรตต่ำสุด
    highest_ou_row = max(ou_rows, key=lambda x: x['handicap_val']) # สูงต่ำเรตสูงสุด
    
    h_winner = team_home if h_score_l > h_score_r else team_away
    h_diff = abs(h_score_l - h_score_r)
    h_win_prob = min(88.0, 50.0 + (h_diff * 1.6))
    
    ou_winner = "สูง (Over)" if ou_score_o > ou_score_u else "ต่ำ (Under)"
    ou_diff = abs(ou_score_o - ou_score_u)
    ou_win_prob = min(88.0, 50.0 + (ou_diff * 1.6))
    
    # ดักจับบอลต่อลึก / บอลถล่มยับ
    is_blowout_game = (base_h >= 2.0) or (base_ou >= 3.75)
    
    if is_blowout_game and base_ou >= 3.5:
        best_pick = f"ต่อ {team_home}"
        best_rate = f"เรต {lowest_h_row['handicap_str']} หรือ สูง {lowest_ou_row['handicap_str']}"
        best_confidence = min(88.0, 68.0 + (base_ou * 2.5))
        analysis_reason = f"⚠️ บอลเกรดต่างชั้นถล่มยับ! โต๊ะเปิดเรตสกอร์รวม {base_ou} ลูก ห้ามเล่นรองหรือต่ำเด็ดขาด"
    elif h_winner == team_home:
        if "สูง" in ou_winner:
            best_pick = f"ต่อ {team_home}"
            best_rate = f"เรต {lowest_h_row['handicap_str']}"
            best_confidence = min(87.5, (h_win_prob * 0.6) + (ou_win_prob * 0.4) + 2.0)
            analysis_reason = "ค่าน้ำฝั่งต่อไหลเข้าทางพร้อมตลาดสูง มีโอกาสยิงทะลุราคาขาดลอย"
        else:
            best_pick = f"ต่อ {team_home} (เน้นเรตปลอดภัยสุด)"
            best_rate = f"เรต {lowest_h_row['handicap_str']}"
            best_confidence = max(55.0, (h_win_prob * 0.7) + ((100 - ou_win_prob) * 0.3))
            analysis_reason = f"ทีมต่อได้เปรียบแต่น้ำสกอร์รวมบีบต่ำ ระวังชนะเฉือน แนะนำให้เล่นเรตต่ำสุด ({lowest_h_row['handicap_str']}) เพื่อกันบิลแตก"
    else:
        if "ต่ำ" in ou_winner and base_ou <= 2.75:
            best_pick = f"รอง {team_away}"
            best_rate = f"เรต {highest_h_row['handicap_str']}"
            best_confidence = min(88.0, (h_win_prob * 0.6) + (ou_win_prob * 0.4) + 2.0)
            analysis_reason = "เรตปกติและน้ำเอียงไปทางสกอร์ต่ำ บอลมีทรงรัดกุม รองแล้วได้เปรียบสูง"
        else:
            best_pick = f"รอง {team_away} (แต้มต่อสูงสุด)"
            best_rate = f"เรต {highest_h_row['handicap_str']}"
            best_confidence = 58.0
            analysis_reason = f"สัญญาณค่าน้ำสวนทางกับรูปเกม หากต้องการลงทุน ให้เน้นเรตรองที่ได้แต้มต่อมากที่สุด ({highest_h_row['handicap_str']})"

    # แสดงผลลัพธ์
    st.subheader("🏆 ผลสรุปฟันธงระดับมืออาชีพ (Pro Pick)")
    st.success(f"🎯 **แนะนำการลงทุนที่ดีที่สุด:** **{best_pick}**")
    st.markdown(f"👉 **ราคาที่น่าสนใจที่สุด:** **{best_rate}**")
    st.markdown(f"📈 **ระดับความน่าลงทุน (เปอร์เซ็นต์ชนะ):** **`{best_confidence:.1f}%`**")
    
    if best_confidence >= 70.0:
        st.info(f"💡 **เหตุผลเชิงลึก:** {analysis_reason}")
    else:
        st.warning(f"⚠️ **ตลาดขัดแย้งกัน (Divergence):** {analysis_reason}\n\n👉 **คำแนะนำ:** ความมั่นใจต่ำกว่า 70% ควรหลีกเลี่ยงการใส่บิลสเต็ป หรือเน้นเล่นเป็นบอลเต็งเรตปลอดภัยเท่านั้น")
    
    st.markdown("---")
    st.subheader("📊 ตรวจสอบข้อมูลแยกแต่ละตลาด")
    c_res1, c_res2 = st.columns(2)
    with c_res1:
        st.write(f"**ฝั่งแฮนดิแคป:** {h_winner}")
        st.caption(f"ดัชนีน้ำไหล: {h_win_prob:.1f}%")
        for r in h_rows:
            st.text(f"เรต {r['handicap_str']}: ได้เปรียบ -> {r['adv']}")
    with c_res2:
        st.write(f"**ฝั่งสกอร์รวม:** {ou_winner}")
        st.caption(f"ดัชนีน้ำไหล: {ou_win_prob:.1f}%")
        for r in ou_rows:
            st.text(f"เรต {r['handicap_str']}: ได้เปรียบ -> {r['adv']}")

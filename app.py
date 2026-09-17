
import streamlit as st

st.set_page_config(page_title="Pro Odds & Over/Under Analyzer V4", page_icon="⚽", layout="centered")

st.title("⚽ เครื่องมือวิเคราะห์บอลคู่: แฮนดิแคป + สูงต่ำ (Pro V4)")
st.caption("ระบบผสานสองตลาด ตรวจจับราคาสลับฝั่งต่อ ออโต้เรตปลอดภัย และเตือนตลาดขัดแย้ง")

# ฟังก์ชันแปลงราคาแต้มต่อเป็นตัวเลขทศนิยม
def parse_rate(rate_str, default_val=0.0):
    try:
        s = str(rate_str).strip().replace('/', '-')
        if '-' in s:
            parts = s.split('-')
            v1 = abs(float(parts[0]))
            v2 = abs(float(parts[1]))
            return (v1 + v2) / 2.0
        return abs(float(s))
    except:
        return default_val

# ฟังก์ชันคำนวณค่าน้ำรายตลาด
def process_market(handicap_labels, handicap_vals, left_odds, right_odds, l_name, r_name):
    weights = [0.50, 0.25, 0.25]
    total_l = 0
    total_r = 0
    rows = []
    
    for i in range(3):
        h_str = str(handicap_labels[i])
        h_val = handicap_vals[i] # ค่าบวก = เจ้าบ้านต่อ, ค่าลบ = เยือนต่อ, 0 = เสมอ
        l = left_odds[i]
        r = right_odds[i]
        
        prob_l = (1 / l) * 100 if l > 0 else 0
        prob_r = (1 / r) * 100 if r > 0 else 0
        margin = (prob_l + prob_r) - 100
        
        fair_l = (prob_l / (prob_l + prob_r)) * 100 if (prob_l + prob_r) > 0 else 50
        fair_r = (prob_r / (prob_l + prob_r)) * 100 if (prob_l + prob_r) > 0 else 50
        
        bonus_l = 3.5 if (0 < l <= 1.78) else 0.0
        bonus_r = 3.5 if (0 < r <= 1.78) else 0.0
        
        adj_l = fair_l + bonus_l
        adj_r = fair_r + bonus_r
        
        norm_l = (adj_l / (adj_l + adj_r)) * 100 if (adj_l + adj_r) > 0 else 50
        norm_r = (adj_r / (adj_l + adj_r)) * 100 if (adj_l + adj_r) > 0 else 50
        
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
    team_home = st.text_input("ทีมเหย้า", value="ทีมเหย้า")
with c_t2:
    team_away = st.text_input("ทีมเยือน", value="ทีมเยือน")

st.markdown("---")

# 1. แฮนดิแคป
st.subheader("🎯 2. ราคาต่อรอง แฮนดิแคป (3 แถว)")
st.caption("💡 สามารถเลือกได้ว่าแถวไหน เจ้าบ้านต่อ / ทีมเยือนต่อ / หรือราคาเสมอ")

col_h1, col_h2, col_h3 = st.columns(3)

with col_h1:
    fav1 = st.selectbox("ฝั่งต่อ (แถว 1)", [f"{team_home} ต่อ", f"{team_away} ต่อ", "เสมอ (0)"], index=0)
    h_rate1 = st.text_input("แต้มต่อ แถว 1", value="0-0.5")
    h_l1 = st.number_input(f"น้ำ {team_home} (1)", value=1.95, step=0.01)
    h_r1 = st.number_input(f"น้ำ {team_away} (1)", value=1.95, step=0.01)

with col_h2:
    fav2 = st.selectbox("ฝั่งต่อ (แถว 2)", [f"{team_home} ต่อ", f"{team_away} ต่อ", "เสมอ (0)"], index=2)
    h_rate2 = st.text_input("แต้มต่อ แถว 2", value="0")
    h_l2 = st.number_input(f"น้ำ {team_home} (2)", value=1.75, step=0.01)
    h_r2 = st.number_input(f"น้ำ {team_away} (2)", value=2.15, step=0.01)

with col_h3:
    fav3 = st.selectbox("ฝั่งต่อ (แถว 3)", [f"{team_home} ต่อ", f"{team_away} ต่อ", "เสมอ (0)"], index=1)
    h_rate3 = st.text_input("แต้มต่อ แถว 3", value="0-0.5")
    h_l3 = st.number_input(f"น้ำ {team_home} (3)", value=2.25, step=0.01)
    h_r3 = st.number_input(f"น้ำ {team_away} (3)", value=1.68, step=0.01)

st.markdown("---")

# 2. สูง-ต่ำ
st.subheader("⚽ 3. ราคาสูง-ต่ำ (Over / Under 3 แถว)")
col_u1, col_u2, col_u3 = st.columns(3)
with col_u1:
    ou_rate1 = st.text_input("เรต สูงต่ำ แถว 1 (หลัก)", value="2-2.5")
    ou_o1 = st.number_input("น้ำ สูง (Over 1)", value=1.95, step=0.01)
    ou_u1 = st.number_input("น้ำ ต่ำ (Under 1)", value=1.95, step=0.01)
with col_u2:
    ou_rate2 = st.text_input("เรต สูงต่ำ แถว 2", value="2")
    ou_o2 = st.number_input("น้ำ สูง (Over 2)", value=1.70, step=0.01)
    ou_u2 = st.number_input("น้ำ ต่ำ (Under 2)", value=2.20, step=0.01)
with col_u3:
    ou_rate3 = st.text_input("เรต สูงต่ำ แถว 3", value="2.5")
    ou_o3 = st.number_input("น้ำ สูง (Over 3)", value=2.25, step=0.01)
    ou_u3 = st.number_input("น้ำ ต่ำ (Under 3)", value=1.65, step=0.01)

st.markdown("---")

if st.button("🚀 ประมวลผลและชี้เป้าทีเด็ด", use_container_width=True):
    # คำนวณแต้มต่อสุทธิ (+ = เจ้าบ้านได้เปรียบต่อ, - = เยือนต่อ)
    raw_rates = [h_rate1, h_rate2, h_rate3]
    fav_picks = [fav1, fav2, fav3]
    h_vals = []
    h_labels = []
    
    for r, f in zip(raw_rates, fav_picks):
        val = parse_rate(r)
        if "เสมอ" in f:
            h_vals.append(0.0)
            h_labels.append("เสมอ (0)")
        elif f == f"{team_home} ต่อ":
            h_vals.append(val)
            h_labels.append(f"{team_home} ต่อ {r}")
        else:
            h_vals.append(-val)
            h_labels.append(f"{team_away} ต่อ {r}")

    h_left = [h_l1, h_l2, h_l3]
    h_right = [h_r1, h_r2, h_r3]
    h_rows, h_score_l, h_score_r = process_market(h_labels, h_vals, h_left, h_right, team_home, team_away)
    
    ou_rates = [ou_rate1, ou_rate2, ou_rate3]
    ou_vals = [parse_rate(x, 2.5) for x in ou_rates]
    ou_left = [ou_o1, ou_o2, ou_o3]
    ou_right = [ou_u1, ou_u2, ou_u3]
    ou_rows, ou_score_o, ou_score_u = process_market(ou_rates, ou_vals, ou_left, ou_right, "สูง", "ต่ำ")
    
    base_ou = ou_vals[0]
    
    h_winner = team_home if h_score_l > h_score_r else team_away
    h_diff = abs(h_score_l - h_score_r)
    h_win_prob = min(88.0, 50.0 + (h_diff * 1.6))
    
    ou_winner = "สูง (Over)" if ou_score_o > ou_score_u else "ต่ำ (Under)"
    ou_diff = abs(ou_score_o - ou_score_u)
    ou_win_prob = min(88.0, 50.0 + (ou_diff * 1.6))
    
    # เลือกเรตปลอดภัยตามทีมที่ชนะการวิเคราะห์
    if h_winner == team_home:
        # หากเจ้าบ้านชนะ ให้เลือกเรตที่เจ้าบ้านต่อน้อยสุด หรือ ได้แต้มต่อมากสุด
        best_safe_row = min(h_rows, key=lambda x: x['handicap_val'])
        best_pick = f"วาง {team_home}"
    else:
        # หากเยือนชนะ ให้เลือกเรตที่เยือนต่อน้อยสุด หรือ ได้แต้มต่อมากสุด
        best_safe_row = max(h_rows, key=lambda x: x['handicap_val'])
        best_pick = f"วาง {team_away}"
        
    best_rate = f"เรต {best_safe_row['handicap_str']}"
    
    # ตรวจสอบความสอดคล้องของตลาด
    if (h_winner == team_home and any(v > 1.5 for v in h_vals)) or (h_winner == team_away and any(v < -1.5 for v in h_vals)):
        is_heavy_fav = True
    else:
        is_heavy_fav = False

    if is_heavy_fav and base_ou >= 3.5:
        best_confidence = min(88.0, 68.0 + (base_ou * 2.5))
        analysis_reason = f"บอลต่างชั้นชัดเจน ตลาดเปิดสูงต่ำรองรับ แนะนำลุยฝั่งต่อตามเรตปลอดภัย"
    elif ("สูง" in ou_winner and is_heavy_fav) or ("ต่ำ" in ou_winner and not is_heavy_fav):
        best_confidence = min(87.5, (h_win_prob * 0.6) + (ou_win_prob * 0.4) + 2.0)
        analysis_reason = "ค่าน้ำแฮนดิแคปและสกอร์รวมส่งเสริมกัน ทิศทางชัดเจน"
    else:
        best_confidence = max(55.0, (h_win_prob * 0.7) + ((100 - ou_win_prob) * 0.3))
        analysis_reason = f"ทิศทางค่าน้ำสองตลาดมีความย้อนแย้งกัน เลี่ยงสเต็ป หากเล่นให้เลือกเรตปลอดภัยสุด ({best_safe_row['handicap_str']})"

    # แสดงผล
    st.subheader("🏆 ผลสรุปฟันธงระดับมืออาชีพ (Pro Pick V4)")
    st.success(f"🎯 **แนะนำการลงทุนที่ดีที่สุด:** **{best_pick}**")
    st.markdown(f"👉 **ราคาที่น่าสนใจที่สุด:** **{best_rate}**")
    st.markdown(f"📈 **ระดับความน่าลงทุน (เปอร์เซ็นต์ชนะ):** **`{best_confidence:.1f}%`**")
    
    if best_confidence >= 70.0:
        st.info(f"💡 **เหตุผลเชิงลึก:** {analysis_reason}")
    else:
        st.warning(f"⚠️ **ตลาดขัดแย้งกัน (Divergence):** {analysis_reason}\n\n👉 **คำแนะนำ:** ความมั่นใจต่ำกว่า 70% ควรหลีกเลี่ยงการใส่บิลสเต็ป")
    
    st.markdown("---")
    st.subheader("📊 ตรวจสอบข้อมูลแยกแต่ละตลาด")
    c_res1, c_res2 = st.columns(2)
    with c_res1:
        st.write(f"**ฝั่งแฮนดิแคป:** {h_winner}")
        st.caption(f"ดัชนีน้ำไหล: {h_win_prob:.1f}%")
        for r in h_rows:
            st.text(f"{r['handicap_str']}: ได้เปรียบ -> {r['adv']}")
    with c_res2:
        st.write(f"**ฝั่งสกอร์รวม:** {ou_winner}")
        st.caption(f"ดัชนีน้ำไหล: {ou_win_prob:.1f}%")
        for r in ou_rows:
            st.text(f"เรต {r['handicap_str']}: ได้เปรียบ -> {r['adv']}")

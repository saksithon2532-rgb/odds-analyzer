import streamlit as st

st.set_page_config(
    page_title="Odds Analyzer V10.2 Classic Pro",
    page_icon="⚽",
    layout="centered"
)

# Dark Mode ธีมมืด สบายตา ปุ่มใหญ่จิ้มง่ายในมือถือ
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0e14;
        color: #e6edf3;
    }
    h1, h2, h3, h4, p, span, label {
        color: #f0f6fc !important;
    }
    .stTextInput input, .stNumberInput input, div[data-baseweb="select"] {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        font-size: 1.05rem !important;
    }
    div[data-baseweb="popover"] ul {
        background-color: #161b22 !important;
        color: #ffffff !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #1f6feb 0%, #238636 100%) !important;
        color: #ffffff !important;
        font-size: 1.15rem !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 20px !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.6) !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ ตัวกรองค่าน้ำแฮนดิแคป (V10.2 Classic Pro)")
st.caption("ระบบคัดเกรด A/B/C ค่าน้ำ 3 แถวราคาแบบดั้งเดิม ไม่ต้องใช้ API ใช้งานง่ายผ่านมือถือ")

# เรตราคาแฮนดิแคป 0 ถึง 7.0 ลูก
HDP_OPTIONS = [
    "เสมอ (0)", "0-0.5 (เสมอควบครึ่ง)", "0.5 (ครึ่งลูก)", "0.5-1 (ครึ่งควบลูก)",
    "1.0 (หนึ่งลูก)", "1-1.5 (ลูกควบลูกครึ่ง)", "1.5 (ลูกครึ่ง)", "1.5-2 (ลูกครึ่งควบสอง)",
    "2.0 (สองลูก)", "2-2.5 (สองควบสองครึ่ง)", "2.5 (สองลูกครึ่ง)", "2.5-3 (สองครึ่งควบสาม)",
    "3.0 (สามลูก)", "3-3.5 (สามควบสามครึ่ง)", "3.5 (สามลูกครึ่ง)", "3.5-4 (สามครึ่งควบสี่)",
    "4.0 (สี่ลูก)", "4-4.5 (สี่ควบสี่ครึ่ง)", "4.5 (สี่ลูกครึ่ง)", "4.5-5 (สี่ครึ่งควบห้า)",
    "5.0 (ห้าลูก)", "5-5.5 (ห้าควบห้าครึ่ง)", "5.5 (ห้าลูกครึ่ง)", "5.5-6 (ห้าครึ่งควบหก)",
    "6.0 (หกลูก)", "6-6.5 (หกควบหกครึ่ง)", "6.5 (หกลูกครึ่ง)", "6.5-7 (หกครึ่งควบเจ็ด)",
    "7.0 (เจ็ดลูก)"
]

# --- ส่วนที่ 1: คู่แข่งขัน & ฝั่งต่อ ---
st.subheader("📌 1. คู่แข่งขัน & ฝั่งต่อ")
c1, c2 = st.columns(2)
with c1:
    home_name = st.text_input("ทีมเหย้า (ฝั่งซ้าย)", value="เจ้าบ้าน")
with c2:
    away_name = st.text_input("ทีมเยือน (ฝั่งขวา)", value="ทีมเยือน")

fav_side = st.radio("ทีมที่เป็นฝั่งต่อ:", [f"{home_name} ต่อ", f"{away_name} ต่อ", "ราคาเสมอ"], horizontal=True)

st.markdown("---")

# --- ส่วนที่ 2: ค่าน้ำและเรตราคา 3 แถว ---
st.subheader("🔢 2. ค่าน้ำและเรตราคา 3 แถว")

# แถวที่ 1
st.markdown("🔹 **แถวที่ 1 (ราคาเปิดหลัก - น้ำหนัก 50%)**")
h_rate1 = st.selectbox("เรตแต้มต่อ แถว 1", HDP_OPTIONS, index=3, key="h_rate1")
col1_l, col1_r = st.columns(2)
with col1_l:
    h_l1 = st.number_input(f"น้ำ {home_name} (1)", value=1.85, step=0.01, format="%.2f", key="hl1")
with col1_r:
    h_r1 = st.number_input(f"น้ำ {away_name} (1)", value=2.05, step=0.01, format="%.2f", key="hr1")

# แถวที่ 2
st.markdown("🔹 **แถวที่ 2 (ราคารอง 1 - น้ำหนัก 25%)**")
h_rate2 = st.selectbox("เรตแต้มต่อ แถว 2", HDP_OPTIONS, index=4, key="h_rate2")
col2_l, col2_r = st.columns(2)
with col2_l:
    h_l2 = st.number_input(f"น้ำ {home_name} (2)", value=2.18, step=0.01, format="%.2f", key="hl2")
with col2_r:
    h_r2 = st.number_input(f"น้ำ {away_name} (2)", value=1.75, step=0.01, format="%.2f", key="hr2")

# แถวที่ 3
st.markdown("🔹 **แถวที่ 3 (ราคารอง 2 - น้ำหนัก 25%)**")
h_rate3 = st.selectbox("เรตแต้มต่อ แถว 3", HDP_OPTIONS, index=2, key="h_rate3")
col3_l, col3_r = st.columns(2)
with col3_l:
    h_l3 = st.number_input(f"น้ำ {home_name} (3)", value=1.65, step=0.01, format="%.2f", key="hl3")
with col3_r:
    h_r3 = st.number_input(f"น้ำ {away_name} (3)", value=2.35, step=0.01, format="%.2f", key="hr3")

st.markdown("---")

# --- ส่วนที่ 3: ตัวเสริมความแม่นยำ (กดเลือกได้เลย ง่าย ๆ ไม่ต้องพิมพ์) ---
st.subheader("⚡ 3. ปัจจัยเสริมหน้างาน (เลือกตามที่เห็น)")
form_status = st.radio(
    "ฟอร์มล่าสุดและการเล่น:",
    ["ปกติ / สูสีกัน", f"🔥 {home_name} ฟอร์มเหนือกว่าชัดเจน", f"🔥 {away_name} ฟอร์มเหนือกว่าชัดเจน"],
    horizontal=True
)
tier_gap = st.checkbox("🏆 ทีมต่อเกรดบอล/ชั้นลีก เหนือกว่าชัดเจน (เช่น บอลถ้วย หรือหัวตารางเจอท้ายตาราง)")

st.markdown("---")

# --- คำนวณผลลัพธ์ ---
if st.button("🚀 สรุปผลวิเคราะห์ความได้เปรียบ", use_container_width=True):
    rates = [h_rate1, h_rate2, h_rate3]
    odds_l = [h_l1, h_l2, h_l3]
    odds_r = [h_r1, h_r2, h_r3]
    weights = [0.50, 0.25, 0.25]
    
    total_l, total_r = 0.0, 0.0
    row_details = []
    advantage_sides = []

    for i in range(3):
        l, r = odds_l[i], odds_r[i]
        prob_l = (1 / l) * 100 if l > 0 else 0
        prob_r = (1 / r) * 100 if r > 0 else 0
        fair_l = (prob_l / (prob_l + prob_r)) * 100
        fair_r = (prob_r / (prob_l + prob_r)) * 100
        
        # จับแรงเทค่าน้ำ
        b_l = 3.5 if l <= 1.78 else 0.0
        b_r = 3.5 if r <= 1.78 else 0.0
        
        adj_l = fair_l + b_l
        adj_r = fair_r + b_r
        norm_l = (adj_l / (adj_l + adj_r)) * 100
        norm_r = (adj_r / (adj_l + adj_r)) * 100
        
        total_l += norm_l * weights[i]
        total_r += norm_r * weights[i]
        
        adv_name = home_name if norm_l > norm_r else away_name
        advantage_sides.append(adv_name)
        
        row_details.append({
            "rate": rates[i],
            "adv": adv_name,
            "norm_l": norm_l,
            "norm_r": norm_r,
            "diff": abs(norm_l - norm_r)
        })

    # บวกคะแนนปัจจัยเสริม
    if home_name in form_status:
        total_l += 3.0
    elif away_name in form_status:
        total_r += 3.0

    if tier_gap:
        if fav_side == f"{home_name} ต่อ":
            total_l += 4.0
        elif fav_side == f"{away_name} ต่อ":
            total_r += 4.0

    # สรุปทีมชนะราคา
    winner_team = home_name if total_l > total_r else away_name
    total_diff = abs(total_l - total_r)

    # เช็คว่าทั้ง 3 แถวไปทางเดียวกันหมดไหม
    all_same_side = (advantage_sides.count(winner_team) == 3)

    # ฟันธงข้อความ ต่อ หรือ รอง
    if "ต่อ" in fav_side:
        action = f"ต่อ [{winner_team}]" if winner_team in fav_side else f"รอง [{winner_team}]"
    else:
        action = f"วาง [{winner_team}]"

    # ตัดเกรด
    if all_same_side and (tier_gap or total_diff >= 6.0):
        grade = "🟢 เกรด A+ (มั่นใจสูงสุด น้ำเอกฉันท์ + บอลเข้าทาง)"
        status_color = "#238636"
    elif all_same_side or total_diff >= 4.0:
        grade = "🔵 เกรด A (สัญญาณชัด น่าลงทุน)"
        status_color = "#1f6feb"
    elif total_diff >= 2.5:
        grade = "🟡 เกรด B (เล่นได้เฉพาะเต็งเดี่ยว)"
        status_color = "#d29922"
    else:
        grade = "🔴 เกรด C (ราคาก้ำกึ่ง ไม่แนะนำ)"
        status_color = "#f85149"

    # กล่องแสดงผลลัพธ์
    st.subheader("🎯 ชี้เป้าฝั่งที่ได้เปรียบ")
    st.markdown(f"""
        <div style="background-color: #161b22; border-left: 6px solid {status_color}; padding: 16px; border-radius: 8px; margin-bottom: 15px;">
            <h2 style="margin: 0; color: #ffffff;">👉 แนะนำเล่น: <span style="color: #58a6ff;">{action}</span></h2>
            <p style="margin: 8px 0 0 0; color: #8b949e;">สถานะความมั่นใจ: <b style="color: {status_color};">{grade}</b></p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"📌 **เรตที่แนะนำ:** ยึดราคาหลักแถว 1 **({h_rate1})**")

    if all_same_side:
        st.caption("✅ น้ำไหลไปในทิศทางเดียวกันหมดทั้ง 3 แถว ความเสี่ยงต่ำ")
    else:
        st.caption("⚠️ ระวัง: มีราคาแถวรองบางเรตเริ่มสวนทาง ควรคุมเงินให้ดี")

    st.markdown("---")
    st.subheader("📊 เจาะลึกรายแถวราคา")
    for idx, rd in enumerate(row_details):
        st.markdown(f"**แถวที่ {idx+1} [{rd['rate']}]:** {home_name} ({rd['norm_l']:.1f}%) vs {away_name} ({rd['norm_r']:.1f}%)")
        st.caption(f"★ ทิศทางราคาเทไป: {rd['adv']} | ส่วนต่างได้เปรียบ: {rd['diff']:.2f}%")
        

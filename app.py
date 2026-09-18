import streamlit as st

st.set_page_config(
    page_title="Odds Analyzer V10.7 Strict Pro",
    page_icon="⚽",
    layout="centered"
)

# Dark Mode ธีมมืด สบายตา ปุ่มใหญ่จิ้มง่ายบนมือถือ
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

st.title("⚽ ตัวกรองค่าน้ำแฮนดิแคป (V10.7 Strict Pro)")
st.caption("ระบบคัดเกรดเข้มงวด ป้องกันกับดักราคาแตกแถว (Divergence Trap) และคัดเกรด A แบบเอกฉันท์ 3-0")

# ตัวเลือกเรตราคา 0 ถึง 7.0 ลูก
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

# --- 1. ข้อมูลคู่แข่งขัน & ฝั่งต่อ ---
st.subheader("📌 1. คู่แข่งขัน & ฝั่งต่อ")
c1, c2 = st.columns(2)
with c1:
    home_name = st.text_input("ทีมเหย้า (ฝั่งซ้าย)", value="เจ้าบ้าน")
with c2:
    away_name = st.text_input("ทีมเยือน (ฝั่งขวา)", value="ทีมเยือน")

fav_side = st.radio("ทีมที่เป็นฝั่งต่อ:", [f"{home_name} ต่อ", f"{away_name} ต่อ", "ราคาเสมอ"], horizontal=True)

st.markdown("---")

# --- 2. บริบทการแข่งขัน & ระดับชั้น ---
st.subheader("🏆 2. รายการแข่งขัน & ระดับชั้น")
col_m1, col_m2 = st.columns(2)
with col_m1:
    match_type = st.selectbox(
        "ประเภทรายการแข่งขัน:",
        [
            "บอลลีกปกติ (เน้นแต้มเต็มที่)",
            "บอลถ้วยยุโรป (UCL / UEL / UECL)",
            "บอลถ้วยในประเทศ (อาจมีโรเตชั่น/พักตัวหลัก)",
            "กระชับมิตร / บอลอุ่นเครื่อง"
        ]
    )
with col_m2:
    tier_level = st.selectbox(
        "ระดับความต่างชั้นของสองทีม:",
        [
            "ระดับใกล้เคียงกัน / คู่คี่สูสี",
            "ทีมต่อเกรดดีกว่าปานกลาง (กลางตาราง vs ท้ายตาราง)",
            "ต่างชั้นกันชัดเจน (หัวตาราง vs ท้ายตาราง / ต่างลีก)"
        ]
    )

st.markdown("---")

# --- 3. ค่าน้ำ 3 แถวราคา ---
st.subheader("🔢 3. ค่าน้ำและเรตราคา 3 แถว")

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

# --- ประมวลผลและตัดเกรด ---
if st.button("🚀 สรุปผลวิเคราะห์ระดับลึก", use_container_width=True):
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
        
        # ค่าน้ำต่ำกว่า 1.78 ได้โบนัสแรงเท
        b_l = 3.5 if l <= 1.78 else 0.0
        b_r = 3.5 if r <= 1.78 else 0.0
        
        adj_l = fair_l + b_l
        adj_r = fair_r + b_r
        norm_l = (adj_l / (adj_l + adj_r)) * 100
        norm_r = (adj_r / (adj_r + adj_r)) * 100
        
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

    # ปรับค่าน้ำหนักตามบริบท
    context_bias = 0.0
    if "ต่างชั้นกันชัดเจน" in tier_level:
        if "บอลถ้วยในประเทศ" not in match_type:
            context_bias += 4.0
    elif "ทีมต่อเกรดดีกว่าปานกลาง" in tier_level:
        context_bias += 1.5

    if fav_side == f"{home_name} ต่อ":
        total_l += context_bias
    elif fav_side == f"{away_name} ต่อ":
        total_r += context_bias

    winner_team = home_name if total_l > total_r else away_name
    total_diff = abs(total_l - total_r)

    # กำหนดสถานะ ต่อ / รอง
    if "ต่อ" in fav_side:
        action = f"ต่อ [{winner_team}]" if winner_team in fav_side else f"รอง [{winner_team}]"
    else:
        action = f"วาง [{winner_team}]"

    # นับจำนวนแถวที่ชี้ไปแต่ละฝั่ง
    count_winner = advantage_sides.count(winner_team)
    is_unanimous = (count_winner == 3)

    # เช็คว่ามีแถวไหนสวนทางแบบรุนแรงหรือไม่ (Divergence Trap Check)
    has_severe_conflict = False
    for rd in row_details:
        if rd['adv'] != winner_team and rd['diff'] >= 8.0:
            has_severe_conflict = True
            break

    # ระบบตัดเกรดเข้มงวด V10.7
    if has_severe_conflict:
        grade = "🔴 เกรด C- (อันตรายสูงสุด: ราคาแตกแถวรุนแรง โต๊ะวางกับดัก)"
        status_color = "#f85149"
        advice_note = "⚠️ ตลาดค่าน้ำแตกแถวชัดเจน (มีราคาชี้นำสวนทาง) มักมีผลพลิกล็อก ไม่แนะนำให้เล่น"
    elif is_unanimous and ("ต่างชั้นกันชัดเจน" in tier_level or total_diff >= 6.0):
        grade = "🟢 เกรด A+ (มั่นใจสูงสุด: น้ำเอกฉันท์ 3-0 + สภาพทีมหนุน)"
        status_color = "#238636"
        advice_note = "✅ ค่าน้ำทั้ง 3 เรตเทไปทิศทางเดียวกันอย่างแท้จริง ไร้สัญญาณขัดแย้ง"
    elif is_unanimous and total_diff >= 3.5:
        grade = "🔵 เกรด A (สัญญาณเอกฉันท์ 3-0 น้ำหนักทิศทางชัดเจน)"
        status_color = "#1f6feb"
        advice_note = "✅ ผ่านเกณฑ์เอกฉันท์ทั้ง 3 แถวราคา ความเสี่ยงต่ำ"
    elif count_winner == 2:
        grade = "🟡 เกรด B- / C (ราคาแตกแถว 2 ต่อ 1: ความได้เปรียบไม่นิ่ง)"
        status_color = "#d29922"
        advice_note = "⚠️ มีราคา 1 ใน 3 แถวชี้สวนทาง ตลาดเปิดหน้าก้ำกึ่ง ห้ามใส่สเต็ป"
    else:
        grade = "🔴 เกรด C (ราคาก้ำกึ่ง ไร้ทิศทาง)"
        status_color = "#f85149"
        advice_note = "⛔ สัญญาณไม่ชัดเจน แนะนำข้ามไปคัดคู่อื่น"

    # แสดงผล
    st.subheader("🎯 ชี้เป้าฝั่งที่ได้เปรียบ")
    st.markdown(f"""
        <div style="background-color: #161b22; border-left: 6px solid {status_color}; padding: 16px; border-radius: 8px; margin-bottom: 15px;">
            <h2 style="margin: 0; color: #ffffff;">👉 แนะนำเล่น: <span style="color: #58a6ff;">{action}</span></h2>
            <p style="margin: 8px 0 0 0; color: #8b949e;">สถานะความมั่นใจ: <b style="color: {status_color};">{grade}</b></p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"📌 **เรตที่แนะนำ:** ยึดราคาหลักแถว 1 **({h_rate1})**")
    st.info(f"💡 **วิเคราะห์เชิงลึก:** {advice_note}")

    st.markdown("---")
    st.subheader("📊 เจาะลึกรายแถวราคา")
    for idx, rd in enumerate(row_details):
        st.markdown(f"**แถวที่ {idx+1} [{rd['rate']}]:** {home_name} ({rd['norm_l']:.1f}%) vs {away_name} ({rd['norm_r']:.1f}%)")
        st.caption(f"★ ทิศทางราคาเทไป: {rd['adv']} | ส่วนต่างได้เปรียบ: {rd['diff']:.2f}%")
        

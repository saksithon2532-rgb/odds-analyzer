import streamlit as st

st.set_page_config(
    page_title="Odds Analyzer V10.2 Pro Plus",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ธีมสีดำสนิทระดับพรีเมียม สบายตา ตัวหนังสือคมชัด เหมาะกับมือถือ
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0e14;
        color: #e6edf3;
    }
    h1, h2, h3, h4, p, span, label {
        color: #f0f6fc !important;
    }
    /* ปรับช่องกรอกตัวเลขและ Selectbox ให้ใหญ่ กดง่ายบนมือถือ */
    .stTextInput input, .stNumberInput input, div[data-baseweb="select"] {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        font-size: 1.05rem !important;
        padding: 8px !important;
    }
    div[data-baseweb="popover"] ul {
        background-color: #161b22 !important;
        color: #ffffff !important;
    }
    /* ปุ่มกดวิเคราะห์เด่นชัด สัมผัสง่าย */
    .stButton > button {
        background: linear-gradient(135deg, #1f6feb 0%, #238636 100%) !important;
        color: #ffffff !important;
        font-size: 1.15rem !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 20px !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.6) !important;
        transition: 0.2s all ease-in-out !important;
    }
    .stButton > button:active {
        transform: scale(0.98);
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ คัดกรองค่าน้ำแฮนดิแคป (V10.2 Pro Plus)")
st.caption("ระบบวิเคราะห์ค่าน้ำ 3 แถวราคา พร้อมอัลกอริทึมจับสัญญาณไหลและเช็คความสอดคล้อง")

# ตัวเลือกราคาต่อรองขยายจุใจ 0 ถึง 7.0 ลูก
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

# แถวที่ 1 (แถวหลัก 50%)
st.markdown("🔹 **แถวที่ 1 (ราคาเปิดหลัก - น้ำหนัก 50%)**")
h_rate1 = st.selectbox("เรตแต้มต่อ แถว 1", HDP_OPTIONS, index=3, key="h_rate1")
col1_l, col1_r = st.columns(2)
with col1_l:
    h_l1 = st.number_input(f"น้ำ {home_name} (1)", value=1.85, step=0.01, format="%.2f", key="hl1")
with col1_r:
    h_r1 = st.number_input(f"น้ำ {away_name} (1)", value=2.05, step=0.01, format="%.2f", key="hr1")

# แถวที่ 2 (แถวรอง 1 - น้ำหนัก 25%)
st.markdown("🔹 **แถวที่ 2 (ราคารอง 1 - น้ำหนัก 25%)**")
h_rate2 = st.selectbox("เรตแต้มต่อ แถว 2", HDP_OPTIONS, index=4, key="h_rate2")
col2_l, col2_r = st.columns(2)
with col2_l:
    h_l2 = st.number_input(f"น้ำ {home_name} (2)", value=2.18, step=0.01, format="%.2f", key="hl2")
with col2_r:
    h_r2 = st.number_input(f"น้ำ {away_name} (2)", value=1.75, step=0.01, format="%.2f", key="hr2")

# แถวที่ 3 (แถวรอง 2 - น้ำหนัก 25%)
st.markdown("🔹 **แถวที่ 3 (ราคารอง 2 - น้ำหนัก 25%)**")
h_rate3 = st.selectbox("เรตแต้มต่อ แถว 3", HDP_OPTIONS, index=2, key="h_rate3")
col3_l, col3_r = st.columns(2)
with col3_l:
    h_l3 = st.number_input(f"น้ำ {home_name} (3)", value=1.65, step=0.01, format="%.2f", key="hl3")
with col3_r:
    h_r3 = st.number_input(f"น้ำ {away_name} (3)", value=2.35, step=0.01, format="%.2f", key="hr3")

st.markdown("---")

# --- ปุ่มคำนวณและประมวลผล ---
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
        
        # ปรับความคม: ดักจับ Juice Flow Trap (น้ำต่ำกว่า 1.78 ได้โบนัสสะท้อนแรงเท)
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
        
        diff = abs(norm_l - norm_r)
        row_details.append({
            "rate": rates[i],
            "adv": adv_name,
            "norm_l": norm_l,
            "norm_r": norm_r,
            "diff": diff
        })

    # สรุปทีมที่ได้เปรียบ
    is_home_better = total_l > total_r
    winner_team = home_name if is_home_better else away_name
    total_diff = abs(total_l - total_r)

    # เช็คความสอดคล้อง 3 แถว (Consensus Check) เพื่อดันเกรดแม่นยำ
    all_same_side = (advantage_sides.count(winner_team) == 3)
    main_row_match = (advantage_sides[0] == winner_team)

    # กำหนดสถานะความมั่นใจ
    if all_same_side and total_diff >= 5.0:
        grade = "เกรด A+ (มั่นใจสูงสุด ทิศทางน้ำเป็นเอกฉันท์ทั้ง 3 แถว)"
        status_color = "#238636"
        sub_badge = "🟢 เกรด A+ (แนะนำเน้นตัวนี้)"
    elif main_row_match and total_diff >= 3.5:
        grade = "เกรด B (น่าลงทุน ราคาหลักไหลตามทิศทาง)"
        status_color = "#1f6feb"
        sub_badge = "🔵 เกรด B (น่าลงทุนเดี่ยว)"
    else:
        grade = "เกรด C (ราคาก้ำกึ่งหรือมีแถวขัดแย้ง)"
        status_color = "#d29922"
        sub_badge = "🟡 เกรด C (เล่นเบาๆ หรือหลีกเลี่ยง)"

    # กล่องผลลัพธ์แบบ V10.2 ดั้งเดิม
    st.subheader("🎯 ชี้เป้าฝั่งที่ได้เปรียบ")
    
    st.markdown(f"""
        <div style="background-color: #161b22; border-left: 6px solid {status_color}; padding: 16px; border-radius: 8px; margin-bottom: 15px;">
            <h2 style="margin: 0; color: #ffffff;">👉 แนะนำเล่น: <span style="color: #58a6ff;">[{winner_team}]</span></h2>
            <p style="margin: 8px 0 0 0; color: #8b949e;">สถานะความมั่นใจ: <b style="color: {status_color};">{sub_badge}</b></p>
        </div>
    """, unsafe_allow_html=True)

    # แนะนำเรตราคาที่ได้เปรียบ
    st.markdown(f"📌 **เรตที่แนะนำ:** ยึดราคาหลักแถว 1 **({h_rate1})** หรือเลือกเรตที่ได้แต้มต่อที่ดีที่สุด")
    
    if all_same_side:
        st.caption("✅ การเทน้ำไหลไปในทิศทางเดียวกันหมดทั้ง 3 แถว ได้เปรียบความเสี่ยงต่ำ เหมาะทั้งบอลเต็งและสเต็ป")
    else:
        st.caption("⚠️ ระวัง: มีราคาแถวรองบางเรตเริ่มบาลานซ์สวนทาง หากแทงให้คุมเงินอย่างรัดกุม")

    st.markdown("---")
    
    # เจาะลึกรายแถวราคาแบบละเอียด
    st.subheader("📊 เจาะลึกรายแถวราคา")
    for idx, rd in enumerate(row_details):
        star_txt = "★ ทิศทางราคาเทไป:"
        warn_txt = " ⚠️ ได้เปรียบน้ำแถวผิดปกติ" if rd['diff'] > 8.0 else ""
        st.markdown(f"**แถวที่ {idx+1} [{rd['rate']}]:** {home_name} ({rd['norm_l']:.1f}%) vs {away_name} ({rd['norm_r']:.1f}%)")
        st.caption(f"{star_txt} {rd['adv']} | ส่วนต่างได้เปรียบ: {rd['diff']:.2f}%{warn_txt}")

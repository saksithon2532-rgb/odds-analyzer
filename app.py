import streamlit as st

st.set_page_config(
    page_title="Odds Analyzer V10.4 Smart Pro",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Dark Mode ธีมมืดพรีเมียม สบายตา กดง่ายบนมือถือ
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
        font-size: 1.0rem !important;
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

st.title("⚽ ตัวกรองค่าน้ำ + ปัจจัยเกมจริง (V10.4)")
st.caption("ระบบผสานค่าน้ำ 3 แถว เข้ากับตัวแปรฟอร์ม ตัวผู้เล่น และแรงจูงใจ เพื่อคัดเกรด A+ ที่แม่นยำที่สุด")

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

# --- ส่วนที่ 1: คู่แข่งขัน ---
st.subheader("📌 1. คู่แข่งขัน")
c1, c2 = st.columns(2)
with c1:
    home_name = st.text_input("ทีมเหย้า (ฝั่งซ้าย)", value="เจ้าบ้าน")
with c2:
    away_name = st.text_input("ทีมเยือน (ฝั่งขวา)", value="ทีมเยือน")

st.markdown("---")

# --- ส่วนที่ 2: ค่าน้ำ 3 แถว ---
st.subheader("🔢 2. ค่าน้ำและเรตราคา 3 แถว")
h_rate1 = st.selectbox("เรตแต้มต่อ แถว 1 (ราคาหลัก)", HDP_OPTIONS, index=3, key="h_rate1")
col1_l, col1_r = st.columns(2)
with col1_l:
    h_l1 = st.number_input(f"น้ำ {home_name} (1)", value=1.85, step=0.01, format="%.2f")
with col1_r:
    h_r1 = st.number_input(f"น้ำ {away_name} (1)", value=2.05, step=0.01, format="%.2f")

h_rate2 = st.selectbox("เรตแต้มต่อ แถว 2 (ราคารอง 1)", HDP_OPTIONS, index=4, key="h_rate2")
col2_l, col2_r = st.columns(2)
with col2_l:
    h_l2 = st.number_input(f"น้ำ {home_name} (2)", value=2.18, step=0.01, format="%.2f")
with col2_r:
    h_r2 = st.number_input(f"น้ำ {away_name} (2)", value=1.75, step=0.01, format="%.2f")

h_rate3 = st.selectbox("เรตแต้มต่อ แถว 3 (ราคารอง 2)", HDP_OPTIONS, index=2, key="h_rate3")
col3_l, col3_r = st.columns(2)
with col3_l:
    h_l3 = st.number_input(f"น้ำ {home_name} (3)", value=1.65, step=0.01, format="%.2f")
with col3_r:
    h_r3 = st.number_input(f"น้ำ {away_name} (3)", value=2.35, step=0.01, format="%.2f")

st.markdown("---")

# --- ส่วนที่ 3: ปัจจัยเสริมหน้างาน (ติ๊กง่ายๆ ไม่เสียเวลา) ---
st.subheader("📋 3. ปัจจัยหน้างานจริง (Quick Factors)")
st.caption("ติ๊กเฉพาะข้อที่มีข้อมูลชัดเจน เพื่อยกระดับความแม่นยำ")

f_home_form = st.checkbox(f"🔥 {home_name} ฟอร์มแรงชัดเจน (ชนะ 3 นัดติด หรือยิงขาดลอย)")
f_home_squad = st.checkbox(f"✅ {home_name} ขุมกำลังสมบูรณ์ ตัวหลักลงครบ ไม่โรเตชั่น")
f_away_missing = st.checkbox(f"⚠️ {away_name} มีปัญหาตัวหลักเจ็บ/แบนสำคัญ หรือพักน้อยกว่า")
f_h2h_home = st.checkbox(f"📊 สถิติ H2H ทางบอลข่มชัดเจน ({home_name} ชนะทาง)")

st.markdown("---")

if st.button("🚀 สรุปผลวิเคราะห์ระดับลึก", use_container_width=True):
    rates = [h_rate1, h_rate2, h_rate3]
    odds_l = [h_l1, h_l2, h_l3]
    odds_r = [h_r1, h_r2, h_r3]
    weights = [0.50, 0.25, 0.25]
    
    total_l, total_r = 0.0, 0.0
    advantage_sides = []

    for i in range(3):
        l, r = odds_l[i], odds_r[i]
        prob_l = (1 / l) * 100 if l > 0 else 0
        prob_r = (1 / r) * 100 if r > 0 else 0
        fair_l = (prob_l / (prob_l + prob_r)) * 100
        fair_r = (prob_r / (prob_l + prob_r)) * 100
        
        b_l = 3.5 if l <= 1.78 else 0.0
        b_r = 3.5 if r <= 1.78 else 0.0
        
        adj_l = fair_l + b_l
        adj_r = fair_r + b_r
        norm_l = (adj_l / (adj_l + adj_r)) * 100
        norm_r = (adj_r / (adj_l + adj_r)) * 100
        
        total_l += norm_l * weights[i]
        total_r += norm_r * weights[i]
        
        advantage_sides.append(home_name if norm_l > norm_r else away_name)

    # คะแนนเสริมจากปัจจัยจริง (Context Bonus)
    factor_score_home = 0
    if f_home_form: factor_score_home += 1
    if f_home_squad: factor_score_home += 1
    if f_away_missing: factor_score_home += 1
    if f_h2h_home: factor_score_home += 1

    # ปรับแต้มได้เปรียบด้วยปัจจัยเสริม
    adj_total_l = total_l + (factor_score_home * 1.5)
    winner_team = home_name if adj_total_l > total_r else away_name
    total_diff = abs(adj_total_l - total_r)

    all_same_side = (advantage_sides.count(winner_team) == 3)

    # ระบบคัดเกรดอัจฉริยะ (Smart Grade)
    if all_same_side and factor_score_home >= 2 and winner_team == home_name:
        grade_text = "🟢 เกรด A+ (Super Match: ค่าน้ำเอกฉันท์ + ปัจจัยฟุตบอลหนุนเต็มตัว)"
        status_color = "#238636"
    elif all_same_side or (factor_score_home >= 2 and total_diff >= 4.0):
        grade_text = "🔵 เกรด A (สัญญาณค่อนข้างชัด มีความน่าลงทุนสูง)"
        status_color = "#1f6feb"
    elif total_diff >= 3.0:
        grade_text = "🟡 เกรด B (ลงทุนเฉพาะเต็งเดี่ยว คุมเงินรัดกุม)"
        status_color = "#d29922"
    else:
        grade_text = "🔴 เกรด C (ราคาก้ำกึ่งหรือมีจุดเสี่ยง ไม่แนะนำเล่น)"
        status_color = "#f85149"

    st.subheader("🎯 สรุปการชี้เป้าแม่นยำพิเศษ")
    st.markdown(f"""
        <div style="background-color: #161b22; border-left: 6px solid {status_color}; padding: 16px; border-radius: 8px; margin-bottom: 15px;">
            <h2 style="margin: 0; color: #ffffff;">👉 แนะนำเล่น: <span style="color: #58a6ff;">[{winner_team}]</span></h2>
            <p style="margin: 8px 0 0 0; color: #8b949e;">ระดับความมั่นใจ: <b style="color: {status_color};">{grade_text}</b></p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"📌 **เรตที่แนะนำ:** ยึดราคาหลักแถว 1 **({h_rate1})**")
    
    if factor_score_home >= 2:
        st.info(f"💡 **วิเคราะห์เชิงลึก:** มีปัจจัยบวกเกื้อหนุนถึง {factor_score_home} ข้อ ขุมกำลังและฟอร์มมีความพร้อมสูง ช่วยปิดความเสี่ยงเรื่องราคาต่อลึกได้ดีเยี่ยม")
    elif factor_score_home == 0 and total_diff < 3.0:
        st.warning("⚠️ **ข้อควรระวัง:** ไม่มีปัจจัยฟอร์มสนับสนุนและค่าน้ำยังก้ำกึ่ง หลีกเลี่ยงการใส่บิลสเต็ป")
        

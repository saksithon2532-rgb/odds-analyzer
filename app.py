import streamlit as st

st.set_page_config(
    page_title="Odds Analyzer V11 Pro Multi-Side",
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

st.title("⚽ ตัวกรองค่าน้ำแฮนดิแคป (V11 Pro Multi-Side)")
st.caption("รองรับราคาสลับฝั่งต่อรายแถว ตรวจจับตลาดขัดแย้ง และป้องกันกับดักราคาโต๊ะล่อ")

HDP_OPTIONS = [
    "เสมอ (0)", "0-0.5 (เสมอควบครึ่ง)", "0.5 (ครึ่งลูก)", "0.5-1 (ครึ่งควบลูก)",
    "1.0 (หนึ่งลูก)", "1-1.5 (ลูกควบลูกครึ่ง)", "1.5 (ลูกครึ่ง)", "1.5-2 (ลูกครึ่งควบสอง)",
    "2.0 (สองลูก)", "2-2.5 (สองควบสองครึ่ง)", "2.5 (สองลูกครึ่ง)", "2.5-3 (สองครึ่งควบสาม)",
    "3.0 (สามลูก)"
]

def parse_hdp_val(h_str):
    if "0-0.5" in h_str: return 0.25
    if "0.5-1" in h_str: return 0.75
    if "1-1.5" in h_str: return 1.25
    if "1.5-2" in h_str: return 1.75
    if "2-2.5" in h_str: return 2.25
    if "2.5-3" in h_str: return 2.75
    if "0.5" in h_str: return 0.5
    if "1.0" in h_str: return 1.0
    if "1.5" in h_str: return 1.5
    if "2.0" in h_str: return 2.0
    if "2.5" in h_str: return 2.5
    if "3.0" in h_str: return 3.0
    return 0.0

# --- 1. ข้อมูลคู่แข่งขัน ---
st.subheader("📌 1. ระบุชื่อทีม (หรือไม่ใส่ก็ได้)")
c1, c2 = st.columns(2)
with c1:
    home_name = st.text_input("ทีมเหย้า (ฝั่งซ้าย)", value="เบรนท์ฟอร์ด")
with c2:
    away_name = st.text_input("ทีมเยือน (ฝั่งขวา)", value="เชลซี")

st.markdown("---")

# --- 2. บริบทการแข่งขัน ---
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
            "ทีมเยือน/เจ้าบ้านเกรดดีกว่าปานกลาง",
            "ต่างชั้นกันชัดเจน (หัวตาราง vs ท้ายตาราง / ต่างลีก)"
        ]
    )

st.markdown("---")

# --- 3. ค่าน้ำ 3 แถวราคา (แยกฝั่งต่ออิสระ) ---
st.subheader("🔢 3. ค่าน้ำและเรตราคา 3 แถว (เลือกฝั่งต่อแยกแถวได้)")

# แถวที่ 1
st.markdown("🔹 **แถวที่ 1 (น้ำหนัก 50%)**")
col1_side, col1_rate = st.columns(2)
with col1_side:
    side1 = st.selectbox("ฝั่งต่อ แถว 1", ["ราคาเสมอ (0)", f"{home_name} ต่อ", f"{away_name} ต่อ"], index=0, key="side1")
with col1_rate:
    h_rate1 = st.selectbox("แต้มต่อ แถว 1", HDP_OPTIONS, index=0, key="h_rate1")
col1_l, col1_r = st.columns(2)
with col1_l:
    h_l1 = st.number_input(f"น้ำ {home_name} (1)", value=2.06, step=0.01, format="%.2f", key="hl1")
with col1_r:
    h_r1 = st.number_input(f"น้ำ {away_name} (1)", value=1.85, step=0.01, format="%.2f", key="hr1")

# แถวที่ 2
st.markdown("🔹 **แถวที่ 2 (น้ำหนัก 25%)**")
col2_side, col2_rate = st.columns(2)
with col2_side:
    side2 = st.selectbox("ฝั่งต่อ แถว 2", ["ราคาเสมอ (0)", f"{home_name} ต่อ", f"{away_name} ต่อ"], index=2, key="side2")
with col2_rate:
    h_rate2 = st.selectbox("แต้มต่อ แถว 2", HDP_OPTIONS, index=1, key="h_rate2")
col2_l, col2_r = st.columns(2)
with col2_l:
    h_l2 = st.number_input(f"น้ำ {home_name} (2)", value=1.77, step=0.01, format="%.2f", key="hl2")
with col2_r:
    h_r2 = st.number_input(f"น้ำ {away_name} (2)", value=2.16, step=0.01, format="%.2f", key="hr2")

# แถวที่ 3
st.markdown("🔹 **แถวที่ 3 (น้ำหนัก 25%)**")
col3_side, col3_rate = st.columns(2)
with col3_side:
    side3 = st.selectbox("ฝั่งต่อ แถว 3", ["ราคาเสมอ (0)", f"{home_name} ต่อ", f"{away_name} ต่อ"], index=1, key="side3")
with col3_rate:
    h_rate3 = st.selectbox("แต้มต่อ แถว 3", HDP_OPTIONS, index=1, key="h_rate3")
col3_l, col3_r = st.columns(2)
with col3_l:
    h_l3 = st.number_input(f"น้ำ {home_name} (3)", value=2.41, step=0.01, format="%.2f", key="hl3")
with col3_r:
    h_r3 = st.number_input(f"น้ำ {away_name} (3)", value=1.62, step=0.01, format="%.2f", key="hr3")

st.markdown("---")

# --- ประมวลผล ---
if st.button("🚀 สรุปผลวิเคราะห์ระดับลึก", use_container_width=True):
    sides = [side1, side2, side3]
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
        
        desc = f"{sides[i]} [{rates[i]}]"
        row_details.append({
            "desc": desc,
            "adv": adv_name,
            "norm_l": norm_l,
            "norm_r": norm_r,
            "diff": abs(norm_l - norm_r)
        })

    winner_team = home_name if total_l > total_r else away_name
    total_diff = abs(total_l - total_r)

    count_winner = advantage_sides.count(winner_team)
    is_unanimous = (count_winner == 3)

    # ตรวจสอบการแตกแถวอย่างรุนแรง
    has_severe_conflict = False
    for rd in row_details:
        if rd['adv'] != winner_team and rd['diff'] >= 8.0:
            has_severe_conflict = True
            break

    # ตรวจจับราคาสลับฝั่งต่อ
    has_mixed_favorites = (f"{home_name} ต่อ" in sides and f"{away_name} ต่อ" in sides)

    # ตัดเกรด
    if has_mixed_favorites:
        grade = "🟡 เกรด B- (ราคาสลับฝั่งต่อ: โต๊ะมองคู่คี่สูสีมาก ระวังบอลออก 3 หน้า)"
        status_color = "#d29922"
        action = f"วาง [{winner_team}]"
        advice_note = "⚠️ มีทั้งราคาที่เจ้าบ้านต่อและเยือนต่อ บ่งชี้ว่าโอกาสออกได้ทั้งสามหน้า เลี่ยงบิลสเต็ปเด็ดขาด"
    elif has_severe_conflict:
        grade = "🔴 เกรด C- (อันตรายสูงสุด: ราคาแตกแถวรุนแรง โต๊ะวางกับดัก)"
        status_color = "#f85149"
        action = f"เสี่ยงวาง [{winner_team}]"
        advice_note = "⚠️ มีราคาชี้นำสวนทางอย่างรุนแรง ไม่แนะนำให้ลงทุน"
    elif is_unanimous and total_diff >= 4.0:
        grade = "🟢 เกรด A+ (มั่นใจสูงสุด: น้ำเอกฉันท์ 3-0)"
        status_color = "#238636"
        action = f"วาง [{winner_team}]"
        advice_note = "✅ ค่าน้ำทั้ง 3 เรตเทไปทิศทางเดียวกันอย่างแท้จริง ไร้สัญญาณขัดแย้ง"
    elif is_unanimous:
        grade = "🔵 เกรด A (สัญญาณเอกฉันท์ 3-0)"
        status_color = "#1f6feb"
        action = f"วาง [{winner_team}]"
        advice_note = "✅ ผ่านเกณฑ์เอกฉันท์ ความเสี่ยงต่ำ"
    else:
        grade = "🟡 เกรด B- / C (ราคาแตกแถว 2 ต่อ 1)"
        status_color = "#d29922"
        action = f"วาง [{winner_team}]"
        advice_note = "⚠️ ค่าน้ำยังไม่นิ่ง มีบางราคาชี้สวนทาง"

    # แสดงผล
    st.subheader("🎯 ชี้เป้าฝั่งที่ได้เปรียบ")
    st.markdown(f"""
        <div style="background-color: #161b22; border-left: 6px solid {status_color}; padding: 16px; border-radius: 8px; margin-bottom: 15px;">
            <h2 style="margin: 0; color: #ffffff;">👉 แนะนำ: <span style="color: #58a6ff;">{action}</span></h2>
            <p style="margin: 8px 0 0 0; color: #8b949e;">สถานะความมั่นใจ: <b style="color: {status_color};">{grade}</b></p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"📌 **เรตที่แนะนำ:** ยึดราคาเปิดหลักแถว 1 **({sides[0]} - {rates[0]})**")
    st.info(f"💡 **วิเคราะห์เชิงลึก:** {advice_note}")

    st.markdown("---")
    st.subheader("📊 เจาะลึกรายแถวราคา")
    for idx, rd in enumerate(row_details):
        st.markdown(f"**แถวที่ {idx+1} [{rd['desc']}]:** {home_name} ({rd['norm_l']:.1f}%) vs {away_name} ({rd['norm_r']:.1f}%)")
        st.caption(f"★ ทิศทางราคาเทไป: {rd['adv']} | ส่วนต่างได้เปรียบ: {rd['diff']:.2f}%")
    

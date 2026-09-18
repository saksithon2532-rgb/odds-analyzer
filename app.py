import streamlit as st

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="เครื่องมือวิเคราะห์แฮนดิแคป",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Dark Mode CSS แบบครบทุกจุด
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117 !important;
        color: #c9d1d9 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #f0f6fc !important;
    }
    input[type="text"], input[type="number"] {
        background-color: #161b22 !important;
        color: #58a6ff !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    input:focus {
        border-color: #58a6ff !important;
        box-shadow: 0 0 0 1px #58a6ff !important;
    }
    button[data-testid="stNumberInputStepDown"], 
    button[data-testid="stNumberInputStepUp"] {
        background-color: #21262d !important;
        color: #c9d1d9 !important;
        border-color: #30363d !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #161b22 !important;
        color: #f0f6fc !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="popover"] ul {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
    }
    div[data-baseweb="popover"] li {
        color: #f0f6fc !important;
    }
    div[data-baseweb="popover"] li:hover {
        background-color: #21262d !important;
    }
    hr {
        border-color: #21262d !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
    }
    div.stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        color: #ffffff !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        border: 1px solid rgba(240, 246, 252, 0.1) !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #2ea043 0%, #3fb950 100%) !important;
        box-shadow: 0 4px 16px rgba(46, 160, 67, 0.4) !important;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ เครื่องมือวิเคราะห์บอล: แฮนดิแคป")
st.caption("ระบบคำนวณค่าน้ำ ป้องกันกับดักราคา และประเมินเกรดความน่าลงทุน")

# ฟังก์ชันแปลงค่าแต้มต่อ
def parse_hdp_val(rate_str):
    if not rate_str or rate_str == "0":
        return 0.0
    mapping = {
        "0": 0.0,
        "0-0.5": 0.25,
        "0.5": 0.5,
        "0.5-1": 0.75,
        "1.0": 1.0,
        "1-1.5": 1.25,
        "1.5": 1.5,
        "1.5-2": 1.75,
        "2.0": 2.0,
        "2-2.5": 2.25,
        "2.5": 2.5,
        "2.5-3": 2.75,
        "3.0": 3.0,
        "3-3.5": 3.25,
        "3.5": 3.5
    }
    for k, v in mapping.items():
        if k in rate_str:
            return v
    return 0.0

def calc_row_probs(odd1, odd2, t1_name, t2_name):
    raw_p1 = 1.0 / odd1
    raw_p2 = 1.0 / odd2
    total_m = raw_p1 + raw_p2
    p1 = (raw_p1 / total_m) * 100.0
    p2 = (raw_p2 / total_m) * 100.0

    if odd1 <= 1.75:
        p1 += 3.5
        p2 -= 3.5
    elif odd2 <= 1.75:
        p2 += 3.5
        p1 -= 3.5

    adv = t1_name if p1 > p2 else t2_name
    diff = abs(p1 - p2)
    return p1, p2, adv, diff

# ส่วนที่ 1: ข้อมูลทีม
st.subheader("📌 1. ระบุชื่อทีม")
c_t1, c_t2 = st.columns(2)
with c_t1:
    team1_name = st.text_input("ทีมเหย้า [1]", value="เจ้าบ้าน")
with c_t2:
    team2_name = st.text_input("ทีมเยือน [2]", value="ทีมเยือน")

side_options = [f"{team1_name} ต่อ", f"{team2_name} ต่อ", "เสมอ (0)"]
hdp_rate_options = [
    "0", "0-0.5", "0.5", "0.5-1", "1.0", "1-1.5", 
    "1.5", "1.5-2", "2.0", "2-2.5", "2.5", "2.5-3", "3.0", "3-3.5", "3.5"
]

st.divider()

# ส่วนที่ 2: เลือกโหมดราคา (1, 2 หรือ 3 ราคา)
st.subheader("⚙️ 2. เลือกจำนวนราคาที่ต้องการวิเคราะห์")
mode = st.radio(
    "จำนวนราคา:",
    ("1 ราคา (ราคาเดียว / ราคาเปิดหลัก)", "2 ราคา (ราคาหลัก + ราคาสำรอง)", "3 ราคา (เจาะลึก 3 แถวราคา)"),
    horizontal=True,
    index=2
)

st.divider()

# ส่วนที่ 3: แบบฟอร์มกรอกราคาตามโหมด
st.subheader("🔢 3. ค่าน้ำและเรตราคาต่อรอง")

# แถวที่ 1 (แสดงทุกโหมด)
st.markdown("🔹 **แถวที่ 1 (ราคาเปิดหลัก)**")
col_f1, col_r1 = st.columns(2)
with col_f1:
    side1 = st.selectbox("ฝั่งต่อ แถว 1", side_options, index=0, key="side1")
with col_r1:
    rate1 = st.selectbox("แต้มต่อ แถว 1", hdp_rate_options, index=4, key="rate1")

col_o1_1, col_o1_2 = st.columns(2)
with col_o1_1:
    o1_1 = st.number_input(f"น้ำ {team1_name} (1)", min_value=1.0, max_value=5.0, value=1.88, step=0.01, key="o1_1")
with col_o1_2:
    o1_2 = st.number_input(f"น้ำ {team2_name} (1)", min_value=1.0, max_value=5.0, value=1.99, step=0.01, key="o1_2")

# แถวที่ 2 (แสดงในโหมด 2 ราคา และ 3 ราคา)
if mode in ["2 ราคา (ราคาหลัก + ราคาสำรอง)", "3 ราคา (เจาะลึก 3 แถวราคา)"]:
    weight_text_2 = "น้ำหนัก 35%" if mode == "2 ราคา (ราคาหลัก + ราคาสำรอง)" else "น้ำหนัก 25%"
    st.markdown(f"🔹 **แถวที่ 2 ({weight_text_2})**")
    col_f2, col_r2 = st.columns(2)
    with col_f2:
        side2 = st.selectbox("ฝั่งต่อ แถว 2", side_options, index=0, key="side2")
    with col_r2:
        rate2 = st.selectbox("แต้มต่อ แถว 2", hdp_rate_options, index=5, key="rate2")

    col_o2_1, col_o2_2 = st.columns(2)
    with col_o2_1:
        o2_1 = st.number_input(f"น้ำ {team1_name} (2)", min_value=1.0, max_value=5.0, value=2.15, step=0.01, key="o2_1")
    with col_o2_2:
        o2_2 = st.number_input(f"น้ำ {team2_name} (2)", min_value=1.0, max_value=5.0, value=1.74, step=0.01, key="o2_2")

# แถวที่ 3 (แสดงเฉพาะโหมด 3 ราคา)
if mode == "3 ราคา (เจาะลึก 3 แถวราคา)":
    st.markdown("🔹 **แถวที่ 3 (น้ำหนัก 25%)**")
    col_f3, col_r3 = st.columns(2)
    with col_f3:
        side3 = st.selectbox("ฝั่งต่อ แถว 3", side_options, index=0, key="side3")
    with col_r3:
        rate3 = st.selectbox("แต้มต่อ แถว 3", hdp_rate_options, index=3, key="rate3")

    col_o3_1, col_o3_2 = st.columns(2)
    with col_o3_1:
        o3_1 = st.number_input(f"น้ำ {team1_name} (3)", min_value=1.0, max_value=5.0, value=1.69, step=0.01, key="o3_1")
    with col_o3_2:
        o3_2 = st.number_input(f"น้ำ {team2_name} (3)", min_value=1.0, max_value=5.0, value=2.22, step=0.01, key="o3_2")

st.divider()

# ประมวลผล
if st.button("🚀 ประมวลผลและชี้เป้าทีเด็ด", type="primary", use_container_width=True):
    if mode == "1 ราคา (ราคาเดียว / ราคาเปิดหลัก)":
        p1, p2, adv, diff = calc_row_probs(o1_1, o1_2, team1_name, team2_name)
        winner_team = adv
        abs_hdp = parse_hdp_val(rate1)

        if abs_hdp >= 1.75 and "ต่อ" in side1:
            grade = "เกรด C- (อันตราย: กับดักบอลต่อลึกเกิน 1.75 ลูก)"
            grade_color = "red"
            advice = f"เลี่ยงวางฝั่งต่อ หรือ พิจารณารองอีกฝั่ง"
            analysis_note = "⚠️ ต่อลึกมาก มีโอกาสชนะในสนามแต่เสี่ยงแพ้ราคาต่อรอง"
        elif diff >= 8.0:
            grade = "เกรด A+ (ความมั่นใจสูงสุด: ค่าน้ำเทขาด)"
            grade_color = "green"
            advice = f"วาง [{winner_team}]"
            analysis_note = f"✨ ค่าน้ำได้เปรียบชัดเจน ส่วนต่างความได้เปรียบสูงถึง {diff:.2f}%"
        elif diff >= 4.0:
            grade = "เกรด A (น่าลงทุน: ทิศทางราคาได้เปรียบ)"
            grade_color = "blue"
            advice = f"วาง [{winner_team}]"
            analysis_note = f"✅ ค่าน้ำมีความได้เปรียบมากกว่าอย่างมีนัยสำคัญ ({diff:.2f}%)"
        else:
            grade = "เกรด B (ปานกลาง: ค่าน้ำสูสี)"
            grade_color = "gray"
            advice = f"พิจารณา [{winner_team}] หรือเลี่ยงสเต็ป"
            analysis_note = "ℹ️ ค่าน้ำสองฝั่งใกล้เคียงกัน ความได้เปรียบไม่ขาด"

        st.subheader("🎯 ชี้เป้าฝั่งที่ได้เปรียบ (โหมด 1 ราคา)")
        with st.container(border=True):
            st.markdown(f"### 👉 แนะนำ: **{advice}**")
            if grade_color == "green":
                st.success(f"**สถานะความมั่นใจ:** 🟢 {grade}")
            elif grade_color == "blue":
                st.info(f"**สถานะความมั่นใจ:** 🔵 {grade}")
            elif grade_color == "red":
                st.error(f"**สถานะความมั่นใจ:** 🔴 {grade}")
            else:
                st.write(f"**สถานะความมั่นใจ:** ⚪ {grade}")

            st.write(f"📌 **เรตที่แนะนำ:** ยึดราคา {side1} - {rate1}")
            st.caption(f"💡 **วิเคราะห์เชิงลึก:** {analysis_note}")

        st.subheader("📊 เจาะลึกความน่าจะเป็น")
        st.write(f"• **{team1_name}:** `{p1:.1f}%` (น้ำ {o1_1}) | **{team2_name}:** `{p2:.1f}%` (น้ำ {o1_2})")
        st.caption(f"★ ทิศทางราคาเทไป: {adv} | ส่วนต่างความได้เปรียบ: {diff:.2f}%")

    else:
        # กำหนดพารามิเตอร์สำหรับ 2 ราคา หรือ 3 ราคา
        if mode == "2 ราคา (ราคาหลัก + ราคาสำรอง)":
            num_rows = 2
            weights = [0.65, 0.35]
            odds = [(o1_1, o1_2), (o2_1, o2_2)]
            rates = [rate1, rate2]
            sides = [side1, side2]
        else:
            num_rows = 3
            weights = [0.50, 0.25, 0.25]
            odds = [(o1_1, o1_2), (o2_1, o2_2), (o3_1, o3_2)]
            rates = [rate1, rate2, rate3]
            sides = [side1, side2, side3]

        hdp_numeric = [parse_hdp_val(r) for r in rates]
        row_details = []
        
        for i in range(num_rows):
            p1, p2, adv, diff = calc_row_probs(odds[i][0], odds[i][1], team1_name, team2_name)
            row_details.append({
                "p1": p1, "p2": p2, "adv": adv, "diff": diff,
                "rate": rates[i], "side": sides[i]
            })

        w_p1_total = 0.0
        w_p2_total = 0.0
        
        for i in range(num_rows):
            p1_val = row_details[i]["p1"]
            p2_val = row_details[i]["p2"]
            
            # ข้ามแถวที่ต่อลึกขึ้นแล้วน้ำล้นตามธรรมชาติ
            if hdp_numeric[i] > hdp_numeric[0] and "ต่อ" in sides[i]:
                if sides[i] == f"{team1_name} ต่อ" and p1_val < 50.0:
                    p1_val = 50.0
                    p2_val = 50.0
                elif sides[i] == f"{team2_name} ต่อ" and p2_val < 50.0:
                    p1_val = 50.0
                    p2_val = 50.0
                    
            w_p1_total += p1_val * weights[i]
            w_p2_total += p2_val * weights[i]

        winner_team = team1_name if w_p1_total > w_p2_total else team2_name
        final_win_pct = max(w_p1_total, w_p2_total)
        final_diff = abs(w_p1_total - w_p2_total)

        fav_sides = [s for s in sides if "ต่อ" in s]
        has_mixed_fav = len(set(fav_sides)) > 1

        has_severe_conflict = False
        for idx, rd in enumerate(row_details):
            if rd['adv'] != winner_team:
                if hdp_numeric[idx] > hdp_numeric[0] and sides[idx] == f"{winner_team} ต่อ":
                    continue
                if rd['diff'] >= 8.0:
                    has_severe_conflict = True
                    break

        if has_severe_conflict:
            grade = "เกรด C- (อันตรายสูงสุด: ราคาแตกแถวรุนแรง โต๊ะวางกับดัก)"
            grade_color = "red"
            advice = f"เลี่ยงวาง [{winner_team}]"
            analysis_note = "⚠️ มีราคาชี้น้ำสวนทางอย่างรุนแรง ไม่แนะนำให้ลงทุน"
        elif has_mixed_fav:
            grade = "เกรด B- (ระวัง: มีการสลับฝั่งต่อรอง)"
            grade_color = "orange"
            advice = f"พิจารณาวาง [{winner_team}] ด้วยความระมัดระวัง"
            analysis_note = "⚠️ ราคาต่อรองสลับฝั่งไปมา ควรลดวงเงินหรือข้าม"
        elif final_win_pct >= 55.0 and final_diff >= 10.0:
            grade = "เกรด A+ (ความมั่นใจสูงสุด: ตลาดเอกฉันท์)"
            grade_color = "green"
            advice = f"วาง [{winner_team}]"
            analysis_note = "✨ ค่าน้ำและราคาหนุนฝั่งเดียวกันชัดเจน ทรงบอลได้เปรียบสูง"
        elif final_win_pct >= 51.5:
            grade = "เกรด A (น่าลงทุน: ทิศทางราคาชัดเจน)"
            grade_color = "blue"
            advice = f"วาง [{winner_team}]"
            analysis_note = "✅ สัญญาณค่าน้ำไหลไปทิศทางเดียวกันอย่างมีนัยสำคัญ ได้เปรียบชัดเจน"
        else:
            grade = "เกรด B (ปานกลาง: บอลสูสี)"
            grade_color = "gray"
            advice = f"พิจารณา [{winner_team}] หรือเน้นบอลสด"
            analysis_note = "ℹ️ ค่าน้ำสองฝั่งค่อนข้างสมดุล"

        st.subheader(f"🎯 ชี้เป้าฝั่งที่ได้เปรียบ ({mode})")
        with st.container(border=True):
            st.markdown(f"### 👉 แนะนำ: **{advice}**")
            if grade_color == "green":
                st.success(f"**สถานะความมั่นใจ:** 🟢 {grade}")
            elif grade_color == "blue":
                st.info(f"**สถานะความมั่นใจ:** 🔵 {grade}")
            elif grade_color == "orange":
                st.warning(f"**สถานะความมั่นใจ:** 🟠 {grade}")
            elif grade_color == "red":
                st.error(f"**สถานะความมั่นใจ:** 🔴 {grade}")
            else:
                st.write(f"**สถานะความมั่นใจ:** ⚪ {grade}")

            st.write(f"📌 **เรตที่แนะนำ:** ยึดราคาเปิดหลักแถว 1 ({side1} - {rate1})")
            st.caption(f"💡 **วิเคราะห์เชิงลึก:** {analysis_note}")

        st.subheader("📊 เจาะลึกรายแถวราคา")
        for i in range(num_rows):
            st.write(f"**แถวที่ {i+1} [{sides[i]} ({rates[i]})]:** {team1_name} ({row_details[i]['p1']:.1f}%) vs {team2_name} ({row_details[i]['p2']:.1f}%)")
            st.caption(f"★ ทิศทางราคาเทไป: {row_details[i]['adv']} | ส่วนต่างได้เปรียบ: {row_details[i]['diff']:.2f}%")


import streamlit as st

# กำหนดค่าหน้าเว็บ
st.set_page_config(page_title="เครื่องมือวิเคราะห์แฮนดิแคป", page_icon="⚽", layout="wide")

st.title("⚽ เครื่องมือวิเคราะห์บอล: แฮนดิแคป 3 แถว")
st.caption("ระบบคำนวณค่าน้ำ ป้องกันกับดักราคา และประเมินเกรดความน่าลงทุน")

# ฟังก์ชันแปลงค่าแต้มต่อเป็นตัวเลข
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

# ส่วนที่ 1: ข้อมูลทีม
st.subheader("📌 1. ระบุชื่อทีม")
c_t1, c_t2 = st.columns(2)
with c_t1:
    team1_name = st.text_input("ทีมเหย้า [1]", value="เจ้าบ้าน")
with c_t2:
    team2_name = st.text_input("ทีมเยือน [2]", value="ทีมเยือน")

# รายการตัวเลือกสำหรับดรอปดาวน์
side_options = [f"{team1_name} ต่อ", f"{team2_name} ต่อ", "เสมอ (0)"]
hdp_rate_options = [
    "0", "0-0.5", "0.5", "0.5-1", "1.0", "1-1.5", 
    "1.5", "1.5-2", "2.0", "2-2.5", "2.5", "2.5-3", "3.0", "3-3.5", "3.5"
]

st.divider()

# ส่วนที่ 2: กรอกข้อมูล 3 แถว
st.subheader("🔢 2. ค่าน้ำและเรตราคา 3 แถว (เลือกฝั่งต่อแยกแถวได้)")

# แถวที่ 1 (น้ำหนัก 50%)
st.markdown("• **แถวที่ 1 (น้ำหนัก 50% - ราคาเปิดหลัก)**")
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

# แถวที่ 2 (น้ำหนัก 25%)
st.markdown("• **แถวที่ 2 (น้ำหนัก 25%)**")
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

# แถวที่ 3 (น้ำหนัก 25%)
st.markdown("• **แถวที่ 3 (น้ำหนัก 25%)**")
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

# ฟังก์ชันคำนวณความน่าจะเป็นของค่าน้ำในแต่ละแถว
def calc_row_probs(odd1, odd2):
    raw_p1 = 1.0 / odd1
    raw_p2 = 1.0 / odd2
    total_m = raw_p1 + raw_p2
    p1 = (raw_p1 / total_m) * 100.0
    p2 = (raw_p2 / total_m) * 100.0

    # โบนัสน้ำต่ำ (Juice Trap Bonus)
    if odd1 <= 1.75:
        p1 += 3.5
        p2 -= 3.5
    elif odd2 <= 1.75:
        p2 += 3.5
        p1 -= 3.5

    adv = team1_name if p1 > p2 else team2_name
    diff = abs(p1 - p2)
    return p1, p2, adv, diff

# ประมวลผลเมื่อกดปุ่ม
if st.button("🚀 สรุปผลวิเคราะห์ระดับลึก", type="primary", use_container_width=True):
    weights = [0.50, 0.25, 0.25]
    odds = [(o1_1, o1_2), (o2_1, o2_2), (o3_1, o3_2)]
    rates = [rate1, rate2, rate3]
    sides = [side1, side2, side3]

    row_details = []
    w_p1_total = 0.0
    w_p2_total = 0.0

    for i in range(3):
        p1, p2, adv, diff = calc_row_probs(odds[i][0], odds[i][1])
        row_details.append({
            "p1": p1, "p2": p2, "adv": adv, "diff": diff,
            "rate": rates[i], "side": sides[i]
        })
        w_p1_total += p1 * weights[i]
        w_p2_total += p2 * weights[i]

    winner_team = team1_name if w_p1_total > w_p2_total else team2_name
    final_win_pct = max(w_p1_total, w_p2_total)
    final_diff = abs(w_p1_total - w_p2_total)

    # ตรวจสอบการสลับฝั่งต่อ
    has_mixed_fav = False
    fav_sides = [s for s in sides if "ต่อ" in s]
    if len(set(fav_sides)) > 1:
        has_mixed_fav = True

    # คำนวณแต้มต่อเป็นตัวเลข
    hdp_numeric = [parse_hdp_val(r) for r in rates]

    # ตรวจสอบการแตกแถวอย่างสมเหตุสมผล
    has_severe_conflict = False
    for idx, rd in enumerate(row_details):
        if rd['adv'] != winner_team:
            # ข้ามแถวที่ต่อลึกกว่าราคาหลักแล้วน้ำล้นตามธรรมชาติ
            if hdp_numeric[idx] > hdp_numeric[0] and sides[idx] == f"{winner_team} ต่อ":
                continue
            # แตกแถวจริงเมื่อแต้มต่อเท่าเดิมหรือลดลง แต่น้ำเทสวนเกิน 8%
            if rd['diff'] >= 8.0:
                has_severe_conflict = True
                break

    # ประเมินเกรดความมั่นใจ
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
    elif final_win_pct >= 58.0 and final_diff >= 12.0:
        grade = "เกรด A+ (ความมั่นใจสูงสุด: ตลาดเอกฉันท์)"
        grade_color = "green"
        advice = f"วาง [{winner_team}]"
        analysis_note = "✨ ค่าน้ำและราคาหนุนฝั่งเดียวกันชัดเจน ทรงบอลได้เปรียบสูง"
    elif final_win_pct >= 54.0:
        grade = "เกรด A (น่าลงทุน: ทิศทางราคาชัดเจน)"
        grade_color = "blue"
        advice = f"วาง [{winner_team}]"
        analysis_note = "✅ สัญญาณค่าน้ำไหลไปทิศทางเดียวกันอย่างมีนัยสำคัญ"
    else:
        grade = "เกรด B (ปานกลาง: บอลสูสี)"
        grade_color = "gray"
        advice = f"พิจารณา [{winner_team}] หรือเน้นบอลสด"
        analysis_note = "ℹ️ ค่าน้ำสองฝั่งค่อนข้างสมดุล"

    # แสดงผลสรุป
    st.subheader("🎯 ชี้เป้าฝั่งที่ได้เปรียบ")
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

    # แสดงรายละเอียดแยกแถว
    st.subheader("📊 เจาะลึกรายแถวราคา")
    for i in range(3):
        st.write(f"**แถวที่ {i+1} [{sides[i]} ({rates[i]})]:** {team1_name} ({row_details[i]['p1']:.1f}%) vs {team2_name} ({row_details[i]['p2']:.1f}%)")
        st.caption(f"★ ทิศทางราคาเทไป: {row_details[i]['adv']} | ส่วนต่างได้เปรียบ: {row_details[i]['diff']:.2f}%")
        

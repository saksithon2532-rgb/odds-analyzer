import streamlit as st

st.set_page_config(page_title="Odds Analyzer Pro V10.2", page_icon="⚽", layout="centered")

st.title("⚽ เครื่องมือวิเคราะห์ราคาบอล (Pro V10.2)")
st.caption("ระบบคัดเกรดความได้เปรียบ A/B/C ถ่วงน้ำหนักราคาหลัก พร้อมใช้งานง่ายบนมือถือ")

# ตัวเลือกเรตราคามาตรฐาน
HDP_OPTIONS = [
    "เสมอ (0)", "0-0.5 (เสมอควบครึ่ง)", "0.5 (ครึ่งลูก)", 
    "0.5-1 (ครึ่งควบลูก)", "1.0 (หนึ่งลูก)", "1-1.5 (ลูกควบลูกครึ่ง)", 
    "1.5 (ลูกครึ่ง)", "1.5-2 (ลูกครึ่งควบสอง)", "2.0 (สองลูก)"
]

# 1. ข้อมูลคู่แข่งขัน
st.subheader("📌 1. คู่แข่งขัน & ฝั่งต่อ")
col_t1, col_t2 = st.columns(2)
with col_t1:
    home_name = st.text_input("ทีมเหย้า (ฝั่งซ้าย)", value="เจ้าบ้าน")
with col_t2:
    away_name = st.text_input("ทีมเยือน (ฝั่งขวา)", value="ทีมเยือน")

fav_side = st.radio(
    "ทีมที่เป็นต่อ:",
    [f"{home_name} ต่อ", f"{away_name} ต่อ", "ราคาเสมอ"],
    horizontal=True
)

st.markdown("---")
st.subheader("🔢 2. ค่าน้ำและเรตราคา 3 แถว")

# แถวที่ 1: ราคาหลัก
st.markdown("##### 🔹 แถวที่ 1 (ราคาเปิดหลัก - น้ำหนัก 50%)")
h1 = st.selectbox("เรตแต้มต่อ แถวที่ 1", HDP_OPTIONS, index=3, key="h1")
c1_l, c1_r = st.columns(2)
with c1_l:
    l1 = st.number_input(f"น้ำ {home_name} (แถว 1)", min_value=1.01, max_value=20.00, value=1.94, step=0.01)
with c1_r:
    r1 = st.number_input(f"น้ำ {away_name} (แถว 1)", min_value=1.01, max_value=20.00, value=1.95, step=0.01)

# แถวที่ 2: ราคารอง 1
st.markdown("##### 🔹 แถวที่ 2 (ราคารอง 1 - น้ำหนัก 25%)")
h2 = st.selectbox("เรตแต้มต่อ แถวที่ 2", HDP_OPTIONS, index=2, key="h2")
c2_l, c2_r = st.columns(2)
with c2_l:
    l2 = st.number_input(f"น้ำ {home_name} (แถว 2)", min_value=1.01, max_value=20.00, value=1.71, step=0.01)
with c2_r:
    r2 = st.number_input(f"น้ำ {away_name} (แถว 2)", min_value=1.01, max_value=20.00, value=2.22, step=0.01)

# แถวที่ 3: ราคารอง 2
st.markdown("##### 🔹 แถวที่ 3 (ราคารอง 2 - น้ำหนัก 25%)")
h3 = st.selectbox("เรตแต้มต่อ แถวที่ 3", HDP_OPTIONS, index=4, key="h3")
c3_l, c3_r = st.columns(2)
with c3_l:
    l3 = st.number_input(f"น้ำ {home_name} (แถว 3)", min_value=1.01, max_value=20.00, value=2.30, step=0.01)
with c3_r:
    r3 = st.number_input(f"น้ำ {away_name} (แถว 3)", min_value=1.01, max_value=20.00, value=1.66, step=0.01)

st.markdown("---")

# ฟังก์ชันคำนวณถ่วงน้ำหนัก
def calculate_pro_odds():
    weights = [0.50, 0.25, 0.25]
    odds_l = [l1, l2, l3]
    odds_r = [r1, r2, r3]
    handicaps = [h1, h2, h3]
    
    total_score_l = 0
    total_score_r = 0
    row_details = []
    
    for i in range(3):
        ol, or_ = odds_l[i], odds_r[i]
        pl = (1 / ol) * 100 if ol > 0 else 0
        pr = (1 / or_) * 100 if or_ > 0 else 0
        margin = (pl + pr) - 100
        
        fair_l = (pl / (pl + pr)) * 100
        fair_r = (pr / (pl + pr)) * 100
        
        # ดักตรวจจับน้ำกดต่ำผิดปกติ (โต๊ะจ่ายต่ำ แสดงว่ากลัวฝั่งนั้น)
        bonus_l = 3.0 if ol <= 1.78 else 0.0
        bonus_r = 3.0 if or_ <= 1.78 else 0.0
        
        adj_l = fair_l + bonus_l
        adj_r = fair_r + bonus_r
        norm_l = (adj_l / (adj_l + adj_r)) * 100
        norm_r = (adj_r / (adj_l + adj_r)) * 100
        
        total_score_l += norm_l * weights[i]
        total_score_r += norm_r * weights[i]
        
        row_details.append({
            "row": i + 1,
            "rate": handicaps[i],
            "fair_l": norm_l,
            "fair_r": norm_r,
            "margin": margin,
            "low_juice_l": ol <= 1.78,
            "low_juice_r": or_ <= 1.78
        })
        
    return total_score_l, total_score_r, row_details

if st.button("🚀 สรุปผลวิเคราะห์ความได้เปรียบ", use_container_width=True):
    score_l, score_r, details = calculate_pro_odds()
    
    st.subheader("🎯 ชี้เป้าฝั่งที่ได้เปรียบ")
    
    diff = abs(score_l - score_r)
    is_left = score_l > score_r
    target_team = home_name if is_left else away_name
    
    # คำนวณเกรดความมั่นใจ
    if diff >= 4.0:
        grade = "🟢 เกรด A (มั่นใจสูง)"
        desc = "กระแสน้ำไหลไปทิศทางเดียวกันอย่างชัดเจน โต๊ะแบกความเสี่ยงฝั่งนี้ เหมาะทั้งบอลเต็งและสเต็ป"
    elif diff >= 1.5:
        grade = "🔵 เกรด B (น่าลงทุน)"
        desc = "น้ำแถวหลักเอื้อชัดเจน แต่อาจมีราคาขยับดักไว้ เหมาะสำหรับเล่นเต็งเดี่ยว"
    else:
        grade = "🟡 เกรด C (ราคาก้ำกึ่ง / เสี่ยง)"
        desc = "โต๊ะเกลี่ยน้ำสมดุลทั้งสองฝั่ง ไม่มีความได้เปรียบชัดเจน แนะนำให้เลี่ยงคู่นี้"

    col_box1, col_box2 = st.columns([2, 1])
    with col_box1:
        if diff >= 1.5:
            st.success(f"### 👉 แนะนำเล่น: **[{target_team}]**")
            st.write(f"📌 **เรตที่แนะนำ:** ยึดราคาหลักแถว 1 **({h1})** หรือเรตแถว 2 ที่น้ำสวย")
        else:
            st.warning("### ⚖️ สองฝั่งได้เปรียบสูสีกัน")
            st.write("📌 แนะนำให้ผ่าน หรือรอราคาไหลช่วงใกล้แข่ง")
    with col_box2:
        st.info(f"**สถานะความมั่นใจ:**\n\n{grade}")

    st.caption(f"💡 {desc}")
    st.markdown("---")
    
    st.subheader("📊 เจาะลึกรายแถวราคา")
    for row in details:
        adv_str = home_name if row['fair_l'] > row['fair_r'] else away_name
        note = ""
        if row['low_juice_l']:
            note = f" ⚠️ *โต๊ะกดน้ำ {home_name} ต่ำผิดปกติ*"
        elif row['low_juice_r']:
            note = f" ⚠️ *โต๊ะกดน้ำ {away_name} ต่ำผิดปกติ*"
            
        st.write(f"**แถวที่ {row['row']} [{row['rate']}]:** {home_name} ({row['fair_l']:.1f}%) vs {away_name} ({row['fair_r']:.1f}%)")
        st.caption(f"👉 ทิศทางราคาเทไป: **{adv_str}** | ค่าน้ำโต๊ะ: {row['margin']:.2f}%{note}")

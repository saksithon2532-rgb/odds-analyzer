
import streamlit as st

st.set_page_config(page_title="Odds Advantage Analyzer", page_icon="⚽", layout="centered")

st.title("⚽ เครื่องมือวิเคราะห์ความได้เปรียบของค่าน้ำ")
st.caption("คำนวณ Implied Probability, ทิศทางน้ำ และแรงกดราคา พร้อมชี้เป้าฝั่งได้เปรียบทุกคู่")

# ฟังก์ชันคำนวณและวิเคราะห์
def analyze_odds(l_name, r_name, left_odds, right_odds):
    results = []
    total_score_left = 0
    total_score_right = 0
    
    for i in range(3):
        l = left_odds[i]
        r = right_odds[i]
        
        # คำนวณ Implied Probability (ความน่าจะเป็นแฝง)
        prob_l = (1 / l) * 100 if l > 0 else 0
        prob_r = (1 / r) * 100 if r > 0 else 0
        margin = (prob_l + prob_r) - 100 # ค่าน้ำที่โต๊ะหัก
        
        # ปรับ Probability ให้เป็นแบบตัดค่าน้ำโต๊ะออก (Fair Probability)
        fair_prob_l = (prob_l / (prob_l + prob_r)) * 100
        fair_prob_r = (prob_r / (prob_l + prob_r)) * 100
        
        # วิเคราะห์ฝั่งได้เปรียบในแต่ละแถว
        if fair_prob_l > fair_prob_r:
            adv = l_name
            total_score_left += (fair_prob_l - fair_prob_r)
        else:
            adv = r_name
            total_score_right += (fair_prob_r - fair_prob_l)
            
        results.append({
            "row": i + 1,
            "l_prob": fair_prob_l,
            "r_prob": fair_prob_r,
            "adv": adv,
            "margin": margin
        })
    
    return results, total_score_left, total_score_right

# UI รับข้อมูล
st.subheader("📌 ข้อมูลคู่แข่งขัน")
col_name1, col_name2 = st.columns(2)
with col_name1:
    left_team = st.text_input("ชื่อฝั่งซ้าย (เหย้า / สูง)", value="ฝั่งซ้าย")
with col_name2:
    right_team = st.text_input("ชื่อฝั่งขวา (เยือน / ต่ำ)", value="ฝั่งขวา")

st.markdown("---")
st.subheader("🔢 กรอกค่าน้ำ 3 แถว")

col_l, col_r = st.columns(2)

with col_l:
    st.markdown(f"**{left_team}**")
    l1 = st.number_input("แถวที่ 1 (ซ้าย)", min_value=1.01, max_value=20.00, value=1.85, step=0.01)
    l2 = st.number_input("แถวที่ 2 (ซ้าย)", min_value=1.01, max_value=20.00, value=2.10, step=0.01)
    l3 = st.number_input("แถวที่ 3 (ซ้าย)", min_value=1.01, max_value=20.00, value=2.45, step=0.01)

with col_r:
    st.markdown(f"**{right_team}**")
    r1 = st.number_input("แถวที่ 1 (ขวา)", min_value=1.01, max_value=20.00, value=2.05, step=0.01)
    r2 = st.number_input("แถวที่ 2 (ขวา)", min_value=1.01, max_value=20.00, value=1.80, step=0.01)
    r3 = st.number_input("แถวที่ 3 (ขวา)", min_value=1.01, max_value=20.00, value=1.55, step=0.01)

# ปุ่มคำนวณ
if st.button("🚀 วิเคราะห์ความได้เปรียบ", use_container_width=True):
    left_odds = [l1, l2, l3]
    right_odds = [r1, r2, r3]
    
    rows_data, score_l, score_r = analyze_odds(left_team, right_team, left_odds, right_odds)
    
    st.markdown("---")
    st.subheader("📊 ผลการวิเคราะห์แยกตามแถวราคา")
    
    for row in rows_data:
        st.write(f"**แถวที่ {row['row']}:** {left_team} ({row['l_prob']:.1f}%) vs {right_team} ({row['r_prob']:.1f}%) | โต๊ะหักค่าน้ำ {row['margin']:.2f}%")
        st.caption(f"👉 แถวนี้ฝั่งได้เปรียบเชิงราคา: **{row['adv']}**")

    st.markdown("---")
    
    # บทสรุปฟันธง
    if score_l > score_r:
        diff = score_l - score_r
        confidence = min(90.0, 50.0 + (diff / 3))
        st.success(f"🎯 **ฟันธงภาพรวม:** แนะนำวางฝั่ง **[{left_team}]**")
        st.info(f"ดัชนีความได้เปรียบเชิงราคาอยู่ที่ **{confidence:.1f}%**")
    elif score_r > score_l:
        diff = score_r - score_l
        confidence = min(90.0, 50.0 + (diff / 3))
        st.success(f"🎯 **ฟันธงภาพรวม:** แนะนำวางฝั่ง **[{right_team}]**")
        st.info(f"ดัชนีความได้เปรียบเชิงราคาอยู่ที่ **{confidence:.1f}%**")
    else:
        st.warning("⚖️ ทั้งสองฝั่งราคาเปิดมาสมดุลกันมาก แนะนำให้มองหาตัวเลือกอื่นหรือเล่นเรตเสมอ")

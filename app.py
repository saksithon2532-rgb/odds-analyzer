import streamlit as st

st.set_page_config(page_title="Odds Advantage Analyzer", page_icon="⚽", layout="centered")

st.title("⚽ เครื่องมือวิเคราะห์ความได้เปรียบ")
st.caption("คำนวณราคาต่อรอง/สูงต่ำ ร่วมกับค่าน้ำ 3 แถว พร้อมชี้เป้าฝั่งได้เปรียบทุกคู่")

# ฟังก์ชันคำนวณ
def analyze_odds(l_name, r_name, handicaps, left_odds, right_odds):
    results = []
    total_score_left = 0
    total_score_right = 0
    
    for i in range(3):
        h = handicaps[i]
        l = left_odds[i]
        r = right_odds[i]
        
        prob_l = (1 / l) * 100 if l > 0 else 0
        prob_r = (1 / r) * 100 if r > 0 else 0
        margin = (prob_l + prob_r) - 100
        
        fair_prob_l = (prob_l / (prob_l + prob_r)) * 100
        fair_prob_r = (prob_r / (prob_l + prob_r)) * 100
        
        if fair_prob_l > fair_prob_r:
            adv = f"{l_name} (เรต {h})"
            total_score_left += (fair_prob_l - fair_prob_r)
        else:
            adv = f"{r_name} (เรต {h})"
            total_score_right += (fair_prob_r - fair_prob_l)
            
        results.append({
            "row": i + 1,
            "handicap": h,
            "l_prob": fair_prob_l,
            "r_prob": fair_prob_r,
            "adv": adv,
            "margin": margin
        })
    
    return results, total_score_left, total_score_right

# 1. ข้อมูลคู่แข่งขัน
st.subheader("📌 ข้อมูลคู่แข่งขัน")
col_n1, col_n2 = st.columns(2)
with col_n1:
    left_team = st.text_input("ชื่อฝั่งซ้าย (เหย้า / สูง)", value="เจ้าบ้าน")
with col_n2:
    right_team = st.text_input("ชื่อฝั่งขวา (เยือน / ต่ำ)", value="ทีมเยือน")

st.markdown("---")
st.subheader("🔢 กรอกราคาต่อรอง & ค่าน้ำ 3 แถว")

# แถวที่ 1
st.markdown("##### 🔹 แถวที่ 1 (ราคาหลัก)")
h1 = st.text_input("แต้มต่อ / สูงต่ำ แถวที่ 1 (เช่น 0.5, 0.5-1, 2.5)", value="0.5", key="h1")
c1_l, c1_r = st.columns(2)
with c1_l:
    l1 = st.number_input(f"น้ำ {left_team} (ซ้าย 1)", min_value=1.01, max_value=20.00, value=1.85, step=0.01)
with c1_r:
    r1 = st.number_input(f"น้ำ {right_team} (ขวา 1)", min_value=1.01, max_value=20.00, value=2.05, step=0.01)

# แถวที่ 2
st.markdown("##### 🔹 แถวที่ 2 (ราคารอง 1)")
h2 = st.text_input("แต้มต่อ / สูงต่ำ แถวที่ 2 (เช่น 0.5-1, 1.0, 2.5-3)", value="0.5-1", key="h2")
c2_l, c2_r = st.columns(2)
with c2_l:
    l2 = st.number_input(f"น้ำ {left_team} (ซ้าย 2)", min_value=1.01, max_value=20.00, value=2.10, step=0.01)
with c2_r:
    r2 = st.number_input(f"น้ำ {right_team} (ขวา 2)", min_value=1.01, max_value=20.00, value=1.80, step=0.01)

# แถวที่ 3
st.markdown("##### 🔹 แถวที่ 3 (ราคารอง 2)")
h3 = st.text_input("แต้มต่อ / สูงต่ำ แถวที่ 3 (เช่น 0-0.5, เสมอ, 2.0-2.5)", value="0-0.5", key="h3")
c3_l, c3_r = st.columns(2)
with c3_l:
    l3 = st.number_input(f"น้ำ {left_team} (ซ้าย 3)", min_value=1.01, max_value=20.00, value=2.45, step=0.01)
with c3_r:
    r3 = st.number_input(f"น้ำ {right_team} (ขวา 3)", min_value=1.01, max_value=20.00, value=1.55, step=0.01)

st.markdown("---")

# ปุ่มคำนวณ
if st.button("🚀 วิเคราะห์ความได้เปรียบ", use_container_width=True):
    handicaps = [h1, h2, h3]
    left_odds = [l1, l2, l3]
    right_odds = [r1, r2, r3]
    
    rows_data, score_l, score_r = analyze_odds(left_team, right_team, handicaps, left_odds, right_odds)
    
    st.subheader("📊 ผลการวิเคราะห์รายแถวราคา")
    for row in rows_data:
        st.write(f"**แถวที่ {row['row']} [เรต {row['handicap']}]:** {left_team} ({row['l_prob']:.1f}%) vs {right_team} ({row['r_prob']:.1f}%)")
        st.caption(f"👉 ฝั่งได้เปรียบเชิงราคา: **{row['adv']}** (ค่าน้ำโต๊ะ {row['margin']:.2f}%)")

    st.markdown("---")
    
    if score_l > score_r:
        diff = score_l - score_r
        confidence = min(92.0, 50.0 + (diff / 3))
        st.success(f"🎯 **ฟันธงภาพรวม:** น้ำไหลเอื้อฝั่ง **[{left_team}]**")
        st.info(f"ดัชนีความได้เปรียบเชิงราคาโดยรวมอยู่ที่ **{confidence:.1f}%**")
    elif score_r > score_l:
        diff = score_r - score_l
        confidence = min(92.0, 50.0 + (diff / 3))
        st.success(f"🎯 **ฟันธงภาพรวม:** น้ำไหลเอื้อฝั่ง **[{right_team}]**")
        st.info(f"ดัชนีความได้เปรียบเชิงราคาโดยรวมอยู่ที่ **{confidence:.1f}%**")
    else:
        st.warning("⚖️ ราคาสมดุลทั้งสองฝั่ง ไม่มีความได้เปรียบชัดเจน")

import streamlit as st

st.set_page_config(page_title="Odds Advantage Analyzer", page_icon="⚽", layout="centered")

st.title("⚽ เครื่องมือวิเคราะห์ความได้เปรียบของค่าน้ำ")
st.caption("คำนวณ Implied Probability พร้อมหัก Margin โต๊ะ และเปรียบเทียบ 3 แถวราคา")

# 1. ข้อมูลคู่แข่งขัน
st.subheader("📌 1. ข้อมูลคู่แข่งขัน")
col_t1, col_t2 = st.columns(2)
with col_t1:
    left_team = st.text_input("ชื่อฝั่งซ้าย (เจ้าบ้าน / สูง)", value="เจ้าบ้าน")
with col_t2:
    right_team = st.text_input("ชื่อฝั่งขวา (ทีมเยือน / ต่ำ)", value="ทีมเยือน")

st.markdown("---")
st.subheader("🔢 2. กรอกราคาต่อรอง & ค่าน้ำ 3 แถว")

# แถวที่ 1
st.markdown("##### 🔹 แถวที่ 1 (ราคาหลัก)")
h1 = st.text_input("แต้มต่อ / เรตสูงต่ำ แถวที่ 1 (เช่น 0.5, 0.5-1, 2.5)", value="0.5", key="h1")
c1_l, c1_r = st.columns(2)
with c1_l:
    l1 = st.number_input(f"ค่าน้ำ {left_team} (ซ้าย 1)", min_value=1.01, max_value=20.00, value=1.85, step=0.01)
with c1_r:
    r1 = st.number_input(f"ค่าน้ำ {right_team} (ขวา 1)", min_value=1.01, max_value=20.00, value=2.05, step=0.01)

# แถวที่ 2
st.markdown("##### 🔹 แถวที่ 2 (ราคารอง 1)")
h2 = st.text_input("แต้มต่อ / เรตสูงต่ำ แถวที่ 2 (เช่น 0.5-1, 1.0, 2.5-3)", value="0.5-1", key="h2")
c2_l, c2_r = st.columns(2)
with c2_l:
    l2 = st.number_input(f"ค่าน้ำ {left_team} (ซ้าย 2)", min_value=1.01, max_value=20.00, value=2.10, step=0.01)
with c2_r:
    r2 = st.number_input(f"ค่าน้ำ {right_team} (ขวา 2)", min_value=1.01, max_value=20.00, value=1.80, step=0.01)

# แถวที่ 3
st.markdown("##### 🔹 แถวที่ 3 (ราคารอง 2)")
h3 = st.text_input("แต้มต่อ / เรตสูงต่ำ แถวที่ 3 (เช่น 0-0.5, เสมอ, 2.0-2.5)", value="0-0.5", key="h3")
c3_l, c3_r = st.columns(2)
with c3_l:
    l3 = st.number_input(f"ค่าน้ำ {left_team} (ซ้าย 3)", min_value=1.01, max_value=20.00, value=2.45, step=0.01)
with c3_r:
    r3 = st.number_input(f"ค่าน้ำ {right_team} (ขวา 3)", min_value=1.01, max_value=20.00, value=1.55, step=0.01)

st.markdown("---")

# ปุ่มคำนวณ
if st.button("🚀 วิเคราะห์ความได้เปรียบ", use_container_width=True):
    handicaps = [h1, h2, h3]
    left_odds = [l1, l2, l3]
    right_odds = [r1, r2, r3]
    
    total_score_left = 0
    total_score_right = 0
    results = []

    for i in range(3):
        h = handicaps[i]
        l = left_odds[i]
        r = right_odds[i]
        
        prob_l = (1 / l) * 100 if l > 0 else 0
        prob_r = (1 / r) * 100 if r > 0 else 0
        margin = (prob_l + prob_r) - 100
        
        fair_l = (prob_l / (prob_l + prob_r)) * 100
        fair_r = (prob_r / (prob_l + prob_r)) * 100
        
        if fair_l > fair_r:
            adv = f"{left_team} (เรต {h})"
            total_score_left += (fair_l - fair_r)
        else:
            adv = f"{right_team} (เรต {h})"
            total_score_right += (fair_r - fair_l)
            
        results.append({
            "row": i + 1,
            "h": h,
            "fair_l": fair_l,
            "fair_r": fair_r,
            "adv": adv,
            "margin": margin
        })

    st.subheader("📊 ผลวิเคราะห์แยกรายแถวราคา")
    for item in results:
        st.write(f"**แถวที่ {item['row']} [เรต {item['h']}]:** {left_team} ({item['fair_l']:.1f}%) vs {right_team} ({item['fair_r']:.1f}%)")
        st.caption(f"👉 ฝั่งได้เปรียบ: **{item['adv']}** (ค่าน้ำโต๊ะหัก {item['margin']:.2f}%)")

    st.markdown("---")
    
    # สรุปภาพรวม
    if total_score_left > total_score_right:
        diff = total_score_left - total_score_right
        conf = min(92.0, 50.0 + (diff / 3))
        st.success(f"🎯 **ฟันธงภาพรวม:** กระแสน้ำเอื้อฝั่ง **[{left_team}]**")
        st.info(f"ดัชนีความได้เปรียบเชิงราคาอยู่ที่ **{conf:.1f}%**")
    elif total_score_right > total_score_left:
        diff = total_score_right - total_score_left
        conf = min(92.0, 50.0 + (diff / 3))
        st.success(f"🎯 **ฟันธงภาพรวม:** กระแสน้ำเอื้อฝั่ง **[{right_team}]**")
        st.info(f"ดัชนีความได้เปรียบเชิงราคาอยู่ที่ **{conf:.1f}%**")
    else:
        st.warning("⚖️ ราคาสมดุลทั้งสองฝั่ง ไม่มีความได้เปรียบชัดเจน")

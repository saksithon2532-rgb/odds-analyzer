import streamlit as st

st.set_page_config(page_title="UG Odds Pattern", layout="centered")
st.title("⚽ ตัวช่วยวิเคราะห์สูตรค่าน้ำ 1.5 & 1.7")

st.info("กรอกค่าน้ำ 3 แถวแรกของคู่นั้นๆ (ดูเฉพาะ 3 แถวแรก)")

col1, col2 = st.columns(2)
with col1:
    st.subheader("ฝั่งซ้าย (เหย้า / สูง)")
    name_a = st.text_input("ชื่อทีมซ้าย / หรือพิมพ์ 'สูง'", "ทีมซ้าย")
    r1_a = st.number_input("แถวที่ 1 (น้ำซ้าย)", value=1.84, step=0.01, format="%.2f")
    r2_a = st.number_input("แถวที่ 2 (น้ำซ้าย)", value=2.15, step=0.01, format="%.2f")
    r3_a = st.number_input("แถวที่ 3 (น้ำซ้าย)", value=2.52, step=0.01, format="%.2f")

with col2:
    st.subheader("ฝั่งขวา (เยือน / ต่ำ)")
    name_b = st.text_input("ชื่อทีมขวา / หรือพิมพ์ 'ต่ำ'", "ทีมขวา")
    r1_b = st.number_input("แถวที่ 1 (น้ำขวา)", value=2.05, step=0.01, format="%.2f")
    r2_b = st.number_input("แถวที่ 2 (น้ำขวา)", value=1.76, step=0.01, format="%.2f")
    r3_b = st.number_input("แถวที่ 3 (น้ำขวา)", value=1.55, step=0.01, format="%.2f")

if st.button("🚀 ตรวจสอบผลตามสูตร", use_container_width=True):
    rows = [
        {'left': r1_a, 'right': r1_b},
        {'left': r2_a, 'right': r2_b},
        {'left': r3_a, 'right': r3_b}
    ]
    
    pos_15 = None
    pos_17 = None
    
    for row in rows:
        for side in ['left', 'right']:
            val = row[side]
            if 1.50 <= val <= 1.59 and pos_15 is None:
                pos_15 = side
            elif 1.70 <= val <= 1.79 and pos_17 is None:
                pos_17 = side

    if pos_15 and pos_17:
        if pos_15 != pos_17:
            win_name = name_a if pos_15 == 'left' else name_b
            win_odd = r1_a if pos_15 == 'left' else r1_b
            st.success(f"✅ **เข้าสูตร: ตามฝั่ง 1.5**\n\n👉 **คำแนะนำ:** ให้เล่นฝั่ง **[{win_name}]** ที่ราคาหลักแถว 1 (ค่าน้ำ {win_odd})")
        else:
            opp_side = 'right' if pos_15 == 'left' else 'left'
            opp_name = name_a if opp_side == 'left' else name_b
            opp_odd = r1_a if opp_side == 'left' else r1_b
            st.warning(f"⚠️ **เข้าสูตรราคาหลอก (1.5 & 1.7 อยู่ฝั่งเดียวกัน)**\n\n👉 **คำแนะนำ:** ให้เล่นสวนทางไปฝั่ง **[{opp_name}]** ที่ราคาหลักแถว 1 (ค่าน้ำ {opp_odd})")
    else:
        st.error("❌ คู่นี้ไม่เข้าสูตร 1.5 & 1.7 (ข้ามไปดูคู่อื่น)")

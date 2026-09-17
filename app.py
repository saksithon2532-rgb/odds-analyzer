import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import re

st.set_page_config(page_title="Pro Odds Analyzer V11", page_icon="⚽", layout="centered")

# แถบตั้งค่าด้านข้าง
with st.sidebar:
    st.subheader("🔑 ตั้งค่าระบบ AI")
    api_key = st.text_input("ใส่ Gemini API Key:", type="password")
    st.caption("คีย์จะถูกใช้สำหรับอ่านภาพเท่านั้น ไม่มีการบันทึกข้อมูล")

st.title("⚽ เครื่องมือวิเคราะห์บอลคู่ (Pro V11.0)")
st.caption("ระบบคำนวณ Calibrated Edge Scale พร้อมสแกนราคาอัตโนมัติ")

# ฟังก์ชันอ่านภาพด้วย gemini-2.0-flash ตามที่ระบบแนะนำ
def parse_image_with_gemini(image, key):
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = """
    วิเคราะห์ภาพตารางราคานี้ และดึงข้อมูลของคู่แรกออกมาในรูปแบบ JSON เท่านั้น โดยไม่มี markdown formatting อื่นๆ:
    {
      "home_team": "ชื่อทีมเจ้าบ้าน",
      "away_team": "ชื่อทีมเยือน",
      "hdp": "แต้มต่อ เช่น 0.5 หรือ 0.5-1",
      "fav_team": "เจ้าบ้านต่อ หรือ ทีมเยือนต่อ",
      "hdp_home_odds": 1.85,
      "hdp_away_odds": 2.05,
      "ou": "เรตสูงต่ำ เช่น 2.5",
      "ou_over_odds": 1.95,
      "ou_under_odds": 1.85
    }
    """
    response = model.generate_content([prompt, image])
    text = response.text
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        return json.loads(json_match.group())
    return json.loads(text)

# ฟังก์ชันคำนวณความได้เปรียบ
def calculate_edge(o1, o2):
    p1 = (1 / o1) * 100 if o1 > 0 else 0
    p2 = (1 / o2) * 100 if o2 > 0 else 0
    fair_p1 = (p1 / (p1 + p2)) * 100
    fair_p2 = (p2 / (p1 + p2)) * 100
    margin = (p1 + p2) - 100
    return fair_p1, fair_p2, margin

if "data" not in st.session_state:
    st.session_state.data = {
        "home": "เจ้าบ้าน", "away": "ทีมเยือน",
        "fav": "เจ้าบ้านต่อ", "hdp": "0.5", "l_hdp": 1.85, "r_hdp": 2.05,
        "ou": "2.5", "o_odds": 1.95, "u_odds": 1.85
    }

st.subheader("📷 1. สแกนราคาจากรูปภาพ (ทางเลือก)")
uploaded_file = st.file_uploader("อัปโหลดภาพแคปหน้าจอราคาบอล", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="ภาพที่อัปโหลด", use_container_width=True)
    
    if st.button("🚀 กดให้ AI อ่านข้อมูลจากภาพ", use_container_width=True):
        if not api_key:
            st.error("กรุณากรอก Gemini API Key ที่แถบด้านซ้ายมือก่อนกดอ่านภาพ")
        else:
            try:
                with st.spinner("AI กำลังแกะข้อมูลราคา..."):
                    parsed = parse_image_with_gemini(img, api_key)
                    st.session_state.data["home"] = parsed.get("home_team", "เจ้าบ้าน")
                    st.session_state.data["away"] = parsed.get("away_team", "ทีมเยือน")
                    st.session_state.data["hdp"] = str(parsed.get("hdp", "0.5"))
                    st.session_state.data["fav"] = parsed.get("fav_team", "เจ้าบ้านต่อ")
                    st.session_state.data["l_hdp"] = float(parsed.get("hdp_home_odds", 1.85))
                    st.session_state.data["r_hdp"] = float(parsed.get("hdp_away_odds", 2.05))
                    st.session_state.data["ou"] = str(parsed.get("ou", "2.5"))
                    st.session_state.data["o_odds"] = float(parsed.get("ou_over_odds", 1.95))
                    st.session_state.data["u_odds"] = float(parsed.get("ou_under_odds", 1.85))
                st.success("ดึงข้อมูลสำเร็จเรียบร้อย!")
                st.rerun()
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {str(e)}")

st.markdown("---")

st.subheader("📌 2. ข้อมูลคู่แข่งขัน")
c_t1, c_t2 = st.columns(2)
with c_t1:
    home_name = st.text_input("ทีมเหย้า (ฝั่งซ้าย)", value=st.session_state.data["home"])
with c_t2:
    away_name = st.text_input("ทีมเยือน (ฝั่งขวา)", value=st.session_state.data["away"])

st.subheader("🎯 3. ราคาต่อรอง แฮนดิแคป (HDP)")
fav = st.selectbox("ฝั่งต่อ", ["เจ้าบ้านต่อ", "ทีมเยือนต่อ", "เสมอ (0)"], 
                   index=0 if "เจ้าบ้าน" in st.session_state.data["fav"] else 1)
col_h1, col_h2, col_h3 = st.columns(3)
with col_h1:
    hdp_rate = st.text_input("แต้มต่อ (เช่น 0.5, 0.5-1)", value=st.session_state.data["hdp"])
with col_h2:
    hdp_l = st.number_input(f"น้ำ {home_name}", min_value=1.01, max_value=20.0, value=st.session_state.data["l_hdp"], step=0.01)
with col_h3:
    hdp_r = st.number_input(f"น้ำ {away_name}", min_value=1.01, max_value=20.0, value=st.session_state.data["r_hdp"], step=0.01)

st.subheader("⚽ 4. ราคาสูง-ต่ำ (Over/Under)")
col_u1, col_u2, col_u3 = st.columns(3)
with col_u1:
    ou_rate = st.text_input("เรตสูงต่ำ (เช่น 2.5, 2.5-3)", value=st.session_state.data["ou"])
with col_u2:
    ou_o = st.number_input("น้ำ สูง", min_value=1.01, max_value=20.0, value=st.session_state.data["o_odds"], step=0.01)
with col_u3:
    ou_u = st.number_input("น้ำ ต่ำ", min_value=1.01, max_value=20.0, value=st.session_state.data["u_odds"], step=0.01)

st.markdown("---")

if st.button("📊 วิเคราะห์ความได้เปรียบเชิงราคา", use_container_width=True):
    p_home, p_away, m_hdp = calculate_edge(hdp_l, hdp_r)
    p_over, p_under, m_ou = calculate_edge(ou_o, ou_u)
    
    st.markdown("### 📈 สรุปผลการวิเคราะห์")
    
    st.write(f"**แฮนดิแคป [{hdp_rate}]:** {home_name} ({p_home:.1f}%) vs {away_name} ({p_away:.1f}%) | โต๊ะหักน้ำ {m_hdp:.2f}%")
    if p_home > p_away:
        st.success(f"👉 ค่าน้ำเอื้อฝั่ง: **[{home_name}]** (ความได้เปรียบ {p_home - p_away:.1f}%)")
    else:
        st.success(f"👉 ค่าน้ำเอื้อฝั่ง: **[{away_name}]** (ความได้เปรียบ {p_away - p_home:.1f}%)")
        
    st.write(f"**สูง-ต่ำ [{ou_rate}]:** สูง ({p_over:.1f}%) vs ต่ำ ({p_under:.1f}%) | โต๊ะหักน้ำ {m_ou:.2f}%")
    if p_over > p_under:
        st.success(f"👉 ค่าน้ำเอื้อฝั่ง: **[สกอร์สูง {ou_rate}]** (ความได้เปรียบ {p_over - p_under:.1f}%)")
    else:
        st.success(f"👉 ค่าน้ำเอื้อฝั่ง: **[สกอร์ต่ำ {ou_rate}]** (ความได้เปรียบ {p_under - p_over:.1f}%)")

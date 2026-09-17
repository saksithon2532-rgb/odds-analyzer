import streamlit as st
from PIL import Image
import json
import google.generativeai as genai

st.set_page_config(page_title="Pro Odds Analyzer (AI Scanner)", layout="wide")

st.title("⚽ เครื่องมือวิเคราะห์บอลคู่ (Pro V11.0 + AI Scanner)")
st.caption("ระบบคำนวณ Calibrated Edge Scale พร้อมสแกนราคาอัตโนมัติด้วย AI")

# --- แถบด้านข้างสำหรับตั้งค่า API Key ---
with st.sidebar:
    st.header("🔑 ตั้งค่าระบบ AI")
    api_key = st.text_input("ใส่ Gemini API Key:", type="password", help="วางรหัส API Key ที่ได้จาก Google AI Studio")
    st.info("คีย์จะถูกใช้สำหรับอ่านรูปภาพเท่านั้น ไม่มีการบันทึกข้อมูล")

# --- ฟังก์ชัน AI อ่านภาพ ---
def analyze_image_with_gemini(image, key):
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = """
    คุณเป็นผู้เชี่ยวชาญการอ่านตารางราคาบอลจากรูปภาพ 
    ให้ดึงข้อมูลค่าน้ำและอัตราต่อรองออกมาในรูปแบบ JSON เท่านั้น โดยมีโครงสร้างดังนี้:
    {
      "team_home": "ชื่อทีมเหย้า",
      "team_away": "ชื่อทีมเยือน",
      "hdp_side": "เจ้าบ้านต่อ" หรือ "ทีมเยือนต่อ" หรือ "เสมอ (0)",
      "hdp_val_1": 0.5,
      "hdp_home_1": 1.85,
      "hdp_away_1": 2.05,
      "ou_val_1": 2.5,
      "ou_over_1": 1.95,
      "ou_under_1": 1.85
    }
    ตอบกลับเฉพาะ JSON ล้วนๆ ห้ามมีคำอธิบายเพิ่มเติม ห้ามมี Markdown block อื่น
    """
    response = model.generate_content([prompt, image])
    text = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)

# --- ส่วนสแกนภาพ ---
st.subheader("📷 1. สแกนราคาจากรูปภาพ (ทางเลือก)")
uploaded_file = st.file_uploader("อัปโหลดภาพแคปหน้าจอราคาบอล", type=["jpg", "jpeg", "png"])

scanned_data = {}
if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, caption="ภาพที่อัปโหลด", width=300)
    if st.button("🚀 กดให้ AI อ่านข้อมูลจากภาพ"):
        with st.spinner("AI กำลังวิเคราะห์ข้อมูลราคา..."):
            try:
                scanned_data = analyze_image_with_gemini(img, api_key)
                st.success("อ่านข้อมูลสำเร็จ! ข้อมูลถูกนำไปกรอกในฟอร์มด้านล่างแล้ว")
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาดในการอ่านภาพ: {str(e)}")
elif uploaded_file and not api_key:
    st.warning("⚠️ กรุณากรอก Gemini API Key ที่แถบด้านซ้ายมือก่อนกดอ่านภาพครับ")

st.markdown("---")

# --- ข้อมูลคู่แข่งขัน ---
st.subheader("📌 2. ข้อมูลคู่แข่งขัน")
c1, c2 = st.columns(2)
with c1:
    team_home = st.text_input("ทีมเหย้า (ฝั่งซ้าย)", value=scanned_data.get("team_home", "เจ้าบ้าน"))
with c2:
    team_away = st.text_input("ทีมเยือน (ฝั่งขวา)", value=scanned_data.get("team_away", "ทีมเยือน"))

# --- ราคาต่อรอง แฮนดิแคป ---
st.subheader("🎯 3. ราคาต่อรอง แฮนดิแคป (HDP)")
side_opts = ["เจ้าบ้านต่อ", "ทีมเยือนต่อ", "เสมอ (0)"]
default_side_idx = 0
if scanned_data.get("hdp_side") in side_opts:
    default_side_idx = side_opts.index(scanned_data.get("hdp_side"))

fav_side = st.selectbox("ฝั่งต่อ", side_opts, index=default_side_idx)

col_h1, col_h2, col_h3 = st.columns(3)
with col_h1:
    hdp_val = st.text_input("แต้มต่อ (เช่น 0.5, 0.5-1)", value=str(scanned_data.get("hdp_val_1", "0.5")))
with col_h2:
    water_home = st.number_input("น้ำ เจ้าบ้าน", value=float(scanned_data.get("hdp_home_1", 1.85)), step=0.01)
with col_h3:
    water_away = st.number_input("น้ำ ทีมเยือน", value=float(scanned_data.get("hdp_away_1", 2.05)), step=0.01)

# --- ราคาสูง-ต่ำ ---
st.subheader("⚽ 4. ราคาสูง-ต่ำ (Over/Under)")
col_ou1, col_ou2, col_ou3 = st.columns(3)
with col_ou1:
    ou_val = st.text_input("เรตสูงต่ำ (เช่น 2.5, 2.5-3)", value=str(scanned_data.get("ou_val_1", "2.5")))
with col_ou2:
    water_over = st.number_input("น้ำ สูง", value=float(scanned_data.get("ou_over_1", 1.95)), step=0.01)
with col_ou3:
    water_under = st.number_input("น้ำ ต่ำ", value=float(scanned_data.get("ou_under_1", 1.85)), step=0.01)

st.markdown("---")

# --- ฟังก์ชันคำนวณความน่าจะเป็น ---
def calc_probs(w1, w2):
    inv1 = 1 / w1 if w1 > 0 else 0
    inv2 = 1 / w2 if w2 > 0 else 0
    margin = (inv1 + inv2) - 1
    fair1 = inv1 / (1 + margin) if (1 + margin) > 0 else 0
    fair2 = inv2 / (1 + margin) if (1 + margin) > 0 else 0
    return fair1 * 100, fair2 * 100

if st.button("🚀 คำนวณและชี้เป้าทีเด็ด", use_container_width=True):
    p_home, p_away = calc_probs(water_home, water_away)
    p_over, p_under = calc_probs(water_over, water_under)
    
    st.subheader("📊 ผลการวิเคราะห์สัญญาณราคา")
    
    c_res1, c_res2 = st.columns(2)
    with c_res1:
        st.write(f"**สัญญาณแฮนดิแคป:** เรต {hdp_val}")
        st.write(f"- โอกาส {team_home}: **{p_home:.1f}%**")
        st.write(f"- โอกาส {team_away}: **{p_away:.1f}%**")
        if p_home > p_away + 5:
            st.success(f"ชี้เป้า: **{team_home}** มีกระแสน้ำหนุนชัดเจน")
        elif p_away > p_home + 5:
            st.success(f"ชี้เป้า: **{team_away}** มีกระแสน้ำหนุนชัดเจน")
        else:
            st.info("สัญญาณน้ำสูสี ทั้งสองฝั่งเปิดโอกาสใกล้เคียงกัน")
            
    with c_res2:
        st.write(f"**สัญญาณสูง-ต่ำ:** เรต {ou_val}")
        st.write(f"- โอกาส สกอร์สูง: **{p_over:.1f}%**")
        st.write(f"- โอกาส สกอร์ต่ำ: **{p_under:.1f}%**")
        if p_over > p_under + 5:
            st.success("ชี้เป้า: **สกอร์สูง** กระแสน้ำเปิดกว้าง")
        elif p_under > p_over + 5:
            st.success("ชี้เป้า: **สกอร์ต่ำ** ปลอดภัยกว่า")
        else:
            st.info("สัญญาณประตูรวมยังก้ำกึ่ง")

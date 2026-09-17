import streamlit as st

st.set_page_config(page_title="เครื่องมือวิเคราะห์บอลคู่: Pro V5", page_icon="⚽", layout="wide")

st.title("⚽ เครื่องมือวิเคราะห์บอลคู่: แฮนดิแคป + สูงต่ำ (Pro V5)")
st.caption("ระบบคำนวณความสอดคล้องสองตลาด + คัดกรองกับดักราคาต่อลึก (Universal Smart Edge)")

# --- 1. ระบุชื่อทีม ---
st.subheader("📌 1. ระบุชื่อทีม")
c_t1, c_t2 = st.columns(2)
with c_t1:
    team_home = st.text_input("ทีมเหย้า", value="เจ้าบ้าน")
with c_t2:
    team_away = st.text_input("ทีมเยือน", value="ทีมเยือน")

st.markdown("---")

# ฟังก์ชันแปลงสตริงราคาเป็น float (รองรับ 0-0.5, 0.25, 2.5-3 ฯลฯ)
def parse_handicap(h_str):
    h_str = str(h_str).strip()
    if not h_str or h_str == "0":
        return 0.0
    mapping = {
        "0-0.5": 0.25, "0.25": 0.25,
        "0.5": 0.5,
        "0.5-1": 0.75, "0.75": 0.75,
        "1": 1.0,
        "1-1.5": 1.25, "1.25": 1.25,
        "1.5": 1.5,
        "1.5-2": 1.75, "1.75": 1.75,
        "2": 2.0,
        "2-2.5": 2.25, "2.25": 2.25,
        "2.5": 2.5,
        "2.5-3": 2.75, "2.75": 2.75,
        "3": 3.0,
        "3-3.5": 3.25, "3.25": 3.25,
        "3.5": 3.5
    }
    return mapping.get(h_str, float(h_str) if h_str.replace('.', '', 1).isdigit() else 0.0)

# --- 2. แฮนดิแคป (3 แถว) ---
st.subheader("🎯 2. ราคาต่อรอง แฮนดิแคป (3 แถว)")
st.caption("เลือกฝั่งต่อ / ใส่เรตแต้มต่อ / ค่าน้ำทั้งสองฝั่ง")

h_cols = st.columns(3)
h_data = []

for i, col in enumerate(h_cols):
    with col:
        fav = st.selectbox(f"ฝั่งต่อ (แถว {i+1})", [f"{team_home} ต่อ", f"{team_away} ต่อ", "เสมอ (0)"], key=f"fav_{i}")
        h_val_raw = st.text_input(f"แต้มต่อ แถว {i+1} (เช่น 0.5, 0-0.5, 1.25)", value="0.5" if i==0 else ("0-0.5" if i==1 else "0.5-1"), key=f"h_val_{i}")
        odds_home = st.number_input(f"น้ำ {team_home} ({i+1})", value=1.90, step=0.01, key=f"oh_{i}")
        odds_away = st.number_input(f"น้ำ {team_away} ({i+1})", value=2.00, step=0.01, key=f"oa_{i}")
        
        parsed_val = parse_handicap(h_val_raw)
        if "เสมอ" in fav:
            signed_h = 0.0
        elif f"{team_home} ต่อ" in fav:
            signed_h = -parsed_val # เจ้าบ้านต่อ ติดลบ
        else:
            signed_h = parsed_val  # ทีมเยือนต่อ เป็นบวก
            
        h_data.append({
            "fav": fav,
            "val_raw": h_val_raw,
            "parsed_val": parsed_val,
            "signed_h": signed_h,
            "odds_h": odds_home,
            "odds_a": odds_away
        })

st.markdown("---")

# --- 3. สูง-ต่ำ (3 แถว) ---
st.subheader("⚽ 3. ราคาสูง-ต่ำ (Over / Under 3 แถว)")
ou_cols = st.columns(3)
ou_data = []

for i, col in enumerate(ou_cols):
    with col:
        ou_val_raw = st.text_input(f"เรต สูงต่ำ แถว {i+1} (เช่น 2.5, 2-2.5, 3.0)", value="2.5" if i==0 else ("2-2.5" if i==1 else "2.5-3"), key=f"ou_val_{i}")
        odds_o = st.number_input(f"น้ำ สูง (Over {i+1})", value=1.92, step=0.01, key=f"oo_{i}")
        odds_u = st.number_input(f"น้ำ ต่ำ (Under {i+1})", value=1.98, step=0.01, key=f"ou_{i}")
        
        ou_data.append({
            "val_raw": ou_val_raw,
            "parsed_val": parse_handicap(ou_val_raw),
            "odds_o": odds_o,
            "odds_u": odds_u
        })

st.markdown("---")

# --- กลไกคำนวณอัจฉริยะ Pro V5 Engine ---
if st.button("🚀 ประมวลผลและชี้เป้าทีเด็ด (Pro V5)", use_container_width=True):
    # 1. วิเคราะห์แฮนดิแคปหลัก
    main_h = h_data[0]
    main_ou = ou_data[0]
    
    # คำนวณ Implied Probability แบบตัด Margin ต๋ง
    prob_h_raw = 1.0 / main_h["odds_h"]
    prob_a_raw = 1.0 / main_h["odds_a"]
    h_margin = prob_h_raw + prob_a_raw
    fair_prob_h = prob_h_raw / h_margin
    fair_prob_a = prob_a_raw / h_margin

    prob_o_raw = 1.0 / main_ou["odds_o"]
    prob_u_raw = 1.0 / main_ou["odds_u"]
    ou_margin = prob_o_raw + prob_u_raw
    fair_prob_o = prob_o_raw / ou_margin
    fair_prob_u = prob_u_raw / ou_margin

    abs_handicap = main_h["parsed_val"]
    is_home_fav = main_h["signed_h"] < 0
    is_away_fav = main_h["signed_h"] > 0
    fav_team_name = team_home if is_home_fav else (team_away if is_away_fav else "ไม่มี (หน้าเสมอ)")
    underdog_team_name = team_away if is_home_fav else team_home

    # 2. ตรวจสอบกับดักต่อลึก (Trap Detection)
    is_heavy_trap = abs_handicap >= 1.75
    
    # 3. ตรวจสอบความสอดคล้องของตลาด (Coherence vs Divergence)
    divergence = False
    coherence = False
    
    # ต่อลึกแต่สกอร์รวมเปิดต่ำ = ตลาดขัดแย้ง (ต่อไม่ยอมยิง)
    if abs_handicap >= 1.0 and main_ou["parsed_val"] <= 2.25:
        divergence = True
    # ต่อบางแต่สกอร์รวมสูงจัด = ตลาดสวนทาง
    elif abs_handicap <= 0.25 and main_ou["parsed_val"] >= 3.0:
        divergence = True
    # บอลทิศทางเดียวกัน: ต่อกำลังดี + สกอร์สูงรับ
    elif (0.5 <= abs_handicap <= 1.5) and (fair_prob_o >= 0.52 and main_ou["parsed_val"] >= 2.5):
        coherence = True
    # บอลสายเหนียว: สูสี + สกอร์ต่ำรับชัดเจน
    elif abs_handicap <= 0.5 and (fair_prob_u >= 0.53 and main_ou["parsed_val"] <= 2.25):
        coherence = True

    # 4. ชี้เป้าตัวเลือกการลงทุน (Selection Engine)
    best_pick = ""
    best_rate = ""
    confidence = 50.0
    reasoning = ""
    trap_warning = ""

    if is_heavy_trap:
        # กรณีเจอบอลต่อ 2.0, 2.5, 3.0+
        confidence = 52.0
        trap_warning = f"⚠️ ตรวจพบกับดักบอลต่อลึก (Heavy Handicap Trap): {fav_team_name} ต่อถึง {abs_handicap} ลูก เสี่ยงชนะในสนามแต่แพ้ราคาต่อรองสูงมาก"
        best_pick = f"เลี่ยงลงทุนฝั่งต่อ หรือ พิจารณารอง {underdog_team_name} (+{abs_handicap})"
        best_rate = f"รอง {underdog_team_name} เรตแต้มหนา"
        reasoning = "สถิติในระยะยาว บอลต่อเกิน 1.75 ลูก อัตราแพ้แต้มต่อสูงเกิน 55% เนื่องจากทีมมักผ่อนเกมหลังนำขาด"
    
    elif divergence:
        confidence = 54.5
        trap_warning = "⚠️ ตลาดขัดแย้งกัน (Divergence): อัตราต่อรองและสกอร์รวมส่งสัญญาณขัดกัน ไม่คุ้มค่าเสี่ยง"
        best_pick = "ข้ามคู่นี้ทันที (ห้ามใส่สเต็ป)"
        best_rate = "ไม่แนะนำให้วางเดิมพัน"
        reasoning = "ตลาดแฮนดิแคปกับสูงต่ำไม่สนับสนุนกัน ค่าน้ำมีความผันผวนสูง"

    else:
        # วิเคราะห์บอลเรตปกติ (0 ถึง 1.5)
        if coherence and abs_handicap <= 0.5 and fair_prob_u > 0.52:
            # สูตรบอลรองกินเต็ม / บอลสกอร์ต่ำ
            confidence = round(75.0 + (fair_prob_u * 15.0), 1)
            best_pick = f"วาง รอง {underdog_team_name}"
            best_rate = f"รอง {underdog_team_name} (+{abs_handicap})"
            reasoning = "เรตเปิดสูสีและตลาดโน้มเอียงไปทางสกอร์ต่ำ บอลรองถือความได้เปรียบสูงมาก หากเจ๊ากินเต็ม/กินครึ่ง"
        
        elif coherence and is_home_fav and fair_prob_h > 0.52:
            # ต่อในบ้านกำลังดี
            confidence = round(74.0 + (fair_prob_h * 14.0), 1)
            best_pick = f"วาง {team_home} (ต่อในบ้าน)"
            best_rate = f"ต่อ {team_home} (-{abs_handicap})"
            reasoning = "เจ้าบ้านต่อในเรตกำลังพอดี ตลาดสูงต่ำรองรับชัดเจน มีโอกาสบดคว้าชัยได้ตามเป้า"

        elif fair_prob_a > 0.53 and abs_handicap <= 0.5:
            # บอลเยือนรองเหนียว
            confidence = round(73.0 + (fair_prob_a * 14.0), 1)
            best_pick = f"วาง รอง {team_away}"
            best_rate = f"รอง {team_away} (+{abs_handicap})"
            reasoning = "ทีมเยือนได้แต้มต่อ มีเกราะกำบังราคาที่ดี ค่าน้ำสมเหตุสมผล"
        
        else:
            # ค่าน้ำก้ำกึ่ง
            confidence = 62.0
            best_pick = f"พิจารณา {fav_team_name if fair_prob_h > fair_prob_a else underdog_team_name}"
            best_rate = f"เรตแถว 1 ({main_h['val_raw']})"
            reasoning = "ค่าน้ำยังแบ่งรับแบ่งสู้ ความได้เปรียบไม่ขาด ควรเลี่ยงสเต็ป"

    confidence = min(88.0, max(45.0, confidence))

    # --- แสดงผลสรุป ---
    st.subheader("🏆 ผลสรุปฟันธงระดับมืออาชีพ (Pro Pick V5)")
    
    if confidence >= 75.0:
        st.success(f"🎯 **แนะนำการลงทุนที่ดีที่สุด:** {best_pick}")
    elif confidence >= 65.0:
        st.info(f"💡 **แนะนำการลงทุน:** {best_pick}")
    else:
        st.warning(f"⛔ **คำแนะนำ:** {best_pick}")

    st.write(f"👉 **ราคาที่น่าสนใจที่สุด:** {best_rate}")
    st.write(f"📈 **ระดับความน่าลงทุน (เปอร์เซ็นต์ชนะ):** **{confidence}%**")
    
    if trap_warning:
        st.warning(trap_warning)
        
    st.info(f"💡 **เหตุผลเชิงลึก:** {reasoning}")
    
    # กล่องตรวจสอบค่าความน่าจะเป็นจริง
    with st.expander("📊 ตรวจสอบค่าความน่าจะเป็นคำนวณจริง (Fair Implied Odds)"):
        st.write(f"- ความน่าจะเป็น {team_home}: `{round(fair_prob_h*100, 1)}%` (ค่าน้ำจริง {main_h['odds_h']})")
        st.write(f"- ความน่าจะเป็น {team_away}: `{round(fair_prob_a*100, 1)}%` (ค่าน้ำจริง {main_h['odds_a']})")
        st.write(f"- ความน่าจะเป็น สกอร์สูง: `{round(fair_prob_o*100, 1)}%` | สกอร์ต่ำ: `{round(fair_prob_u*100, 1)}%`")

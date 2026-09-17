import streamlit as st

st.set_page_config(page_title="Odds Analyzer Pro V10.3", page_icon="⚽", layout="centered")

st.title("⚽ เครื่องมือวิเคราะห์ราคาบอล (Pro V10.3)")
st.caption("ระบบคำนวณ 2 หรือ 3 แถวราคา พร้อมเปรียบเทียบ แฮนดิแคป vs สูงต่ำ ชี้เป้าตัวที่ดีที่สุด")

# ตัวเลือกเรตราคามาตรฐาน
HDP_OPTIONS = [
    "เสมอ (0)", "0-0.5 (เสมอควบครึ่ง)", "0.5 (ครึ่งลูก)", 
    "0.5-1 (ครึ่งควบลูก)", "1.0 (หนึ่งลูก)", "1-1.5 (ลูกควบลูกครึ่ง)", 
    "1.5 (ลูกครึ่ง)", "1.5-2 (ลูกครึ่งควบสอง)", "2.0 (สองลูก)"
]

OU_OPTIONS = [
    "1.5-2 (ลูกครึ่งควบสอง)", "2.0 (สองลูก)", "2-2.5 (สองควบสองครึ่ง)",
    "2.5 (สองลูกครึ่ง)", "2.5-3 (สองครึ่งควบสาม)", "3.0 (สามลูก)", "3-3.5 (สามควบสามครึ่ง)"
]

# 1. ข้อมูลคู่แข่งขัน
st.subheader("📌 1. ข้อมูลคู่แข่งขัน")
col_t1, col_t2 = st.columns(2)
with col_t1:
    home_name = st.text_input("ทีมเหย้า (ฝั่งซ้าย)", value="เจ้าบ้าน")
with col_t2:
    away_name = st.text_input("ทีมเยือน (ฝั่งขวา)", value="ทีมเยือน")

num_rows = st.radio("จำนวนแถวราคาที่ต้องการกรอก:", [2, 3], horizontal=True, index=0)

st.markdown("---")

# 2. แฮนดิแคป
st.subheader("🎯 2. ราคาแฮนดิแคป (HDP)")
h_fav = st.radio("ทีมต่อในแถวหลัก:", [f"{home_name} ต่อ", f"{away_name} ต่อ", "เสมอ (0)"], horizontal=True)

h_rates, h_lefts, h_rights = [], [], []
for i in range(num_rows):
    st.markdown(f"**แถวที่ {i+1} {'(ราคาหลัก - น้ำหนักสำคัญ)' if i==0 else '(ราคารอง)'}**")
    hr = st.selectbox(f"เรตแต้มต่อ แถว {i+1}", HDP_OPTIONS, index=2 if i==0 else 1, key=f"hr_{i}")
    c_l, c_r = st.columns(2)
    with c_l:
        hl = st.number_input(f"น้ำ {home_name} ({i+1})", value=1.85 if i==0 else 2.10, step=0.01, key=f"hl_{i}")
    with c_r:
        hr_val = st.number_input(f"น้ำ {away_name} ({i+1})", value=2.05 if i==0 else 1.80, step=0.01, key=f"hri_{i}")
    h_rates.append(hr)
    h_lefts.append(hl)
    h_rights.append(hr_val)

st.markdown("---")

# 3. สูง-ต่ำ
st.subheader("⚽ 3. ราคาสูง-ต่ำ (Over / Under)")
ou_rates, ou_overs, ou_unders = [], [], []
for i in range(num_rows):
    st.markdown(f"**แถวที่ {i+1} {'(ราคาหลัก)' if i==0 else '(ราคารอง)'}**")
    our = st.selectbox(f"เรต สูง-ต่ำ แถว {i+1}", OU_OPTIONS, index=3 if i==0 else 2, key=f"our_{i}")
    c_o, c_u = st.columns(2)
    with c_o:
        oo = st.number_input(f"น้ำ สูง ({i+1})", value=1.95 if i==0 else 1.75, step=0.01, key=f"oo_{i}")
    with c_u:
        ou = st.number_input(f"น้ำ ต่ำ ({i+1})", value=1.95 if i==0 else 2.15, step=0.01, key=f"ou_{i}")
    ou_rates.append(our)
    ou_overs.append(oo)
    ou_unders.append(ou)

st.markdown("---")

def evaluate_market(left_odds, right_odds, n_rows):
    weights = [0.65, 0.35] if n_rows == 2 else [0.50, 0.25, 0.25]
    tot_l, tot_r = 0.0, 0.0
    for i in range(n_rows):
        ol, or_ = left_odds[i], right_odds[i]
        pl = (1 / ol) * 100 if ol > 0 else 0
        pr = (1 / or_) * 100 if or_ > 0 else 0
        sum_p = pl + pr
        fl = (pl / sum_p) * 100
        fr = (pr / sum_p) * 100
        
        bonus_l = 3.0 if ol <= 1.78 else 0.0
        bonus_r = 3.0 if or_ <= 1.78 else 0.0
        
        adj_l = fl + bonus_l
        adj_r = fr + bonus_r
        norm_l = (adj_l / (adj_l + adj_r)) * 100
        norm_r = (adj_r / (adj_l + adj_r)) * 100
        
        tot_l += norm_l * weights[i]
        tot_r += norm_r * weights[i]
        
    diff = abs(tot_l - tot_r)
    conf = min(88.0, 50.0 + (diff * 2.2))
    return tot_l, tot_r, diff, conf

if st.button("🚀 วิเคราะห์ความได้เปรียบ 2 ตลาด", use_container_width=True):
    # คำนวณ HDP
    hl_tot, hr_tot, diff_h, conf_h = evaluate_market(h_lefts, h_rights, num_rows)
    target_hdp = home_name if hl_tot > hr_tot else away_name
    pick_hdp = f"{target_hdp} ({h_rates[0]})"
    
    # คำนวณ OU
    oo_tot, ou_tot, diff_ou, conf_ou = evaluate_market(ou_overs, ou_unders, num_rows)
    target_ou = "สูง (Over)" if oo_tot > ou_tot else "ต่ำ (Under)"
    pick_ou = f"{target_ou} ({ou_rates[0]})"
    
    # เปรียบเทียบหา Best Value Pick
    if conf_ou > conf_h:
        best_market = "ราคาสูง-ต่ำ"
        best_pick = pick_ou
        best_conf = conf_ou
    else:
        best_market = "ราคาแฮนดิแคป"
        best_pick = pick_hdp
        best_conf = conf_h
        
    st.subheader("🏆 ชี้เป้าตัวที่น่าลงทุนที่สุด (Best Pick)")
    
    if best_conf >= 70.0:
        grade = "🟢 เกรด A (มั่นใจสูง ค่าน้ำได้เปรียบชัด)"
        st.success(f"### 👉 แนะนำเล่น: **[{best_pick}]**")
    elif best_conf >= 60.0:
        grade = "🔵 เกรด B (น่าลงทุนเฉพาะเต็งเดี่ยว)"
        st.info(f"### 👉 แนะนำเล่น: **[{best_pick}]**")
    else:
        grade = "🟡 เกรด C (ราคาก้ำกึ่ง โต๊ะบาลานซ์น้ำมาดี)"
        st.warning(f"### ⚠️ ราคาก้ำกึ่ง: **[{best_pick}]**")
        
    st.write(f"📊 **ประเภทราคาที่ดีที่สุด:** {best_market}")
    st.write(f"📈 **ดัชนีความได้เปรียบ:** `{best_conf:.1f}%` ({grade})")
    
    st.markdown("---")
    st.subheader("🔍 สรุปเปรียบเทียบทั้ง 2 หน้าเล่น")
    c_res1, c_res2 = st.columns(2)
    with c_res1:
        st.markdown(f"**ฝั่งแฮนดิแคป:**")
        st.write(f"- ตัวเลือก: **{pick_hdp}**")
        st.write(f"- ความได้เปรียบ: **{conf_h:.1f}%**")
    with c_res2:
        st.markdown(f"**ฝั่งสูง-ต่ำ:**")
        st.write(f"- ตัวเลือก: **{pick_ou}**")
        st.write(f"- ความได้เปรียบ: **{conf_ou:.1f}%**")

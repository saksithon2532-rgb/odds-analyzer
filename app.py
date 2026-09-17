import streamlit as st

st.set_page_config(page_title="Pro Odds Analyzer V8 (Dual Engine)", page_icon="⚽", layout="centered")

st.title("⚽ เครื่องมือวิเคราะห์บอลคู่ (Pro V8 - Smart Decision)")
st.caption("ระบบ Dual Engine: ชั่งน้ำหนักอัตโนมัติระหว่าง 'แฮนดิแคป' กับ 'สูง-ต่ำ' ตัวไหนคมกว่าชี้เป้าตัวนั้น")

def calc_probs(odds_l, odds_r):
    prob_l = (1.0 / odds_l) * 100.0 if odds_l > 0 else 0.0
    prob_r = (1.0 / odds_r) * 100.0 if odds_r > 0 else 0.0
    fair_l = (prob_l / (prob_l + prob_r)) * 100.0 if (prob_l + prob_r) > 0 else 50.0
    fair_r = (prob_r / (prob_l + prob_r)) * 100.0 if (prob_l + prob_r) > 0 else 50.0
    
    # โบนัสน้ำไหล (ค่าน้ำบีบจ่ายต่ำ)
    bonus_l = 3.5 if (0 < odds_l <= 1.80) else 0.0
    bonus_r = 3.5 if (0 < odds_r <= 1.80) else 0.0
    
    tot_l = fair_l + bonus_l
    tot_r = fair_r + bonus_r
    norm_l = (tot_l / (tot_l + tot_r)) * 100.0
    norm_r = (tot_r / (tot_l + tot_r)) * 100.0
    return norm_l, norm_r

# --- 1. ระบุชื่อทีม ---
st.subheader("📌 1. ระบุชื่อทีม")
c_t1, c_t2 = st.columns(2)
with c_t1:
    team_home = st.text_input("ทีมเหย้า (ฝั่งซ้าย)", value="โอลิมปิคโคเปนฮาเก้น")
with c_t2:
    team_away = st.text_input("ทีมเยือน (ฝั่งขวา)", value="เซลต้าบีโก้")

st.markdown("---")

# --- 2. แฮนดิแคป ---
st.subheader("🎯 2. ราคาต่อรอง แฮนดิแคป (3 แถว)")
side_opts = ["เจ้าบ้านต่อ", "ทีมเยือนต่อ", "เสมอ (0)"]

col_h1, col_h2, col_h3 = st.columns(3)
with col_h1:
    st.markdown("**แถว 1 (หลัก)**")
    side_1 = st.selectbox("ฝั่งต่อ (1)", side_opts, index=1, key="s1")
    h_rate1 = st.text_input("แต้มต่อ (1)", value="0.5", key="hr1")
    h_l1 = st.number_input(f"น้ำ {team_home} (1)", value=2.11, step=0.01, key="hl1")
    h_r1 = st.number_input(f"น้ำ {team_away} (1)", value=1.83, step=0.01, key="hr_1")

with col_h2:
    st.markdown("**แถว 2**")
    side_2 = st.selectbox("ฝั่งต่อ (2)", side_opts, index=1, key="s2")
    h_rate2 = st.text_input("แต้มต่อ (2)", value="0.5-1", key="hr2")
    h_l2 = st.number_input(f"น้ำ {team_home} (2)", value=1.82, step=0.01, key="hl2")
    h_r2 = st.number_input(f"น้ำ {team_away} (2)", value=2.10, step=0.01, key="hr_2")

with col_h3:
    st.markdown("**แถว 3**")
    side_3 = st.selectbox("ฝั่งต่อ (3)", side_opts, index=1, key="s3")
    h_rate3 = st.text_input("แต้มต่อ (3)", value="0-0.5", key="hr3")
    h_l3 = st.number_input(f"น้ำ {team_home} (3)", value=2.46, step=0.01, key="hl3")
    h_r3 = st.number_input(f"น้ำ {team_away} (3)", value=1.60, step=0.01, key="hr_3")

st.markdown("---")

# --- 3. สูง-ต่ำ ---
st.subheader("⚽ 3. ราคาสูง-ต่ำ (3 แถว)")
col_u1, col_u2, col_u3 = st.columns(3)
with col_u1:
    st.markdown("**สูงต่ำ แถว 1 (หลัก)**")
    ou_rate1 = st.text_input("เรต สูงต่ำ (1)", value="2-2.5", key="our1")
    ou_o1 = st.number_input("น้ำ สูง (1)", value=1.83, step=0.01, key="ouo1")
    ou_u1 = st.number_input("น้ำ ต่ำ (1)", value=2.06, step=0.01, key="ouu1")

with col_u2:
    st.markdown("**สูงต่ำ แถว 2**")
    ou_rate2 = st.text_input("เรต สูงต่ำ (2)", value="2.5", key="our2")
    ou_o2 = st.number_input("น้ำ สูง (2)", value=2.12, step=0.01, key="ouo2")
    ou_u2 = st.number_input("น้ำ ต่ำ (2)", value=1.78, step=0.01, key="ouu2")

with col_u3:
    st.markdown("**สูงต่ำ แถว 3**")
    ou_rate3 = st.text_input("เรต สูงต่ำ (3)", value="2", key="our3")
    ou_o3 = st.number_input("น้ำ สูง (3)", value=1.59, step=0.01, key="ouo3")
    ou_u3 = st.number_input("น้ำ ต่ำ (3)", value=2.42, step=0.01, key="ouu3")

st.markdown("---")

if st.button("🚀 ประมวลผลและชี้เป้าทีเด็ด (Dual Engine)", use_container_width=True):
    weights = [0.50, 0.25, 0.25]
    
    # 1. วิเคราะห์แฮนดิแคป
    h_l = [h_l1, h_l2, h_l3]
    h_r = [h_r1, h_r2, h_r3]
    tot_hl, tot_hr = 0.0, 0.0
    for i in range(3):
        pl, pr = calc_probs(h_l[i], h_r[i])
        tot_hl += pl * weights[i]
        tot_hr += pr * weights[i]
        
    diff_h = abs(tot_hl - tot_hr)
    conf_h = min(88.0, 50.0 + (diff_h * 1.6))
    
    if side_1 == "เจ้าบ้านต่อ":
        lbl_h_main = f"ต่อ {team_home} ({h_rate1})" if tot_hl > tot_hr else f"รอง {team_away} (+{h_rate1})"
    elif side_1 == "ทีมเยือนต่อ":
        lbl_h_main = f"รอง {team_home} (+{h_rate1})" if tot_hl > tot_hr else f"ต่อ {team_away} ({h_rate1})"
    else:
        lbl_h_main = f"วาง {team_home} (0.0)" if tot_hl > tot_hr else f"วาง {team_away} (0.0)"
        
    # 2. วิเคราะห์สูง-ต่ำ
    ou_o = [ou_o1, ou_o2, ou_o3]
    ou_u = [ou_u1, ou_u2, ou_u3]
    tot_oo, tot_ou = 0.0, 0.0
    for i in range(3):
        po, pu = calc_probs(ou_o[i], ou_u[i])
        tot_oo += po * weights[i]
        tot_ou += pu * weights[i]
        
    diff_ou = abs(tot_oo - tot_ou)
    conf_ou = min(88.0, 50.0 + (diff_ou * 1.6))
    lbl_ou_main = f"สูง {ou_rate1}" if tot_oo > tot_ou else f"ต่ำ {ou_rate1}"
    
    # 3. Decision Engine: ตัวไหนคะแนนสูงกว่า เลือกตัวนั้น
    st.subheader("🏆 ผลสรุปฟันธงระดับมืออาชีพ (Pro V8)")
    
    if conf_ou > conf_h and conf_ou >= 68.0:
        # ตลาดสูง-ต่ำได้เปรียบกว่าแฮนดิแคป
        target_market = "ราคาสูง-ต่ำ (Total Goals)"
        final_pick = f"วาง {lbl_ou_main}"
        final_conf = conf_ou
        reason = f"ตลาดสูง-ต่ำมีทิศทางน้ำชัดเจนกว่าแฮนดิแคป (ค่าน้ำฝั่ง {'สูง' if tot_oo > tot_ou else 'ต่ำ'} ไหลเอื้อมาก)"
    else:
        # ตลาดแฮนดิแคปได้เปรียบกว่า
        target_market = "ราคาแฮนดิแคป (Handicap)"
        final_pick = f"วาง {lbl_h_main}"
        final_conf = conf_h
        reason = f"ตลาดแต้มต่อแฮนดิแคปมีความได้เปรียบชัดเจนกว่าราคาผลรวมประตู"

    if final_conf >= 75.0:
        st.success(f"🎯 **คำแนะนำ:** **{final_pick}**")
        badge = "🟢 เล่นได้ทั้งบอลเต็งและสเต็ป (เกรด A)"
    elif final_conf >= 68.0:
        st.info(f"🎯 **คำแนะนำ:** **{final_pick}**")
        badge = "🔵 เหมาะสำหรับบอลเต็งเดี่ยวเท่านั้น (เกรด B)"
    else:
        st.warning(f"⚠️ **คำแนะนำ:** **{final_pick}** (ความได้เปรียบไม่ขาด)")
        badge = "🟡 ตลาดก้ำกึ่ง ห้ามใส่สเต็ปเด็ดขาด"

    st.markdown(f"📊 **ประเภทราคาที่เลือกเล่น:** **{target_market}**")
    st.markdown(f"📈 **ระดับความมั่นใจ:** **`{final_conf:.1f}%`** ({badge})")
    st.caption(f"💡 **เหตุผลเชิงลึก:** {reason}")
    
    with st.expander("🔍 ดูคะแนนเปรียบเทียบทั้ง 2 ตลาด"):
        st.write(f"- แฮนดิแคป: **{lbl_h_main}** (มั่นใจ {conf_h:.1f}%)")
        st.write(f"- สูง-ต่ำ: **{lbl_ou_main}** (มั่นใจ {conf_ou:.1f}%)")

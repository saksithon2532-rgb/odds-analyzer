import streamlit as st

st.set_page_config(page_title="Pro Odds Analyzer V10 (Calibrated)", page_icon="⚽", layout="centered")

st.title("⚽ เครื่องมือวิเคราะห์บอลคู่ (Pro V10 - ปรับจูนความไวค่าน้ำ)")
st.caption("สูตรคำนวณแบบ Calibrated Edge Scale: ตรวจจับค่าน้ำไหลและปลดล็อกระดับ 70%-80%+ ตามความได้เปรียบจริง")

def calc_probs(odds_l, odds_r):
    if odds_l <= 0 or odds_r <= 0:
        return 50.0, 50.0
    prob_l = (1.0 / odds_l) * 100.0
    prob_r = (1.0 / odds_r) * 100.0
    sum_p = prob_l + prob_r
    fair_l = (prob_l / sum_p) * 100.0
    fair_r = (prob_r / sum_p) * 100.0
    
    # โบนัสน้ำบีบจริงในตลาดเอเชีย
    bonus_l = 4.5 if odds_l <= 1.80 else (2.0 if odds_l <= 1.85 else 0.0)
    bonus_r = 4.5 if odds_r <= 1.80 else (2.0 if odds_r <= 1.85 else 0.0)
    
    tot_l = fair_l + bonus_l
    tot_r = fair_r + bonus_r
    norm_l = (tot_l / (tot_l + tot_r)) * 100.0
    norm_r = (tot_r / (tot_l + tot_r)) * 100.0
    return norm_l, norm_r

def get_weights(num_rows):
    if num_rows == 2:
        return [0.65, 0.35]
    elif num_rows == 3:
        return [0.50, 0.25, 0.25]
    else:
        return [0.45, 0.25, 0.15, 0.15]

# --- 1. ระบุชื่อทีม ---
st.subheader("📌 1. ข้อมูลคู่แข่งขัน")
c_t1, c_t2 = st.columns(2)
with c_t1:
    team_home = st.text_input("ทีมเหย้า (ฝั่งซ้าย)", value="เจ้าบ้าน")
with c_t2:
    team_away = st.text_input("ทีมเยือน (ฝั่งขวา)", value="ทีมเยือน")

st.markdown("---")

# --- 2. แฮนดิแคป ---
st.subheader("🎯 2. ราคาต่อรอง แฮนดิแคป")
num_h_rows = st.radio("เลือกจำนวนแถวราคาแฮนดิแคป", [2, 3, 4], index=0, horizontal=True)

side_opts = ["เจ้าบ้านต่อ", "ทีมเยือนต่อ", "เสมอ (0)"]
h_sides, h_rates, h_lefts, h_rights = [], [], [], []
h_cols = st.columns(num_h_rows)

default_sides = [0, 0, 0, 0]
default_rates = ["0.5", "0.5-1", "0-0.5", "1"]
default_l = [1.80, 2.10, 1.65, 2.35]
default_r = [2.08, 1.80, 2.30, 1.60]

for idx in range(num_h_rows):
    with h_cols[idx]:
        st.markdown(f"**แถวที่ {idx+1} {'(หลัก)' if idx==0 else ''}**")
        s = st.selectbox(f"ฝั่งต่อ ({idx+1})", side_opts, index=default_sides[idx], key=f"hs_{idx}")
        r = st.text_input(f"แต้มต่อ ({idx+1})", value=default_rates[idx], key=f"hr_{idx}")
        l = st.number_input(f"น้ำ {team_home} ({idx+1})", value=default_l[idx], step=0.01, key=f"hl_{idx}")
        ri = st.number_input(f"น้ำ {team_away} ({idx+1})", value=default_r[idx], step=0.01, key=f"hri_{idx}")
        h_sides.append(s)
        h_rates.append(r)
        h_lefts.append(l)
        h_rights.append(ri)

st.markdown("---")

# --- 3. สูง-ต่ำ ---
st.subheader("⚽ 3. ราคาสูง-ต่ำ")
num_ou_rows = st.radio("เลือกจำนวนแถวราคาสูง-ต่ำ", [2, 3, 4], index=0, horizontal=True)

ou_rates, ou_overs, ou_unders = [], [], []
ou_cols = st.columns(num_ou_rows)

default_ou_rates = ["2.5", "2.5-3", "2-2.5", "3"]
default_o = [2.10, 2.35, 1.80, 2.50]
default_u = [1.80, 1.60, 2.10, 1.50]

for idx in range(num_ou_rows):
    with ou_cols[idx]:
        st.markdown(f"**แถวที่ {idx+1} {'(หลัก)' if idx==0 else ''}**")
        r = st.text_input(f"เรต สูงต่ำ ({idx+1})", value=default_ou_rates[idx], key=f"our_{idx}")
        o = st.number_input(f"น้ำ สูง ({idx+1})", value=default_o[idx], step=0.01, key=f"ouo_{idx}")
        u = st.number_input(f"น้ำ ต่ำ ({idx+1})", value=default_u[idx], step=0.01, key=f"ouu_{idx}")
        ou_rates.append(r)
        ou_overs.append(o)
        ou_unders.append(u)

st.markdown("---")

if st.button("🚀 ประมวลผลและชี้เป้าทีเด็ด (Pro V10)", use_container_width=True):
    # คำนวณแฮนดิแคป
    w_h = get_weights(num_h_rows)
    tot_hl, tot_hr = 0.0, 0.0
    for i in range(num_h_rows):
        pl, pr = calc_probs(h_lefts[i], h_rights[i])
        tot_hl += pl * w_h[i]
        tot_hr += pr * w_h[i]
        
    diff_h = abs(tot_hl - tot_hr)
    # Calibrated Scale: ปรับตัวคูณเป็น 2.45 เพื่อสะท้อนขอบเขต 50% - 85% ได้แม่นยำจริง
    conf_h = min(88.0, 50.0 + (diff_h * 2.45))
    
    main_side = h_sides[0]
    main_rate = h_rates[0]
    if main_side == "เจ้าบ้านต่อ":
        lbl_h_main = f"ต่อ {team_home} ({main_rate})" if tot_hl > tot_hr else f"รอง {team_away} (+{main_rate})"
    elif main_side == "ทีมเยือนต่อ":
        lbl_h_main = f"รอง {team_home} (+{main_rate})" if tot_hl > tot_hr else f"ต่อ {team_away} ({main_rate})"
    else:
        lbl_h_main = f"วาง {team_home} (0.0)" if tot_hl > tot_hr else f"วาง {team_away} (0.0)"

    # คำนวณสูง-ต่ำ
    w_ou = get_weights(num_ou_rows)
    tot_oo, tot_ou = 0.0, 0.0
    for i in range(num_ou_rows):
        po, pu = calc_probs(ou_overs[i], ou_unders[i])
        tot_oo += po * w_ou[i]
        tot_ou += pu * w_ou[i]
        
    diff_ou = abs(tot_oo - tot_ou)
    conf_ou = min(88.0, 50.0 + (diff_ou * 2.45))
    lbl_ou_main = f"สูง {ou_rates[0]}" if tot_oo > tot_ou else f"ต่ำ {ou_rates[0]}"
    
    # เลือกระหว่างสองตลาด
    st.subheader("🏆 ผลสรุปฟันธงระดับมืออาชีพ (Pro V10)")
    
    if conf_ou > conf_h and conf_ou >= 68.0:
        target_market = "ราคาสูง-ต่ำ (Total Goals)"
        final_pick = f"วาง {lbl_ou_main}"
        final_conf = conf_ou
        reason = f"ตลาดสูง-ต่ำมีความชัดเจนกว่า (ค่าน้ำฝั่ง {'สูง' if tot_oo > tot_ou else 'ต่ำ'} จ่ายต่ำและมีความได้เปรียบสูง)"
    else:
        target_market = "ราคาแฮนดิแคป (Handicap)"
        final_pick = f"วาง {lbl_h_main}"
        final_conf = conf_h
        reason = "ตลาดแฮนดิแคปมีความได้เปรียบชัดเจนกว่าราคาผลรวมสกอร์"

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

import streamlit as st

def calculate_bmr(gender, weight, height, age):
    if gender == "ชาย":
        return 66 + (13.7 * weight) + (5 * height) - (6.8 * age)
    else:
        return 655 + (9.6 * weight) + (1.8 * height) - (4.7 * age)

activity_levels = {
    "ไม่ออกกำลังกายเลย": 1.2,
    "ออกกำลังกายเล็กน้อย (1-2 วัน/สัปดาห์)": 1.375,
    "ออกกำลังกายปานกลาง (3-5 วัน/สัปดาห์)": 1.55,
    "ออกกำลังกายหนัก (6-7 วัน/สัปดาห์)": 1.725,
    "ออกกำลังกายหนักมาก + ทำงานใช้แรง": 1.9
}

st.title("🔥 โปรแกรมคำนวณพลังงานที่ใช้ในแต่ละวัน (BMR & TDEE)")

gender = st.radio("เพศ", ["ชาย", "หญิง"])
age = st.number_input("อายุ (ปี)", min_value=10, max_value=100, value=25)
weight = st.number_input("น้ำหนัก (กก.)", min_value=1.0, max_value=300.0, step=0.1)
height = st.number_input("ส่วนสูง (ซม.)", min_value=50.0, max_value=250.0, step=0.1)
activity = st.selectbox("ระดับการออกกำลังกาย", list(activity_levels.keys()))

# เพิ่มตัวเลือกเป้าหมายการเปลี่ยนน้ำหนักต่อสัปดาห์
st.markdown("---")
st.subheader("🎯 เป้าหมายการเปลี่ยนน้ำหนัก")
goal_type = st.radio("เป้าหมาย", ["ลดน้ำหนัก", "เพิ่มน้ำหนัก", "รักษาน้ำหนัก"])
kg_per_week = 0.0
if goal_type != "รักษาน้ำหนัก":
    kg_per_week = st.selectbox(
        "ต้องการ{}น้ำหนักกี่กิโลกรัมต่อสัปดาห์?".format("ลด" if goal_type=="ลดน้ำหนัก" else "เพิ่ม"),
        [0.25, 0.5, 0.75, 1.0],
        format_func=lambda x: f"{x} กก./สัปดาห์"
    )

if st.button("คำนวณ BMR & TDEE"):
    bmr = calculate_bmr(gender, weight, height, age)
    tdee = bmr * activity_levels[activity]

    st.success(f"BMR ของคุณคือ: {bmr:.2f} แคลอรี่/วัน")
    st.info(f"TDEE ของคุณคือ: {tdee:.2f} แคลอรี่/วัน")

    st.markdown("### 🎯 คำแนะนำ:")
    if goal_type == "รักษาน้ำหนัก":
        st.write(f"- หากต้องการรักษาน้ำหนัก: ควรบริโภค **{tdee:.0f} แคลอรี่/วัน**")
    else:
        # 1 กก. = 7700 kcal
        kcal_change = kg_per_week * 7700 / 7  # ต่อวัน
        if goal_type == "ลดน้ำหนัก":
            target_cal = tdee - kcal_change
            st.write(f"- หากต้องการลดน้ำหนัก {kg_per_week} กก./สัปดาห์: ควรบริโภค **{target_cal:.0f} แคลอรี่/วัน** (ลดลง {kcal_change:.0f} kcal/วัน)")
        else:
            target_cal = tdee + kcal_change
            st.write(f"- หากต้องการเพิ่มน้ำหนัก {kg_per_week} กก./สัปดาห์: ควรบริโภค **{target_cal:.0f} แคลอรี่/วัน** (เพิ่มขึ้น {kcal_change:.0f} kcal/วัน)")

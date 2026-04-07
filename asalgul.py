import streamlit as st
import urllib.parse

# --- НЕГИЗГИ МААЛЫМАТТАР ---
MY_PHONE = "996221109756"
MY_MBANK = "221468504"
ADMIN_PASSWORD = "777"
CAFE_NAME = "🌸 АСАЛГҮЛ 🌸"

st.set_page_config(page_title=CAFE_NAME, page_icon="🌸")

# Меню (Сүрөттөрдүн жаңы шилтемелери менен)
if 'menu_items' not in st.session_state:
    st.session_state.menu_items = {
        "🍲 Плов": {"баасы": 220, "сүрөт": "https://img.freepik.com/free-photo/uzbek-pilaf-with-lamb_127032-2114.jpg?w=740"},
        "🍜 Лагман": {"баасы": 190, "сүрөт": "https://img.freepik.com/free-photo/asian-soup-with-noodles-meat-vegetables_127032-1555.jpg?w=740"},
        "🥟 Манты": {"баасы": 200, "сүрөт": "https://img.freepik.com/free-photo/traditional-central-asian-food-manti_127032-2633.jpg?w=740"},
        "🥗 Шакарөп": {"баасы": 50, "сүрөт": "https://img.freepik.com/free-photo/salad-with-tomatoes-onions_127032-1845.jpg?w=740"},
        "☕ Чай": {"баасы": 30, "сүрөт": "https://img.freepik.com/free-photo/cup-tea-with-mint-lemon_127032-2050.jpg?w=740"}
    }

# --- САЙТТЫН КӨРҮНҮШҮ ---
st.markdown(f"<h1 style='text-align: center; color: #D81B60;'>{CAFE_NAME}</h1>", unsafe_allow_html=True)
st.write("---")

# Админ бөлүмү
with st.sidebar:
    st.header("⚙️ Башкаруу")
    pass_input = st.text_input("Пароль:", type="password")
    if pass_input == ADMIN_PASSWORD:
        st.success("Админ кирди")

# Менюну чыгаруу
selected_orders = {}
total_sum = 0

for dish, info in st.session_state.menu_items.items():
    col1, col2 = st.columns([1.5, 2])
    
    with col1:
        # Сүрөттү жүктөөдө ката кетсе, текст чыгат
        st.image(info["сүрөт"], use_container_width=True, caption=dish)
        
    with col2:
        st.subheader(dish)
        st.write(f"**Баасы:** {info['баасы']} сом")
        count = st.number_input("Саны:", min_value=0, key=f"cnt_{dish}")
        if count > 0:
            selected_orders[dish] = count
            total_sum += info["баасы"] * count
    st.write("---")

# Төлөм жана Жөнөтүү
if total_sum > 0:
    st.write(f"### 💰 Жалпы сумма: **{total_sum} сом**")
    st.info(f"💳 М-Банк номерибиз: **{MY_MBANK}**")
    
    location = st.text_input("📍 Дарегиңизди же столдун номерин жазыңыз:")
    
    if st.button("🚀 ЗАКАЗДЫ WHATSAPP-КА ЖӨНӨТҮҮ"):
        if location:
            items_text = "".join([f"• {d}: {c} даана\n" for d, c in selected_orders.items()])
            final_msg = f"🌸 *ЗАКАЗ: {CAFE_NAME}*\n\n{items_text}\n💰 *Сумма:* {total_sum} сом\n📍 *Жайы:* {location}\n💳 Төлөм: М-Банк аркылуу"
            
            encoded_msg = urllib.parse.quote(final_msg)
            url = f"https://wa.me/{MY_PHONE}?text={encoded_msg}"
            
            st.markdown(f'''
                <a href="{url}" target="_blank" style="text-decoration:none;">
                    <div style="background-color:#25D366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">
                        ✅ ЖӨНӨТҮҮНҮ ЫРАСТОО
                    </div>
                </a>
            ''', unsafe_allow_html=True)
        else:
            st.error("Сураныч, дарегиңизди жазыңыз!")

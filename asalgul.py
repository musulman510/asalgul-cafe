import streamlit as st
import urllib.parse

# --- ЖӨНӨТҮҮЛӨР ---
MY_PHONE = "996221109756"
MY_MBANK = "221468504"
ADMIN_PASSWORD = "777"
CAFE_NAME = "🌸 АСАЛГҮЛ 🌸"

st.set_page_config(page_title=CAFE_NAME, page_icon="🌸")

# Сүрөттөр менен негизги меню
if 'menu_items' not in st.session_state:
    st.session_state.menu_items = {
        "🍲 Плов": {"баасы": 220, "сүрөт": "https://i.ibb.co/L6VvX7T/plov.jpg"},
        "🍜 Лагман": {"баасы": 190, "сүрөт": "https://i.ibb.co/m0fGz5w/lagman.jpg"},
        "🥟 Манты": {"баасы": 200, "сүрөт": "https://i.ibb.co/xL7W8tG/manty.jpg"},
        "🥗 Шакарап": {"баасы": 50, "сүрөт": "https://i.ibb.co/rtLzVzF/shakarap.jpg"},
        "☕ Кара чай": {"баasы": 30, "сүрөт": "https://i.ibb.co/8Y5WfW4/tea.jpg"}
    }

# --- АДМИН ПАНЕЛЬ ---
with st.sidebar:
    st.header("⚙️ Башкаруу")
    pwd = st.text_input("Пароль:", type="password")
    if pwd == ADMIN_PASSWORD:
        st.success("Админ кирди")
        st.subheader("➕ Жаңы тамак кошуу")
        new_name = st.text_input("Тамактын аты:")
        new_price = st.number_input("Баасы (сом):", min_value=0)
        new_img = st.text_input("Сүрөт шилтемеси (ImgBB сайтынан):")
        
        if st.button("Кошуу"):
            if new_name and new_img:
                st.session_state.menu_items[new_name] = {"баасы": new_price, "сүрөт": new_img}
                st.rerun()

# --- НЕГИЗГИ БЕТ ---
st.markdown(f"<h1 style='text-align: center; color: #D81B60;'>{CAFE_NAME}</h1>", unsafe_allow_html=True)
st.write("---")

selected_orders = {}
total_sum = 0

# Менюну чыгаруу
for dish, info in st.session_state.menu_items.items():
    col1, col2 = st.columns([1.5, 2])
    with col1:
        st.image(info["сүрөт"], use_container_width=True)
    with col2:
        st.subheader(dish)
        st.write(f"**Баасы:** {info['баасы']} сом")
        count = st.number_input("Саны:", min_value=0, key=f"key_{dish}")
        if count > 0:
            selected_orders[dish] = count
            total_sum += info["баасы"] * count
    st.write("---")

# Заказды жөнөтүү
if total_sum > 0:
    st.write(f"### 💰 Жалпы сумма: {total_sum} сом")
    st.info(f"💳 М-Банк: {MY_MBANK}")
    location = st.text_input("📍 Стол же дарегиңиз:")
    
    if st.button("🚀 ЗАКАЗДЫ ЖӨНӨТҮҮ"):
        if location:
            items_text = "".join([f"• {d}: {c} даана\n" for d, c in selected_orders.items()])
            final_msg = f"🌸 *ЗАКАЗ: {CAFE_NAME}*\n\n{items_text}\n💰 *Сумма:* {total_sum} сом\n📍 *Жайы:* {location}"
            url = f"https://wa.me/{MY_PHONE}?text={urllib.parse.quote(final_msg)}"
            st.markdown

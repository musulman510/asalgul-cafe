import streamlit as st
import urllib.parse

# --- ЖӨНӨТҮҮЛӨР ---
MY_PHONE = "996221109756"
MY_MBANK = "221468504"
ADMIN_PASSWORD = "777"
CAFE_NAME = "🌸 АСАЛГҮЛ 🌸"

# Дизайн
st.set_page_config(page_title=CAFE_NAME, page_icon="🌸")

# Меню маалыматтары (Сүрөттөрдүн шилтемеси менен)
if 'menu_items' not in st.session_state:
    st.session_state.menu_items = {
        "🍲 Плов": {"баасы": 220, "сүрөт": "https://images.unsplash.com/photo-1626305716186-09859f515024?w=500"},
        "🍜 Лагман": {"баасы": 190, "сүрөт": "https://images.unsplash.com/photo-1512058560366-cd242955a732?w=500"},
        "🥟 Манты": {"баасы": 200, "сүрөт": "https://images.unsplash.com/photo-1534422298391-e4f8c170db76?w=500"},
        "🥗 Шакарөп": {"баасы": 50, "сүрөт": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500"},
        "☕ Чай": {"баасы": 30, "сүрөт": "https://images.unsplash.com/photo-1544787210-2213d84ad960?w=500"}
    }
if 'is_open' not in st.session_state:
    st.session_state.is_open = True

# --- НЕГИЗГИ БЕТ ---
st.markdown(f"<h1 style='text-align: center;'>{CAFE_NAME}</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Админ")
    pwd = st.text_input("Пароль:", type="password")
    if pwd == ADMIN_PASSWORD:
        st.session_state.is_open = st.toggle("Кафе иштеп жатат", value=st.session_state.is_open)

if not st.session_state.is_open:
    st.error("🛑 КЕЧИРИҢИЗ, КАФЕ ЖАБЫК")
else:
    st.success("✅ Биз ачыкпыз! Заказ бериңиз:")

    selected_orders = {}
    total = 0

    for dish, info in st.session_state.menu_items.items():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(info["сүрөт"], use_container_width=True)
        with col2:
            st.write(f"### {dish}")
            st.write(f"Баасы: {info['баасы']} сом")
            qty = st.number_input("Саны:", min_value=0, key=f"qty_{dish}")
            if qty > 0:
                selected_orders[dish] = qty
                total += info["баасы"] * qty
        st.divider()

    if total > 0:
        st.info(f"💰 Жалпы: {total} сом | 💳 М-Банк: {MY_MBANK}")
        loc = st.text_input("📍 Стол же Дарек:")
        
        if st.button("🚀 WHATSAPP-КА ЖӨНӨТҮҮ"):
            if loc:
                order_list = "".join([f"- {d}: {q}\n" for d, q in selected_orders.items()])
                msg = f"🌸 ЗАКАЗ: {CAFE_NAME}\n{order_list}Сумма: {total}\nЖайы: {loc}"
                url = f"https://wa.me/{MY_PHONE}?text={urllib.parse.quote(msg)}"
                st.markdown(f'[✅ ЖӨНӨТҮҮНҮ ЫРАСТОО]({url})')
            else:
                st.warning("Даректи жазыңыз!")


        
     
                

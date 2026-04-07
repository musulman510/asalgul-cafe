import streamlit as st
from datetime import datetime

# --- ЖӨНӨТҮҮЛӨР ---
ADMIN_PASSWORD = "777"
CAFE_NAME = "🌸 АСАЛГҮЛ 🌸"

st.set_page_config(page_title=CAFE_NAME, page_icon="🌸")

# Базаны түзүү
if 'orders_db' not in st.session_state:
    st.session_state.orders_db = []

# Меню (Сен жөнөткөн сүрөттөр менен)
menu = {
    "🍲 Плов": {"баасы": 220, "сүрөт": "https://i.ibb.co/L6VvX7T/plov.jpg"},
    "🍜 Лагман": {"баасы": 190, "сүрөт": "https://i.ibb.co/m0fGz5w/lagman.jpg"},
    "🥟 Манты": {"баасы": 200, "сүрөт": "https://i.ibb.co/xL7W8tG/manty.jpg"},
    "🥗 Шакарап": {"баасы": 50, "сүрөт": "https://i.ibb.co/rtLzVzF/shakarap.jpg"},
    "☕ Кара чай": {"баасы": 30, "сүрөт": "https://i.ibb.co/8Y5WfW4/tea.jpg"}
}

with st.sidebar:
    st.header("⚙️ Кирүү")
    mode = st.radio("Тандаңыз:", ["🙋 Кардар", "👨‍🍳 Сатуучу"])

# --- САТУУЧУНУН (АШПОЗЧУНУН) ПАНЕЛИ ---
if mode == "👨‍🍳 Сатуучу":
    pwd = st.text_input("Пароль:", type="password")
    if pwd == ADMIN_PASSWORD:
        st.title("📥 Түшкөн заказдар")
        
        active_orders = [o for o in st.session_state.orders_db if o['статус'] != "Аткарылды"]
        
        if not active_orders:
            st.info("Азырынча жаңы заказ жок.")
        else:
            for i, order in enumerate(st.session_state.orders_db):
                if order['статус'] != "Аткарылды":
                    with st.expander(f"📦 Заказ: {order['жайы']} ({order['убакыт']})"):
                        st.write(f"**Тел:** {order['номер']}")
                        st.write(f"**Заказ:** {order['тамактар']}")
                        st.write(f"**Сумма:** {order['сумма']} сом")
                        
                        # БАСКЫЧТАР ЛОГИКАСЫ
                        if order['түрү'] == "Кафедемин":
                            if st.button(f"Тамак даяр (Алып кетиңиз) ✅", key=f"ready_{i}"):
                                order['статус'] = "ТАМАК ДАЯР! Келип алып кетсеңиз болот 🍽️"
                                st.rerun()
                        else:
                            if st.button(f"Тамак жөнөтүлдү (Жолдо) 🚗", key=f"ship_{i}"):
                                order['статус'] = "ТАМАК ЖӨНӨТҮЛДҮ! Жолдо баратат, күтүңүз 🛵"
                                st.rerun()
                        
                        if st.button("Архивке сактоо (Өчүрүү) 🗑️", key=f"done_{i}"):
                            order['статус'] = "Аткарылды"
                            st.rerun()

# --- КАРДАРДЫН БЕТИ ---
else:
    st.title(CAFE_NAME)
    tab1, tab2 = st.tabs(["🛒 Тамак тандоо", "🔔 Заказдын абалы"])
    
    with tab1:
        selected = {}
        total = 0
        for dish, info in menu.items():
            col1, col2 = st.columns([1, 2])
            with col1: st.image(info["сүрөт"])
            with col2:
                st.subheader(dish)
                st.write(f"{info['баасы']} сом")
                qty = st.number_input("Саны", min_value=0, key=f"u_{dish}")
                if qty > 0:
                    selected[dish] = qty
                    total += info['баасы'] * qty
            st.divider()
        
        if total > 0:
            st.subheader(f"Жалпы: {total} сом")
            order_type = st.selectbox("Каякка?", ["Кафедемин", "Жеткирүү (Үйгө)"])
            phone = st.text_input("📞 Номериңиз (заказды текшерүү үчүн):")
            loc = st.text_input("📍 Стол № же Дарегиңиз:")
            
            if st.button("🚀 ЗАКАЗ БЕРҮҮ"):
                if phone and loc:
                    new_order = {
                        "номер": phone, "тамактар": str(selected),
                        "сумма": total, "жайы": loc, "түрү": order_type,
                        "статус": "Даярдалып жатат... 🔥",
                        "убакыт": datetime.now().strftime("%H:%M")
                    }
                    st.session_state.orders_db.append(new_order)
                    st.success("Заказыңыз кабыл алынды!")
                else:
                    st.error("Номер жана даректи толтуруңуз!")

    with tab2:
        check_phone = st.text_input("Заказыңызды текшерүү үчүн номериңизди жазыңыз:")
        if check_phone:
            found = False
            for order in reversed(st.session_state.orders_db):
                if order['номер'] == check_phone and order['статус'] != "Аткарылды":
                    st.warning(f"📊 Статус: {order['статус']}")
                    st.info(f"📝 Заказыңыз: {order['тамактар']}")
                    found = True
            if not found:
                st.write("Бул номерде активдүү заказ табылган жок.")

import streamlit as st
import urllib.parse

# --- НЕГИЗГИ ЖӨНӨТҮҮЛӨР ---
MY_PHONE = "996221109756"  # Сенин WhatsApp номериң
MY_MBANK = "221468504"     # Сенин М-Банк номериң
ADMIN_PASSWORD = "777"     
CAFE_NAME = "🌸 АСАЛГҮЛ 🌸"

# --- МААЛЫМАТТАРДЫ САКТОО ---
if 'is_open' not in st.session_state:
    st.session_state.is_open = True
if 'menu_items' not in st.session_state:
    st.session_state.menu_items = {
        "🍲 Плов": 220,
        "🍜 Лагман": 190,
        "🥟 Манты": 200,
        "🥗 Шакарөп": 50,
        "☕ Чай": 30
    }

# --- САЙТТЫН ТҮЗҮЛҮШҮ ---
st.set_page_config(page_title=CAFE_NAME, page_icon="🌸")

# --- САТУУЧУ ҮЧҮН ПАНЕЛЬ ---
with st.sidebar:
    st.header("⚙️ Башкаруу")
    pwd = st.text_input("Пароль:", type="password")
    if pwd == ADMIN_PASSWORD:
        st.success("Админ кирди")
        st.session_state.is_open = st.toggle("Кафе ачык", value=st.session_state.is_open)
        
        st.subheader("➕ Тамак кошуу")
        n = st.text_input("Аты:")
        p = st.number_input("Баасы:", min_value=0)
        if st.button("Кошуу"):
            st.session_state.menu_items[n] = p
            st.rerun()
    else:
        st.info("Бул бөлүм сатуучу үчүн.")

# --- КАРДАРЛАР ҮЧҮН БЕТ ---
st.title(f"{CAFE_NAME} Кафеси")

if not st.session_state.is_open:
    st.error("🛑 КЕЧИРИҢИЗ, КАФЕ БҮГҮН ИШТЕБЕЙТ!")
else:
    st.success("✅ Биз ачыкпыз! Төмөндөн тамак тандаңыз:")
    
    selected_orders = {}
    total_price = 0
    
    # Меню
    for dish, price in st.session_state.menu_items.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{dish}** — {price} сом")
        with col2:
            qty = st.number_input("Саны:", min_value=0, key=f"qty_{dish}")
            if qty > 0:
                selected_orders[dish] = qty
                total_price += price * qty

    st.divider()
    
    # Заказ маалыматы
    order_type = st.radio("Кайда отурасыз?", ("Кафеде (Столдо)", "Үйгө жеткирүү"))
    location = st.text_input("Столдун номери же Дарегиңиз:")

    if total_price > 0:
        st.write(f"### Жалпы сумма: **{total_price} сом**")
        
        # М-Банк маалыматын көрсөтүү
        st.info(f"💳 **Төлөм үчүн М-Банк номери:** `{MY_MBANK}`")
        
        # WhatsApp текст
        order_details = "".join([f"- {item}: {q} даана\n" for item, q in selected_orders.items()])
        final_message = (
            f"🌸 *ЖАҢЫ ЗАКАЗ - {CAFE_NAME}*\n"
            f"---------------------------\n"
            f"{order_details}"
            f"---------------------------\n"
            f"💰 *Сумма:* {total_price} сом\n"
            f"📍 *Жайы:* {order_type}\n"
            f"🏠 *Дарек/Стол:* {location}\n"
            f"💳 *Төлөм:* М-Банк ({MY_MBANK})"
        )
        
        encoded_msg = urllib.parse.quote(final_message)
        wa_url = f"https://wa.me/{MY_PHONE}?text={encoded_msg}"
        
        if st.button("🚀 ЗАКАЗДЫ ЖӨНӨТҮҮ"):
            if not location:
                st.warning("Сураныч, столду же даректи жазыңыз!")
            else:
                st.markdown(f'''
                    <a href="{wa_url}" target="_blank" style="text-decoration:none;">
                        <div style="background-color:#25D366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">
                            📲 WHATSAPP-ТАН ЫРАСТОО
                        </div>
                    </a>
                ''', unsafe_allow_html=True)
                

import streamlit as st
import plotly.graph_objects as go
from supabase import create_client
from stock_utils import get_stock_data, calculate_change
from ai_engine import generate_ai_report
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(layout="wide")

st.title("🚀 AI Stock Dashboard")

col1, col2 = st.columns(2)

with col1:
    stock = st.text_input("Stock Symbol", "AAPL")

with col2:
    email = st.text_input("Email")

if st.button("Analyze"):

    data = get_stock_data(stock)

    if data is None:
        st.error("Invalid stock")
        st.stop()

    # 🔥 PRO GRAPH (PLOTLY)
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["Close"],
        mode='lines',
        line=dict(width=3)
    ))

    fig.update_layout(
        template="plotly_dark",
        title=f"{stock} Price Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

    # AI
    change = calculate_change(data)
    ai = generate_ai_report(stock, change)

    st.subheader("🧠 AI Analysis")
    st.markdown(ai)

    # SAVE USER
    if email:
        supabase.table("users").upsert({
            "email": email,
            "stocks": stock
        }).execute()

        st.success("Saved & will receive daily report 🚀")



       

       

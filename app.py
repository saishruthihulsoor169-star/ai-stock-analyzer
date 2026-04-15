import streamlit as st
import plotly.graph_objects as go
from supabase import create_client
from stock_utils import get_stock_data, analyze_stock, get_news
from ai_engine import generate_ai_report
from mailer import send_email
import os

# ---------- SUPABASE ----------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------- UI ----------
st.set_page_config(layout="wide")
st.title("🚀 AI Stock Dashboard")

col1, col2 = st.columns(2)

with col1:
    stock = st.text_input("Stock Symbol", "AAPL")

with col2:
    email = st.text_input("Email")

# ---------- BUTTON ----------
if st.button("Analyze"):

    # ---------- FETCH DATA ----------
    data = get_stock_data(stock)

    if data is None:
        st.error(f"❌ Could not fetch data for '{stock}'")
        st.stop()

    st.success("✅ Data fetched successfully")

    # ---------- GRAPH ----------
    smooth = data["Close"].rolling(5).mean()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data["Date"],
        y=data["Close"],
        mode='lines',
        name="Raw",
        opacity=0.3
    ))

    fig.add_trace(go.Scatter(
        x=data["Date"],
        y=smooth,
        mode='lines',
        name="Trend",
        line=dict(width=3)
    ))

    fig.update_layout(
        template="plotly_dark",
        title=f"{stock} Price Trend",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------- ANALYSIS ----------
    result = analyze_stock(data)
    change = result["change"]

    ai = generate_ai_report(stock, change)

    st.subheader("🤖 AI Analysis")
    st.markdown(ai)

    # ---------- NEWS ----------
    news = get_news(stock)

    st.subheader("📰 News")
    for n in news:
        st.write("•", n)

    # ---------- SAVE + EMAIL ----------
    if email:
        try:
            # Save to DB
            supabase.table("users").upsert({
                "email": email,
                "stocks": stock
            }).execute()

            # Email content
            email_content = f"""
            <h2>📊 AI Stock Report</h2>
            <p><b>Stock:</b> {stock}</p>
            <p><b>Change:</b> {change}%</p>

            <h3>🤖 AI Analysis</h3>
            <p>{ai}</p>

            <h3>📰 News</h3>
            <ul>
            {''.join([f'<li>{n}</li>' for n in news])}
            </ul>
            """

            # Send Email
            send_email(
                to_email=email,
                subject=f"{stock} Stock Report",
                html=email_content
            )

            st.success("✅ Email sent successfully 🚀")

        except Exception as e:
            st.error(f"❌ Error: {e}")


       

       

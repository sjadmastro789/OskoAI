import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.campaign_tools import get_campaign_summary, compare_campaigns, get_optimization_tips
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="OskoAI - Marketing Agent", page_icon="🤖", layout="wide")

st.markdown("""
<style>
    .title-style {
        font-size: 42px; font-weight: bold;
        background: linear-gradient(90deg, #00C851, #007bff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

col_logo, col_title = st.columns([1, 8])
with col_logo:
    st.markdown("# 🤖")
with col_title:
    st.markdown('<p class="title-style">OskoAI — Marketing Optimization Agent</p>', unsafe_allow_html=True)
    st.caption("نظام ذكاء اصطناعي متكامل لتحليل وتحسين الحملات التسويقية • Powered by Groq LLaMA 3.3")

st.divider()
df = pd.read_csv("data/campaigns.csv")

# ── القسم 1: KPIs ──
st.subheader("📊 لوحة المؤشرات الرئيسية")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("💰 إجمالي الإنفاق", f"${df['spend'].sum():,.0f}")
with col2:
    st.metric("📈 إجمالي الإيراد", f"${df['revenue'].sum():,.0f}")
with col3:
    profit = df['revenue'].sum() - df['spend'].sum()
    st.metric("💵 صافي الربح", f"${profit:,.0f}", f"+{profit/df['spend'].sum()*100:.0f}%")
with col4:
    st.metric("🏆 أفضل ROAS", df.groupby("campaign_name")["ROAS"].mean().idxmax())
with col5:
    st.metric("🎯 متوسط CTR", f"{df['CTR'].mean():.2f}%")

st.divider()

# ── القسم 2: Charts ──
st.subheader("📉 تحليل الأداء")
tab1, tab2, tab3 = st.tabs(["📈 ROAS عبر الزمن", "💸 الإنفاق vs الإيراد", "🎯 مقارنة KPIs"])

with tab1:
    fig1 = px.line(df, x="date", y="ROAS", color="campaign_name",
        title="ROAS عبر الزمن", template="plotly_dark")
    fig1.update_layout(height=400)
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    fig2 = px.bar(df.groupby("campaign_name")[["spend","revenue"]].sum().reset_index(),
        x="campaign_name", y=["spend","revenue"], barmode="group",
        title="الإنفاق مقابل الإيراد", template="plotly_dark",
        color_discrete_sequence=["#FF4444", "#00C851"])
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    comparison = df.groupby("campaign_name")[["CTR","ROAS","CPA"]].mean().round(2)
    fig3 = px.bar(comparison.reset_index(), x="campaign_name", y=["CTR","ROAS","CPA"],
        barmode="group", title="مقارنة KPIs", template="plotly_dark")
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ── القسم 3: جدول البيانات ──
st.subheader("📋 تفاصيل الحملات")
campaign_filter = st.selectbox("اختر الحملة:", ["الكل"] + list(df["campaign_name"].unique()))
if campaign_filter == "الكل":
    st.dataframe(df, use_container_width=True, height=300)
else:
    st.dataframe(df[df["campaign_name"] == campaign_filter], use_container_width=True, height=300)

st.divider()

# ── القسم 4: OskoAI Agent ──
st.subheader("🤖 اسأل OskoAI Agent")
col_q, col_btn = st.columns([5, 1])
with col_q:
    question = st.text_input("سؤالك:", placeholder="مثال: أي حملة أفضل وليش؟", label_visibility="collapsed")
with col_btn:
    ask_btn = st.button("🚀 اسأل", type="primary", use_container_width=True)

if ask_btn:
    if question:
        with st.spinner("🧠 OskoAI يفكر..."):
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            data_context = compare_campaigns() + "\n" + get_optimization_tips()
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"أنت OskoAI خبير تسويق.\nبيانات:\n{data_context}\nأجب بالعربي."},
                    {"role": "user", "content": question}
                ]
            )
            st.success("✅ جواب OskoAI:")
            st.write(response.choices[0].message.content)
    else:
        st.warning("⚠️ اكتب سؤالك أولاً!")

st.divider()

# ── القسم 5: توصيات تلقائية ──
st.subheader("💡 توصيات OskoAI التلقائية")
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1:
    if st.button("📊 تحليل Google Ads", use_container_width=True):
        st.info(get_campaign_summary("Google_Ads"))
with col_t2:
    if st.button("📱 تحليل Meta Ads", use_container_width=True):
        st.info(get_campaign_summary("Meta_Ads"))
with col_t3:
    if st.button("📧 تحليل Email Campaign", use_container_width=True):
        st.info(get_campaign_summary("Email_Campaign"))
if st.button("🔍 اعرض كل التوصيات", type="primary", use_container_width=True):
    with st.spinner("يحلل..."):
        st.success(get_optimization_tips())

st.divider()

# ── القسم 6: Analytics Agent ──
st.subheader("🔬 Analytics Agent — تحليل متعمق")
col_a1, col_a2 = st.columns(2)
with col_a1:
    if st.button("📈 تحليل الاتجاهات", use_container_width=True):
        with st.spinner("يحلل..."):
            from agents.analytics_agent import analyze_trends
            st.info(analyze_trends())
    if st.button("⚠️ كشف الشذوذات", use_container_width=True):
        with st.spinner("يكشف..."):
            from agents.analytics_agent import detect_anomalies
            st.warning(detect_anomalies())
with col_a2:
    if st.button("📅 أفضل وأسوأ الأيام", use_container_width=True):
        with st.spinner("يحلل..."):
            from agents.analytics_agent import get_best_days
            st.info(get_best_days())
    if st.button("💰 توصية الميزانية", use_container_width=True):
        with st.spinner("يحسب..."):
            from agents.analytics_agent import budget_recommendation
            st.success(budget_recommendation())

st.divider()

# ── القسم 7: Content Agent ──
st.subheader("✍️ Content Agent — توليد إعلانات")
campaign_for_content = st.selectbox("اختر الحملة:", ["Google_Ads", "Meta_Ads", "Email_Campaign"], key="content_selectbox")
if st.button("✍️ ولّد نسخ إعلانية", type="primary", use_container_width=True):
    with st.spinner("Content Agent يكتب الإعلانات..."):
        from agents.content_agent import generate_ad_copy
        st.success(generate_ad_copy(campaign_for_content))

st.divider()

# ── القسم 8: Budget Agent ──
st.subheader("💰 Budget Agent — إدارة الميزانية")
total_budget = st.number_input(
    "أدخل ميزانيتك الإجمالية ($):",
    min_value=1000, max_value=1000000, value=10000, step=1000
)
col_b1, col_b2, col_b3 = st.columns(3)
with col_b1:
    if st.button("💰 وزّع الميزانية", use_container_width=True):
        with st.spinner("يحسب..."):
            from agents.budget_agent import allocate_budget
            st.success(allocate_budget(total_budget))
with col_b2:
    if st.button("📅 توقعات 3 أشهر", use_container_width=True):
        with st.spinner("يتنبأ..."):
            from agents.budget_agent import roi_forecast
            st.info(roi_forecast(3))
with col_b3:
    if st.button("🔍 حملات تحتاج تحسين", use_container_width=True):
        with st.spinner("يحلل..."):
            from agents.budget_agent import optimize_underperforming
            st.warning(optimize_underperforming())

st.divider()
st.caption("🤖 OskoAI v1.0 — Marketing Optimization Agent | Powered by Groq LLaMA 3.3 | Built with Streamlit")
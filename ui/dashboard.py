import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.campaign_tools import get_campaign_summary, compare_campaigns, get_optimization_tips
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# إعداد الصفحة
st.set_page_config(
    page_title="OskoAI - Marketing Agent",
    page_icon="🤖",
    layout="wide"
)

# Header
st.title("🤖 OskoAI — Marketing Optimization Agent")
st.markdown("**نظام ذكاء اصطناعي لتحليل وتحسين الحملات التسويقية**")
st.divider()

# تحميل البيانات
df = pd.read_csv("data/campaigns.csv")

# القسم الأول — إحصائيات سريعة
st.subheader("📊 نظرة عامة على الحملات")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("إجمالي الإنفاق", f"${df['spend'].sum():,.0f}")
with col2:
    st.metric("إجمالي الإيراد", f"${df['revenue'].sum():,.0f}")
with col3:
    st.metric("صافي الربح", f"${df['revenue'].sum() - df['spend'].sum():,.0f}")
with col4:
    best = df.groupby("campaign_name")["ROAS"].mean().idxmax()
    st.metric("أفضل حملة", best)

st.divider()

# القسم الثاني — مقارنة الحملات
st.subheader("📈 مقارنة أداء الحملات")

comparison = df.groupby("campaign_name")[["CTR","ROAS","CPA","spend","revenue"]].mean().round(2)
st.dataframe(comparison, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.bar_chart(comparison["ROAS"], color="#00C851")

with col2:
    st.bar_chart(comparison["CTR"], color="#FF4444")

st.divider()

# القسم الثالث — OskoAI Agent
st.subheader("🤖 اسأل OskoAI Agent")

question = st.text_input(
    "اكتب سؤالك عن الحملات:",
    placeholder="مثال: أي حملة أفضل وليش؟"
)

if st.button("🚀 اسأل الـ Agent", type="primary"):
    if question:
        with st.spinner("OskoAI يفكر..."):

            client = Groq(api_key=os.getenv("GROQ_API_KEY"))

            # جمع كل البيانات
            data_context = compare_campaigns() + "\n" + get_optimization_tips()

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"""أنت OskoAI خبير تسويق ذكي.
بيانات الحملات:
{data_context}
أجب بشكل واضح ومختصر بالعربي."""},
                    {"role": "user", "content": question}
                ]
            )

            answer = response.choices[0].message.content
            st.success("✅ جواب OskoAI:")
            st.write(answer)
    else:
        st.warning("اكتب سؤالك أولاً!")

st.divider()

# القسم الرابع — توصيات تلقائية
st.subheader("💡 توصيات OskoAI التلقائية")

if st.button("🔍 اعرض التوصيات"):
    with st.spinner("يحلل البيانات..."):
        tips = get_optimization_tips()
        st.info(tips)
        st.divider()

# القسم الخامس — Charts احترافية
st.subheader("📉 تحليل الأداء عبر الزمن")

import plotly.express as px

# Chart 1 — ROAS عبر الزمن
fig1 = px.line(
    df, x="date", y="ROAS",
    color="campaign_name",
    title="ROAS عبر الزمن لكل حملة",
    labels={"date": "التاريخ", "ROAS": "عائد الإنفاق", "campaign_name": "الحملة"}
)
st.plotly_chart(fig1, use_container_width=True)

# Chart 2 — الإنفاق vs الإيراد
fig2 = px.bar(
    df.groupby("campaign_name")[["spend","revenue"]].sum().reset_index(),
    x="campaign_name", y=["spend","revenue"],
    title="الإنفاق مقابل الإيراد لكل حملة",
    barmode="group",
    labels={"campaign_name": "الحملة", "value": "المبلغ ($)"}
)
st.plotly_chart(fig2, use_container_width=True)
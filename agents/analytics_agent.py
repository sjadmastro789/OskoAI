import pandas as pd
import sys
import os
from groq import Groq
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ═══════════════════════════════════
# أدوات التحليل المتخصصة
# ═══════════════════════════════════

def detect_anomalies() -> str:
    """يكتشف الأيام غير الطبيعية في أداء الحملات"""
    df = pd.read_csv("data/campaigns.csv")
    results = []

    for campaign in df["campaign_name"].unique():
        camp_df = df[df["campaign_name"] == campaign]
        mean_roas = camp_df["ROAS"].mean()
        std_roas = camp_df["ROAS"].std()

        anomalies = camp_df[
            (camp_df["ROAS"] > mean_roas + 2 * std_roas) |
            (camp_df["ROAS"] < mean_roas - 2 * std_roas)
        ]

        if not anomalies.empty:
            for _, row in anomalies.iterrows():
                results.append(
                    f"⚠️ {campaign} — يوم {row['date']}: ROAS = {row['ROAS']} "
                    f"(المتوسط: {mean_roas:.2f})"
                )

    return "\n".join(results) if results else "✅ لا توجد أيام غير طبيعية"


def analyze_trends() -> str:
    """يحلل الاتجاهات خلال الشهر"""
    df = pd.read_csv("data/campaigns.csv")
    df["date"] = pd.to_datetime(df["date"])

    results = []
    for campaign in df["campaign_name"].unique():
        camp_df = df[df["campaign_name"] == campaign].sort_values("date")

        first_half = camp_df.iloc[:15]["ROAS"].mean()
        second_half = camp_df.iloc[15:]["ROAS"].mean()
        change = ((second_half - first_half) / first_half) * 100

        trend = "📈 تحسن" if change > 0 else "📉 تراجع"
        results.append(
            f"{trend} {campaign}: {change:+.1f}% "
            f"(أول الشهر: {first_half:.2f} → آخر الشهر: {second_half:.2f})"
        )

    return "\n".join(results)


def get_best_days() -> str:
    """يجيب أفضل وأسوأ أيام لكل حملة"""
    df = pd.read_csv("data/campaigns.csv")
    results = []

    for campaign in df["campaign_name"].unique():
        camp_df = df[df["campaign_name"] == campaign]
        best = camp_df.loc[camp_df["ROAS"].idxmax()]
        worst = camp_df.loc[camp_df["ROAS"].idxmin()]

        results.append(f"""
📌 {campaign}:
   🟢 أفضل يوم: {best['date']} — ROAS: {best['ROAS']} | إيراد: ${best['revenue']:.0f}
   🔴 أسوأ يوم:  {worst['date']} — ROAS: {worst['ROAS']} | إيراد: ${worst['revenue']:.0f}""")

    return "\n".join(results)


def budget_recommendation() -> str:
    """يوصي بتوزيع الميزانية بناءً على الأداء"""
    df = pd.read_csv("data/campaigns.csv")
    perf = df.groupby("campaign_name")["ROAS"].mean()
    total = perf.sum()

    results = ["💰 توصية توزيع الميزانية:"]
    for campaign, roas in perf.items():
        percentage = (roas / total) * 100
        results.append(f"   {campaign}: {percentage:.1f}% من الميزانية (ROAS: {roas:.2f}x)")

    return "\n".join(results)


# ═══════════════════════════════════
# Analytics Agent
# ═══════════════════════════════════

ANALYTICS_TOOLS = {
    "detect_anomalies": detect_anomalies,
    "analyze_trends": analyze_trends,
    "get_best_days": get_best_days,
    "budget_recommendation": budget_recommendation,
}

ANALYTICS_PROMPT = """
أنت Analytics Agent متخصص في تحليل بيانات التسويق.
عندك 4 أدوات متخصصة:

1. detect_anomalies — يكتشف الأيام غير الطبيعية
2. analyze_trends — يحلل الاتجاهات
3. get_best_days — يجيب أفضل وأسوأ الأيام
4. budget_recommendation — يوصي بتوزيع الميزانية

للرد على أي سؤال اختر الأداة المناسبة واكتب:
TOOL: [اسم الأداة]
"""


def run_analytics_agent(question: str) -> str:
    print(f"\n🔬 Analytics Agent — السؤال: {question}")
    print("=" * 50)

    messages = [
        {"role": "system", "content": ANALYTICS_PROMPT},
        {"role": "user", "content": question}
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0
    )

    agent_response = response.choices[0].message.content

    # تشغيل الأداة المناسبة
    tool_result = ""
    for tool_name, tool_func in ANALYTICS_TOOLS.items():
        if tool_name in agent_response:
            tool_result = tool_func()
            print(f"🔧 Tool: {tool_name}")
            print(f"📊 النتيجة:\n{tool_result}")
            break

    # الجواب النهائي
    if tool_result:
        messages.append({"role": "assistant", "content": agent_response})
        messages.append({
            "role": "user",
            "content": f"نتيجة التحليل:\n{tool_result}\n\nأعطني تحليلاً احترافياً مفصلاً بالعربي."
        })

        final = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0
        )
        answer = final.choices[0].message.content
    else:
        answer = agent_response

    print(f"\n✅ التحليل النهائي:\n{answer}")
    return answer


if __name__ == "__main__":
    print("\n🔬 اختبار Analytics Agent")
    print("=" * 50)
    run_analytics_agent("حلل الاتجاهات وقل لي أي حملة تتحسن وأيها تتراجع؟")
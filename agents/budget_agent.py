import pandas as pd
import sys
import os
from groq import Groq
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ═══════════════════════════════════
# أدوات الميزانية
# ═══════════════════════════════════

def allocate_budget(total_budget: float) -> str:
    """يوزع الميزانية بذكاء بناءً على أداء الحملات"""
    df = pd.read_csv("data/campaigns.csv")
    perf = df.groupby("campaign_name")["ROAS"].mean()
    total_roas = perf.sum()

    result = [f"💰 توزيع ميزانية ${total_budget:,.0f}:\n"]
    for campaign, roas in perf.items():
        allocation = (roas / total_roas) * total_budget
        percentage = (roas / total_roas) * 100
        expected_revenue = allocation * roas
        result.append(
            f"📌 {campaign}:\n"
            f"   • الميزانية المقترحة: ${allocation:,.0f} ({percentage:.1f}%)\n"
            f"   • ROAS المتوقع: {roas:.2f}x\n"
            f"   • الإيراد المتوقع: ${expected_revenue:,.0f}\n"
        )

    total_expected = sum(
        (perf[c] / total_roas) * total_budget * perf[c]
        for c in perf.index
    )
    result.append(f"✅ إجمالي الإيراد المتوقع: ${total_expected:,.0f}")
    return "\n".join(result)


def roi_forecast(months: int = 3) -> str:
    """يتنبأ بالـ ROI للأشهر القادمة"""
    df = pd.read_csv("data/campaigns.csv")

    avg_spend = df.groupby("campaign_name")["spend"].mean()
    avg_revenue = df.groupby("campaign_name")["revenue"].mean()
    avg_roas = df.groupby("campaign_name")["ROAS"].mean()

    result = [f"📅 توقعات {months} أشهر القادمة:\n"]
    for campaign in avg_spend.index:
        monthly_spend = avg_spend[campaign] * 30
        monthly_revenue = avg_revenue[campaign] * 30
        total_spend = monthly_spend * months
        total_revenue = monthly_revenue * months
        profit = total_revenue - total_spend

        result.append(
            f"📌 {campaign}:\n"
            f"   • إنفاق شهري: ${monthly_spend:,.0f}\n"
            f"   • إيراد شهري: ${monthly_revenue:,.0f}\n"
            f"   • ربح {months} أشهر: ${profit:,.0f}\n"
            f"   • ROAS: {avg_roas[campaign]:.2f}x\n"
        )

    return "\n".join(result)


def optimize_underperforming() -> str:
    """يحدد الحملات الضعيفة ويعطي توصيات"""
    df = pd.read_csv("data/campaigns.csv")
    avg_roas = df.groupby("campaign_name")["ROAS"].mean()
    overall_avg = avg_roas.mean()

    result = ["🔍 تحليل الحملات الضعيفة:\n"]
    for campaign, roas in avg_roas.items():
        if roas < overall_avg:
            gap = overall_avg - roas
            result.append(
                f"⚠️ {campaign} — أقل من المتوسط بـ {gap:.2f} نقطة\n"
                f"   • ROAS الحالي: {roas:.2f}x\n"
                f"   • المتوسط العام: {overall_avg:.2f}x\n"
                f"   • التوصية: راجع استهداف الجمهور وجودة المحتوى\n"
            )
        else:
            result.append(f"✅ {campaign} — أداء ممتاز ({roas:.2f}x)\n")

    return "\n".join(result)


# ═══════════════════════════════════
# Budget Agent
# ═══════════════════════════════════

def run_budget_agent(total_budget: float = 10000) -> str:
    """يشغّل Budget Agent الكامل"""
    print(f"\n💰 Budget Agent — ميزانية: ${total_budget:,.0f}")
    print("=" * 50)

    allocation = allocate_budget(total_budget)
    forecast = roi_forecast(3)
    optimization = optimize_underperforming()

    context = f"{allocation}\n\n{forecast}\n\n{optimization}"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": """أنت Budget Agent خبير في إدارة ميزانيات التسويق.
بناءً على البيانات، أعطِ توصيات مالية واضحة ومفصلة بالعربي."""},
            {"role": "user", "content": f"بناءً على هذه البيانات:\n{context}\n\nأعطني خطة ميزانية شاملة."}
        ]
    )

    answer = response.choices[0].message.content
    print(f"✅ توصية Budget Agent:\n{answer}")
    return answer


if __name__ == "__main__":
    print(allocate_budget(10000))
    print("\n" + "="*50 + "\n")
    print(roi_forecast(3))
    print("\n" + "="*50 + "\n")
    print(optimize_underperforming())
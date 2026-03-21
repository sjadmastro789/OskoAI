from groq import Groq
from dotenv import load_dotenv
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ═══════════════════════════════════
# أدوات الـ Content Agent
# ═══════════════════════════════════

def generate_ad_copy(campaign_name: str) -> str:
    """يولد نسخ إعلانية محسّنة لحملة معينة"""
    df = pd.read_csv("data/campaigns.csv")
    camp = df[df["campaign_name"] == campaign_name]

    if camp.empty:
        return f"ما وجدت حملة: {campaign_name}"

    avg_roas = camp["ROAS"].mean()
    avg_ctr = camp["CTR"].mean()
    avg_cpa = camp["CPA"].mean()

    prompt = f"""أنت خبير كتابة إعلانية محترف.
بيانات الحملة {campaign_name}:
- متوسط ROAS: {avg_roas:.2f}x
- متوسط CTR: {avg_ctr:.2f}%
- متوسط CPA: {avg_cpa:.2f}$

اكتب 3 نسخ إعلانية مختلفة لهذه الحملة:
1. نسخة عاطفية تركز على المشاعر
2. نسخة منطقية تركز على الأرقام والفوائد
3. نسخة عاجلة تخلق إحساس بالإلحاح

لكل نسخة اكتب:
- العنوان (Headline)
- النص الرئيسي (Body)
- الدعوة للعمل (CTA)
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def score_ad_copy(ad_text: str) -> str:
    """يقيّم جودة نص إعلاني"""
    prompt = f"""أنت خبير تسويق. قيّم هذا الإعلان من 1-10 في هذه المعايير:

الإعلان:
{ad_text}

قيّمه في:
1. الوضوح والبساطة (1-10)
2. قوة العنوان (1-10)
3. فعالية الـ CTA (1-10)
4. الجاذبية العاطفية (1-10)
5. المصداقية (1-10)

ثم أعطِ تقييماً إجمالياً وتوصيات للتحسين."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def suggest_improvements(campaign_name: str) -> str:
    """يقترح تحسينات للحملة بناءً على بياناتها"""
    df = pd.read_csv("data/campaigns.csv")
    camp = df[df["campaign_name"] == campaign_name]

    avg_roas = camp["ROAS"].mean()
    avg_ctr = camp["CTR"].mean()
    avg_cpa = camp["CPA"].mean()

    # تحديد المشاكل
    issues = []
    if avg_ctr < 3:
        issues.append(f"CTR منخفض ({avg_ctr:.2f}%) — العنوان مو جذاب كفاية")
    if avg_roas < 3:
        issues.append(f"ROAS منخفض ({avg_roas:.2f}x) — العائد أقل من المتوقع")
    if avg_cpa > 30:
        issues.append(f"CPA مرتفع ({avg_cpa:.2f}$) — تكلفة التحويل عالية")

    if not issues:
        issues.append("الحملة تؤدي بشكل جيد!")

    prompt = f"""أنت خبير تسويق رقمي.
حملة {campaign_name} عندها هذه المشاكل:
{chr(10).join(issues)}

أعطِ 5 توصيات عملية ومحددة لتحسين أداء الحملة.
كل توصية تكون قابلة للتطبيق فوراً."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# ═══════════════════════════════════
# Content Agent
# ═══════════════════════════════════

def run_content_agent(task: str, campaign_name: str = "Meta_Ads") -> str:
    print(f"\n✍️ Content Agent — المهمة: {task}")
    print("=" * 50)

    if "نسخ" in task or "إعلان" in task or "copy" in task.lower():
        result = generate_ad_copy(campaign_name)
    elif "تقييم" in task or "score" in task.lower():
        result = score_ad_copy(task)
    else:
        result = suggest_improvements(campaign_name)

    print(f"✅ النتيجة:\n{result}")
    return result


if __name__ == "__main__":
    print("\n✍️ اختبار Content Agent")
    print("=" * 50)
    run_content_agent("اكتب نسخ إعلانية", "Meta_Ads")
import sys
import os
from groq import Groq
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# استيراد كل الـ Agents
from agents.analytics_agent import analyze_trends, detect_anomalies, get_best_days
from agents.budget_agent import allocate_budget, roi_forecast, optimize_underperforming
from agents.content_agent import generate_ad_copy
from tools.campaign_tools import compare_campaigns, get_optimization_tips

# ═══════════════════════════════════
# كل الأدوات المتاحة
# ═══════════════════════════════════
ALL_TOOLS = {
    "compare_campaigns": {"func": compare_campaigns, "desc": "مقارنة أداء الحملات"},
    "analyze_trends": {"func": analyze_trends, "desc": "تحليل الاتجاهات"},
    "detect_anomalies": {"func": detect_anomalies, "desc": "كشف الشذوذات"},
    "get_best_days": {"func": get_best_days, "desc": "أفضل وأسوأ الأيام"},
    "allocate_budget": {"func": lambda: allocate_budget(10000), "desc": "توزيع الميزانية"},
    "roi_forecast": {"func": lambda: roi_forecast(3), "desc": "توقعات الـ ROI"},
    "optimize_underperforming": {"func": optimize_underperforming, "desc": "تحسين الحملات الضعيفة"},
    "get_optimization_tips": {"func": get_optimization_tips, "desc": "توصيات التحسين"},
}

ORCHESTRATOR_PROMPT = """
أنت Orchestrator Agent — الدماغ الرئيسي لنظام OskoAI.
مهمتك تحليل سؤال المستخدم وتحديد أفضل الأدوات للإجابة.

الأدوات المتاحة:
1. compare_campaigns — مقارنة أداء الحملات
2. analyze_trends — تحليل الاتجاهات
3. detect_anomalies — كشف الشذوذات
4. get_best_days — أفضل وأسوأ الأيام
5. allocate_budget — توزيع الميزانية
6. roi_forecast — توقعات الـ ROI
7. optimize_underperforming — تحسين الحملات الضعيفة
8. get_optimization_tips — توصيات التحسين

للإجابة اكتب بالضبط:
TOOLS: [اسم الأداة 1, اسم الأداة 2]
REASON: [سبب اختيارك]
"""


def run_orchestrator(question: str) -> dict:
    """يشغّل الـ Orchestrator ويعطي تقرير شامل"""
    print(f"\n🎯 Orchestrator — السؤال: {question}")
    print("=" * 60)

    # الخطوة 1: الـ Orchestrator يختار الأدوات
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": ORCHESTRATOR_PROMPT},
            {"role": "user", "content": question}
        ],
        temperature=0
    )

    decision = response.choices[0].message.content
    print(f"🧠 قرار الـ Orchestrator:\n{decision}")

    # الخطوة 2: تشغيل الأدوات المختارة
    tools_results = {}
    for tool_name, tool_info in ALL_TOOLS.items():
        if tool_name in decision:
            print(f"\n🔧 تشغيل: {tool_name}")
            result = tool_info["func"]()
            tools_results[tool_name] = result
            print(f"✅ خلص: {tool_name}")

    # الخطوة 3: تجميع كل النتائج
    combined_results = "\n\n".join([
        f"=== {name} ===\n{result}"
        for name, result in tools_results.items()
    ])

    # الخطوة 4: الـ Orchestrator يولّد التقرير النهائي
    final_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": """أنت OskoAI Orchestrator — خبير تسويق رقمي متكامل.
بناءً على نتائج التحليل، أعطِ تقريراً شاملاً ومنظماً بالعربي يتضمن:
1. ملخص الوضع الحالي
2. أبرز النتائج
3. التوصيات المحددة
4. الخطوات التالية المقترحة"""},
            {"role": "user", "content": f"السؤال: {question}\n\nنتائج التحليل:\n{combined_results}"}
        ]
    )

    final_answer = final_response.choices[0].message.content
    print(f"\n📋 التقرير النهائي:\n{final_answer}")

    return {
        "question": question,
        "tools_used": list(tools_results.keys()),
        "results": tools_results,
        "final_report": final_answer
    }


if __name__ == "__main__":
    result = run_orchestrator("أعطني تقرير شامل عن أداء كل الحملات وكيف أحسنها؟")
    print("\n" + "="*60)
    print(f"✅ الأدوات المستخدمة: {result['tools_used']}")
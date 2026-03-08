from groq import Groq
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.campaign_tools import get_campaign_summary, compare_campaigns, get_optimization_tips

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# تعريف الـ Tools للـ Agent
TOOLS = {
    "get_campaign_summary": get_campaign_summary,
    "compare_campaigns": compare_campaigns,
    "get_optimization_tips": get_optimization_tips,
}

SYSTEM_PROMPT = """
أنت OskoAI، خبير تسويق رقمي ذكي. عندك 3 أدوات:

1. get_campaign_summary(campaign_name) — تحلل حملة معينة
   الحملات المتاحة: Google_Ads, Meta_Ads, Email_Campaign

2. compare_campaigns() — تقارن بين كل الحملات

3. get_optimization_tips() — تعطي توصيات تحسين

للرد على أي سؤال، اتبع هذا الأسلوب:
THINK: [فكر شو تحتاج]
TOOL: [اسم الأداة]
INPUT: [المدخل]
RESULT: [نتيجة الأداة]
ANSWER: [جوابك النهائي للمستخدم]
"""

def run_agent(question: str) -> str:
    print(f"\n🤖 السؤال: {question}")
    print("=" * 50)

    # الخطوة 1: الـ Agent يفكر ويختار الـ Tool
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0
    )

    agent_response = response.choices[0].message.content
    print(f"🧠 تفكير الـ Agent:\n{agent_response}")

    # الخطوة 2: نشغّل الـ Tool اللي اختارها
    tool_result = ""
    for tool_name, tool_func in TOOLS.items():
        if tool_name in agent_response:
            if "INPUT:" in agent_response:
                input_line = [l for l in agent_response.split("\n") if "INPUT:" in l]
                tool_input = input_line[0].replace("INPUT:", "").strip() if input_line else ""
            else:
                tool_input = ""
            tool_result = tool_func(tool_input)
            print(f"\n🔧 Tool نفّذت: {tool_name}")
            print(f"📊 النتيجة:\n{tool_result}")
            break

    # الخطوة 3: الـ Agent يعطي الجواب النهائي
    if tool_result:
        messages.append({"role": "assistant", "content": agent_response})
        messages.append({"role": "user", "content": f"نتيجة الأداة:\n{tool_result}\n\nالآن أعطني الجواب النهائي."})

        final_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0
        )
        final_answer = final_response.choices[0].message.content
    else:
        final_answer = agent_response

    print(f"\n✅ الجواب النهائي:\n{final_answer}")
    return final_answer


if __name__ == "__main__":
    run_agent("قارن بين الحملات وقل لي أيها أفضل وليش؟")
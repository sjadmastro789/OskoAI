# 🤖 OskoAI — Marketing Optimization Agent

نظام ذكاء اصطناعي متكامل لتحليل وتحسين الحملات التسويقية

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.54-red)
![Groq](https://img.shields.io/badge/Groq-LLaMA3.3-green)

---

## 🎯 المشكلة

الشركات تُنفق ميزانيات ضخمة على الحملات الإعلانية دون تحليل دقيق،
مما يؤدي لضياع جزء كبير من الميزانية على حملات ضعيفة الأداء.

## 💡 الحل

OskoAI نظام Multi-Agent ذكي يحلل أداء الحملات تلقائياً
ويعطي توصيات محددة لتحسين الـ ROI بضغطة زر.

---

## 🏗️ معمارية النظام
```
[المستخدم]
     ↓
[Orchestrator Agent] ← الدماغ الرئيسي
     ↓
┌────┬────────┬──────────┐
↓    ↓        ↓          ↓
[Analytics] [Content] [Budget]
 Agent       Agent     Agent
     ↓
[data/campaigns.csv]
     ↓
[Final Recommendations]
```

---

## 🤖 الـ Agents

| Agent | المهمة |
|-------|--------|
| 🎯 Orchestrator | يختار الأدوات ويولّد تقارير شاملة |
| 🔬 Analytics | يحلل الاتجاهات ويكشف الشذوذات |
| ✍️ Content | يولّد نسخ إعلانية محسّنة |
| 💰 Budget | يوزع الميزانية ويتنبأ بالـ ROI |

---

## 📊 الـ Tools المبنية

- `compare_campaigns` — مقارنة أداء الحملات
- `analyze_trends` — تحليل الاتجاهات عبر الزمن
- `detect_anomalies` — كشف الأيام غير الطبيعية
- `get_best_days` — أفضل وأسوأ أيام لكل حملة
- `allocate_budget` — توزيع الميزانية بذكاء
- `roi_forecast` — توقعات الـ ROI للأشهر القادمة
- `optimize_underperforming` — تحسين الحملات الضعيفة
- `generate_ad_copy` — توليد إعلانات A/B

---

## 🛠️ Tech Stack

| التقنية | الاستخدام |
|---------|-----------|
| Python 3.11 | لغة البرمجة |
| Groq LLaMA 3.3 | نموذج الذكاء الاصطناعي |
| Streamlit | واجهة المستخدم |
| Pandas | تحليل البيانات |
| Plotly | الرسوم البيانية |

---

## 🚀 كيف تشغّل المشروع
```bash
# 1. استنسخ المشروع
git clone https://github.com/sjadmastro789/OskoAI.git
cd OskoAI

# 2. فعّل البيئة
python -m venv venv
venv\Scripts\activate

# 3. ثبّت المكتبات
pip install -r requirements.txt

# 4. أضف الـ API Key
echo GROQ_API_KEY=your_key_here > .env

# 5. أنشئ البيانات
python data/create_mock_data.py

# 6. شغّل التطبيق
streamlit run ui/dashboard.py
```

---

## 📁 هيكل المشروع
```
OskoAI/
├── agents/
│   ├── orchestrator.py      # الدماغ الرئيسي
│   ├── analytics_agent.py   # تحليل البيانات
│   ├── content_agent.py     # توليد الإعلانات
│   └── budget_agent.py      # إدارة الميزانية
├── data/
│   ├── campaigns.csv        # بيانات الحملات
│   └── create_mock_data.py  # إنشاء البيانات
├── tools/
│   └── campaign_tools.py    # أدوات التحليل
├── ui/
│   └── dashboard.py         # واجهة Streamlit
├── docs/
│   └── architecture.png     # معمارية النظام
└── requirements.txt
```

---

## 👨‍💻 المطور

**OskoAI** — مشروع في مجال AI Agents
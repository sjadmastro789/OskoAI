import pandas as pd

def get_campaign_summary(campaign_name: str) -> str:
    """تجيب ملخص أداء حملة معينة"""
    df = pd.read_csv("data/campaigns.csv")
    campaign_df = df[df["campaign_name"] == campaign_name]

    if campaign_df.empty:
        return f"ما وجدت حملة باسم: {campaign_name}"

    return f"""
📊 ملخص حملة: {campaign_name}
- متوسط CTR:  {campaign_df['CTR'].mean():.2f}%
- متوسط ROAS: {campaign_df['ROAS'].mean():.2f}x
- متوسط CPA:  {campaign_df['CPA'].mean():.2f}$
- إجمالي الإنفاق:  ${campaign_df['spend'].sum():.2f}
- إجمالي الإيراد: ${campaign_df['revenue'].sum():.2f}
"""

def compare_campaigns(_input: str = "") -> str:
    """تقارن بين جميع الحملات"""
    df = pd.read_csv("data/campaigns.csv")
    comparison = df.groupby("campaign_name")[["CTR","ROAS","CPA","spend","revenue"]].mean().round(2)
    best_roas = comparison["ROAS"].idxmax()
    return f"""
📈 مقارنة الحملات:
{comparison.to_string()}

🏆 أفضل حملة ROAS: {best_roas}
"""

def get_optimization_tips(_input: str = "") -> str:
    """تعطي توصيات تحسين بناءً على البيانات"""
    df = pd.read_csv("data/campaigns.csv")
    comparison = df.groupby("campaign_name")[["ROAS","CPA","spend"]].mean().round(2)
    best = comparison["ROAS"].idxmax()
    worst = comparison["ROAS"].idxmin()

    return f"""
💡 توصيات OskoAI:
- زد ميزانية {best} — أعلى ROAS ({comparison.loc[best,'ROAS']}x)
- راجع {worst} — أقل ROAS ({comparison.loc[worst,'ROAS']}x)
- متوسط CPA الكلي: ${df['CPA'].mean():.2f}
"""
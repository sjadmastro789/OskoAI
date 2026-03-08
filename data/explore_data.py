import pandas as pd

df = pd.read_csv("data/campaigns.csv")

print("=" * 40)
print("📊 تقرير OskoAI - تحليل الحملات")
print("=" * 40)

print(f"\n✅ إجمالي الصفوف: {len(df)}")
print(f"✅ عدد الحملات: {df['campaign_name'].nunique()}")
print(f"✅ الفترة الزمنية: {df['date'].min()} → {df['date'].max()}")

print("\n📈 متوسط الأداء لكل حملة:")
summary = df.groupby("campaign_name")[["CTR","ROAS","CPA","spend","revenue"]].mean().round(2)
print(summary)

print("\n🏆 أفضل حملة ROAS:")
best = df.groupby("campaign_name")["ROAS"].mean().idxmax()
print(f"   {best}")

print("\n💸 إجمالي الإنفاق vs الإيراد:")
print(f"   إجمالي الإنفاق:  ${df['spend'].sum():.2f}")
print(f"   إجمالي الإيراد: ${df['revenue'].sum():.2f}")
print(f"   صافي الربح:     ${df['revenue'].sum() - df['spend'].sum():.2f}")
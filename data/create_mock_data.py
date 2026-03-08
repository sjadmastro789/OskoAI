import pandas as pd
import random

random.seed(42)

campaigns = []

for day in range(1, 31):
    for campaign in ["Google_Ads", "Meta_Ads", "Email_Campaign"]:
        spend = round(random.uniform(100, 1000), 2)
        revenue = round(random.uniform(200, 3000), 2)
        clicks = random.randint(50, 500)
        impressions = random.randint(1000, 10000)
        conversions = random.randint(5, 50)

        campaigns.append({
            "date": f"2024-01-{day:02d}",
            "campaign_name": campaign,
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "spend": spend,
            "revenue": revenue,
            "CTR": round(clicks / impressions * 100, 2),
            "CPA": round(spend / conversions, 2),
            "ROAS": round(revenue / spend, 2)
        })

df = pd.DataFrame(campaigns)
df.to_csv("data/campaigns.csv", index=False)

print("✅ تم إنشاء الملف: data/campaigns.csv")
print(f"عدد الصفوف: {len(df)}")
print("\nأول 5 صفوف:")
print(df.head())
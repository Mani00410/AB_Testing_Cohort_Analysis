# Project 2: A/B Testing & Cohort Analysis
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from scipy import stats

# ---------- 1. Generate Dummy Dataset ----------
num_users = 1000
user_ids = [f'U{2000+i}' for i in range(num_users)]
groups = np.random.choice(['A','B'], size=num_users)
feature_used = np.random.choice(['FeatureX','FeatureY'], size=num_users)
session_duration = np.random.randint(5,120, size=num_users)
conversion = [1 if g=='B' and random.random()<0.55 else 1 if g=='A' and random.random()<0.45 else 0 for g in groups]
signup_dates = [datetime(2025,1,1)+timedelta(days=random.randint(0,90)) for _ in range(num_users)]
last_active_dates = [date+timedelta(days=random.randint(0,30)) for date in signup_dates]

df_ab = pd.DataFrame({
    'user_id': user_ids,
    'group': groups,
    'feature_used': feature_used,
    'session_duration': session_duration,
    'conversion': conversion,
    'signup_date': signup_dates,
    'last_active_date': last_active_dates
})

df_ab.to_csv('ab_test.csv', index=False)
print("Dataset created: ab_test.csv")

# ---------- 2. A/B Test Analysis ----------
conv_a = df_ab[df_ab['group']=='A']['conversion']
conv_b = df_ab[df_ab['group']=='B']['conversion']

t_stat, p_val = stats.ttest_ind(conv_a, conv_b)
print(f"\nA/B Test p-value: {p_val:.4f}")

conv_rate_a = conv_a.mean() * 100
conv_rate_b = conv_b.mean() * 100
print(f"Control A Conversion: {conv_rate_a:.2f}%")
print(f"Variant B Conversion: {conv_rate_b:.2f}%")

# ---------- 3. Cohort Analysis ----------
df_ab['signup_month'] = pd.to_datetime(df_ab['signup_date']).dt.to_period('M')
df_ab['retention_7d'] = ((pd.to_datetime(df_ab['last_active_date'])-pd.to_datetime(df_ab['signup_date'])).dt.days>=7).astype(int)
df_ab['retention_14d'] = ((pd.to_datetime(df_ab['last_active_date'])-pd.to_datetime(df_ab['signup_date'])).dt.days>=14).astype(int)
df_ab['retention_30d'] = ((pd.to_datetime(df_ab['last_active_date'])-pd.to_datetime(df_ab['signup_date'])).dt.days>=30).astype(int)

cohort_retention = df_ab.groupby('signup_month')[['retention_7d','retention_14d','retention_30d']].mean()*100
print("\nCohort Retention % per month:\n", cohort_retention)

# ---------- 4. Funnel Analysis ----------
total_users = len(df_ab)
feature_users = df_ab[df_ab['feature_used']=='FeatureX'].shape[0]
converted_users = df_ab['conversion'].sum()

funnel_featurex = feature_users / total_users * 100
funnel_conversion = converted_users / total_users * 100
print(f"\nFeatureX Usage Funnel: {funnel_featurex:.2f}%")
print(f"Overall Conversion Funnel: {funnel_conversion:.2f}%")
project2_ab_test.py
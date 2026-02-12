import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

n = 5000
data = []

for i in range(n):
    debtor_id = f'DEBTOR_{i:05d}'
    age = np.random.randint(18, 85)
    fico_score = np.random.randint(300, 850)
    days_overdue = np.random.choice([np.random.randint(1, 30), np.random.randint(31, 90), np.random.randint(91, 180), np.random.randint(181, 365)], p=[0.4, 0.3, 0.2, 0.1])
    income_level = np.random.choice(['low', 'medium', 'high'], p=[0.5, 0.35, 0.15])
    has_collateral = int(np.random.random() < 0.25)
    region_risk = np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.2, 0.4, 0.2, 0.1])
    payment_history = np.random.beta(2, 5) * 100
    bankruptcy_flag = int(np.random.random() < 0.03)
    pensioner_flag = int(age >= 60 and np.random.random() < 0.6)
    
    base_prob = 0.7
    base_prob -= days_overdue * 0.0015
    base_prob += (fico_score - 500) * 0.0008
    base_prob += has_collateral * 0.15
    base_prob -= (region_risk - 1) * 0.05
    base_prob += (payment_history / 100) * 0.2
    if bankruptcy_flag: base_prob *= 0.05
    if pensioner_flag: base_prob *= 0.3
    
    recovery_prob = np.clip(base_prob + np.random.normal(0, 0.08), 0, 1)
    
    data.append({
        'debtor_id': debtor_id,
        'age': age,
        'fico_score': fico_score,
        'days_overdue': days_overdue,
        'income_level': income_level,
        'has_collateral': has_collateral,
        'region_risk': region_risk,
        'payment_history': round(payment_history, 2),
        'bankruptcy_flag': bankruptcy_flag,
        'pensioner_flag': pensioner_flag,
        'recovery_probability': round(recovery_prob, 4)
    })

df = pd.DataFrame(data)
df.to_csv('data/raw/debtors_synthetic.csv', index=False, encoding='utf-8-sig')

print(f'✅ Сгенерировано {len(df)} должников')
print(f'📊 Статистика вероятности взыскания:')
print(f'   Мин: {df["recovery_probability"].min():.2%}')
print(f'   Макс: {df["recovery_probability"].max():.2%}')
print(f'   Среднее: {df["recovery_probability"].mean():.2%}')
print(f'⚠️  Регуляторные ловушки:')
print(f'   Банкротство: {df["bankruptcy_flag"].sum()} должников ({df["bankruptcy_flag"].mean():.1%})')
print(f'   Пенсионеры: {df["pensioner_flag"].sum()} должников ({df["pensioner_flag"].mean():.1%})')
print(f'💾 Файл сохранён: data/raw/debtors_synthetic.csv')

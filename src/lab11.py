from pathlib import Path
import pandas as pd

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 20)

# Варіант 6

# 1. Завантаження даних
BASE_DIR = Path(__file__).resolve().parent.parent
df = pd.read_csv(BASE_DIR / 'data' / 'sales_data.csv', parse_dates=['date'])

# 2. Первинний аналіз даних
print("Перші 5 рядків:")
print(df.head())
print("\nЗагальна інформація:")
df.info()
print("\nСтатистичні характеристики:")
print(df.describe())

# 3. Фільтрація: price між 1-м (25%) та 3-м (75%) квартилями
q1 = df['price'].quantile(0.25)
q3 = df['price'].quantile(0.75)
print(f"Q1 = {q1}, Q3 = {q3}")
filtered_df = df[(df['price'] >= q1) & (df['price'] <= q3)]
print("\nВідфільтровані дані:")
print(filtered_df)

# 4. Сортування за total_amount (quantity * price) у порядку спадання
# total_amount ще не існує, тому спочатку обчислюємо його
df['total_amount'] = df['quantity'] * df['price']
sorted_df = df.sort_values(by='total_amount', ascending=False)
print("\nВідсортовані дані:")
print(sorted_df)

# 5. Групування за product_id та стандартне відхилення price
grouped_df = df.groupby('product_id')['price'].std().reset_index()
grouped_df = grouped_df.rename(columns={'price': 'price_std'})
print("\nЗгруповані дані:")
print(grouped_df)

# 6. Додавання стовпця month
df['month'] = df['date'].dt.month
print("\nДані з новим стовпцем month:")
print(df)

# 7. Видалення стовпців quantity та price
df = df.drop(columns=['quantity', 'price'])
print("\nДані після видалення стовпців:")
print(df)

# 8. Обробка пропущених значень: date -> найближча попередня дата
print("\nПропущених значень у date до обробки:", df['date'].isna().sum())
df['date'] = df['date'].ffill()
print("Пропущених значень у date після обробки:", df['date'].isna().sum())
print("\nДані після заповнення пропущених значень:")
print(df)

# 9. Зведена таблиця: рядки - month, стовпці - store_id,
# значення - кількість унікальних product_id
pivot_table = df.pivot_table(values='product_id', index='month',
                             columns='store_id', aggfunc='nunique')
print("\nЗведена таблиця:")
print(pivot_table)
import pandas as pd
df = pd.read_excel('listings_manual.xlsx')
print('✅ Kolumny z danymi (0 brak = super):')
for c in ['brand','model','year','mileage','fuel_type','capacity','power','currency','transmission','color','doors','body_type','condition','price']:
    empties = (df[c].astype(str).str.len()==0) | df[c].isna()
    print(f'  {c:15}: {int(empties.sum())} brak')
print('\n📊 Przykład wiersza #1:')
row = df.iloc[0][['url','brand','model','year','mileage','fuel_type','capacity','power','price','currency','transmission','color','doors','body_type','condition']]
for k,v in row.items():
    print(f'  {k:15}: {v}')

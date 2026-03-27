FILE = r'C:\HDCS_Project\03\GNI_Autonomous\src\app\page.tsx'
with open(FILE, 'r', encoding='utf-8', errors='surrogateescape') as f:
    content = f.read()
print('File length:', len(content))
for term in ['latestArticles', 'Three Pillar', 'Quadratic']:
    print(f'{term}:', content.find(term))
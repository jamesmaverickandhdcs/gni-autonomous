FILE = r'C:\HDCS_Project\03\GNI_Autonomous\src\app\page.tsx'
with open(FILE, 'r', encoding='utf-8', errors='surrogateescape') as f:
    content = f.read()

idx = content.find('bg-yellow-900 border border-yellow-700')
print('Disclaimer at:', idx)
print(repr(content[idx-300:idx+50]))
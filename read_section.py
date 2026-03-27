# read_section.py
FILE = r'C:\HDCS_Project\03\GNI_Autonomous\src\app\page.tsx'
with open(FILE, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

print('=== PREVIOUS REPORTS SECTION ===')
idx = content.find('Previous Reports')
print(repr(content[idx-300:idx+600]))

print()
print('=== DISCLAIMER SECTION ===')
idx2 = content.find('Disclaimer:')
print(repr(content[idx2-300:idx2+200]))
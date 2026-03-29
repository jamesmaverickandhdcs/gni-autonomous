with open("src/app/quota/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Find Cross-Navigation block
idx = content.find("Cross-Navigation")
print("=== CROSS-NAV BLOCK ===")
print(repr(content[idx-10:idx+600]))

# Find Dashboard link
idx2 = content.find("← Dashboard") 
if idx2 == -1:
    idx2 = content.find("larr; Dashboard")
print("\n=== DASHBOARD LINK ===")
print(repr(content[idx2-100:idx2+100]))
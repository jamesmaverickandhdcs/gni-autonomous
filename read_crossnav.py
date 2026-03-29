# Print the cross-nav block from brief to see exact pattern
with open("src/app/brief/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Find Cross-nav section
idx = content.find("Cross-nav")
print(repr(content[idx-50:idx+500]))
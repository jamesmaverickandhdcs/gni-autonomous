c = open('src/app/transparency/page.tsx', 'rb').read()

# Fix broken emoji bytes - identify exact sequences
# Run diagnostic first
import re

text = c.decode('utf-8', errors='replace')

# Find broken sequences
print("Header area:", repr(text[text.find('GNI Transparency'):text.find('GNI Transparency')+60]))
print("Arrow area:", repr(text[text.find('Collected'):text.find('Collected')+80]))
print("Description:", repr(text[text.find('Explainable AI'):text.find('Explainable AI')+50]))

with open('src/app/about/page.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('Total lines:', len(lines))
print()

# Print all lines with line numbers
for i, line in enumerate(lines, start=1):
    print(str(i).rjust(3) + ': ' + line, end='')
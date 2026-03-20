content = open('.gitignore', encoding='utf-8').read()
if 'fix_*.py' not in content:
    content += '\n# Temporary fix/check scripts\nfix_*.py\nwrite_*.py\ncheck_*.py\n'
    open('.gitignore', 'w', encoding='utf-8').write(content)
    print('Added to .gitignore')
else:
    print('Already present')

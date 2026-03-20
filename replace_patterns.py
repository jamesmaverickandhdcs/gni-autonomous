content = open('ai_engine/funnel/intelligence_funnel.py', encoding='utf-8').read()

new_patterns = """INJECTION_PATTERNS = [
    # Category 1: Direct instruction overrides
    r'ignore\\s+(previous|prior|above|all)\\s+instructions?',
    r'disregard\\s+(previous|prior|above|all)\\s+instructions?',
    r'forget\\s+(previous|prior|above|all)\\s+instructions?',
    r'override\\s+(previous|prior|above|all)\\s+instructions?',
    r'new\\s+instructions?\\s*:',
    r'updated\\s+instructions?\\s*:',
    r'system\\s*:\\s*you\\s+are',
    r'you\\s+are\\s+now\\s+(a\\s+)?(?:different|new|another)',
    r'act\\s+as\\s+(a|an)\\s+\\w+',
    r'pretend\\s+(you\\s+are|to\\s+be)',
    r'roleplay\\s+as',
    r'from\\s+now\\s+on\\s+(you|act|behave)',
    r'your\\s+new\\s+(role|persona|identity|task)\\s+is',
    # Category 2: Score manipulation
    r'rate\\s+this\\s+article\\s+[0-9]+\\s*/\\s*[0-9]+',
    r'score\\s*[=:]\\s*[0-9]+',
    r'set\\s+(score|rating|priority)\\s+to',
    r'give\\s+(this|all)\\s+(article|story)\\s+a\\s+(score|rating)',
    r'mark\\s+(all|this)\\s+(others?|article)',
    r'rank\\s+(this|all)\\s+(article|story)\\s+(as|at)\\s+(top|highest|first)',
    # Category 3: Bias manipulation
    r'(system|admin|root)\\s*:\\s*(override|bypass|ignore)',
    r'always\\s+(rate|score|rank)\\s+(israel|iran|us|china|russia)\\s+as',
    r'ignore\\s+(all\\s+)?(article|news)\\s+(from|about)',
    r'filter\\s+out\\s+(all\\s+)?(article|news)\\s+(from|about)',
    r'never\\s+(report|include|select)\\s+(news|article)\\s+(about|from)',
    # Category 4: Prompt boundary attacks
    r'```\\s*(system|assistant|user)\\s*```',
    r'<\\s*system\\s*>',
    r'\\[INST\\]',
    r'\\[\\/INST\\]',
    r'<<SYS>>',
    r'<</SYS>>',
    r'human\\s*:\\s*ignore',
    r'assistant\\s*:\\s*sure',
    r'<\\|system\\|>',
    r'<\\|user\\|>',
    r'<\\|assistant\\|>',
    r'\\[SYSTEM\\]',
    r'\\[USER\\]',
    r'\\[ASSISTANT\\]',
    # Category 5: Encoded attacks
    r'aWdub3Jl',
    r'aW5zdHJ1Y3Rpb24',
    r'base64\\s*:\\s*[A-Za-z0-9+/=]{20,}',
    r'&#x[0-9a-fA-F]{2};.*ignore',
    # Category 6: Multilingual injections
    r'ignorez\\s+les\\s+instructions',
    r'ignorar\\s+las\\s+instrucciones',
    r'ignorieren\\s+sie\\s+die\\s+anweisungen',
    r'ignora\\s+(le\\s+)?istruzioni',
    # Category 7: Role confusion and jailbreak
    r'(unlock|enable|activate)\\s+(developer|god|admin|root|jailbreak)\\s+mode',
    r'DAN\\s+(mode|protocol|is\\s+now)',
    r'jailbreak(ed|\\s+mode|\\s+prompt)?',
    r'(bypass|circumvent|override)\\s+(safety|filter|restriction|guideline)',
    r'(forget|ignore)\\s+(that\\s+)?(you\\s+are\\s+an?\\s+)?(ai|assistant|bot)',
    # Category 8: Context overflow
    r'\\[\\s*IGNORE\\s*EVERYTHING\\s*ABOVE\\s*\\]',
    r'###\\s*(end|stop|ignore)\\s*(above|previous|all)',
    r'-{10,}\\s*(new\\s+instruction|system\\s+prompt)',
    # Category 9: Nested injections
    r'the\\s+article\\s+says\\s+(to\\s+)?(ignore|override|disregard)',
    r'urgent\\s*:\\s*(ignore|override|disregard)\\s+(all\\s+)?instructions?',
    # Category 10: Code execution and data exfiltration
    r'print\\s*\\(',
    r'exec\\s*\\(',
    r'eval\\s*\\(',
    r'__import__',
    r'send\\s+(all|this)\\s+(data|article|information)\\s+to',
    r'forward\\s+(all|this)\\s+(data|article|information)\\s+to',
    r'exfiltrate\\s+(data|information|results)',
    r'http[s]?://(?!www\\.(aljazeera|cnn|foxnews|bbc|dw|reuters|bloomberg|nikkei|wired|technologyreview|france24|usni|straitstimes|rcinet)\\.(com|org|net|co))',
]"""

result = content[:2377] + new_patterns + content[3000:]

with open('ai_engine/funnel/intelligence_funnel.py', 'w', encoding='utf-8', newline='\n') as f:
    f.write(result)

# Verify
c2 = open('ai_engine/funnel/intelligence_funnel.py', encoding='utf-8').read()
import re
patterns_match = re.search(r'INJECTION_PATTERNS = \[(.*?)\]', c2, re.DOTALL)
if patterns_match:
    count = len(re.findall(r"r'", patterns_match.group(1)))
    print(f'Done - {count} patterns in funnel')
else:
    print('ERROR - patterns not found')
print('_check_injection present:', 'def _check_injection' in c2)
print('DAN pattern present:', 'DAN' in c2)

import json
import re

nb_path = '/Users/mac/Dropbox/Agentix AI/Research Phd/R5-Fatwa AI/paper-source-code/R5-Fatwa AI-reproducible.ipynb'

with open(nb_path, 'r') as f:
    nb = json.load(f)

# Regex to find sk-proj keys or anything assigned to api_key=
def redact(text):
    text = re.sub(r'sk-[a-zA-Z0-9\-_]{20,}', 'YOUR_OPENAI_API_KEY', text)
    text = re.sub(r'ck-[a-zA-Z0-9\-_]{20,}', 'YOUR_CHROMA_API_KEY', text)
    return text

for c in nb['cells']:
    if 'source' in c:
        for i, line in enumerate(c['source']):
            c['source'][i] = redact(line)

with open(nb_path, 'w') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

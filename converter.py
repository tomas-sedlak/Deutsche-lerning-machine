import pdfplumber

pairs = []
with pdfplumber.open("data/Wortliste_4_en.pdf") as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            for row in table[1:]:
                if not row[1]: continue
                de, en = row[0].strip(), row[1].strip()
                pairs.append({"de": de, "en": en})


import json

with open("data/b1_en_vocab.json", "w", encoding="utf‑8") as f:
    json.dump(pairs, f, ensure_ascii=False, indent=2)
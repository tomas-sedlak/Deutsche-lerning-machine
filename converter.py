import pdfplumber

input_path = "data/Wortliste_4_en.pdf"
output_path = "data/b1_en_vocab.json"

lectures = []
current_lecture = None
current_vocab = []

with pdfplumber.open(input_path) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        if not tables: continue
        for table in tables:
            for row in table[1:]:
                if not row[1]:  # This is a new lection
                    # Save previous lection if exists
                    if current_lecture and current_vocab:
                        lectures.append({
                            "lecture": current_lecture,
                            "vocabulary": current_vocab
                        })
                    
                    # Start new lection
                    current_lecture = row[0].strip()
                    current_vocab = []
                else:  # This is vocabulary
                    de, en = row[0].strip(), row[1].strip()
                    current_vocab.append({"de": de, "en": en})

# Don't forget to save the last lection
if current_lecture and current_vocab:
    lectures.append({
        "lecture": current_lecture,
        "vocabulary": current_vocab
    })

import json

with open(output_path, "w", encoding="utf‑8") as f:
    json.dump(lectures, f, ensure_ascii=False, indent=2)
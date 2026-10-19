import pandas as pd
import re
import os

# === File paths ===
input_file = "data/deidentified/deidentified_notes.csv"
output_file = "outputs/ner_entities_regex.csv"

# === Load de-identified notes ===
df_notes = pd.read_csv(input_file)

# === Validate required column ===
if 'deidentified_note' not in df_notes.columns:
    raise ValueError("'deidentified_note' column not found.")

# === Define regex patterns for different entity types ===
patterns = {
    "DATE": r"\b(?:\d{1,2}[/-])?\d{1,2}[/-]\d{2,4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{2,4}",
    "PHONE": r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "HOSPITAL": r"\b[A-Z][a-z]+ (General|Hospital|Clinic|Medical Center)\b",
    "VITALS": r"\b\d{2,3}/\d{2,3}|\d{1,3}\.\d{1} (°F|°C|mg/dL|mmHg)\b",
    "ID": r"\bID[:\s]*\d{3,}\b"
}

# === Initialize list for results ===
results = []

# === Loop through each note and apply patterns ===
for idx, note in enumerate(df_notes['deidentified_note']):
    for label, pattern in patterns.items():
        for match in re.finditer(pattern, note):
            results.append({
                "note_id": idx,
                "entity": match.group(),
                "entity_group": label,
                "start": match.start(),
                "end": match.end()
            })

# === Save the extracted entities ===
os.makedirs("outputs", exist_ok=True)
df_result = pd.DataFrame(results)
df_result.to_csv(output_file, index=False)

print(f"Regex entity extraction complete. Output saved to {output_file}")
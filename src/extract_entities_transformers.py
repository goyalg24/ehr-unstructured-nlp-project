from transformers import pipeline
import pandas as pd
import os

# === File paths ===
input_file = "data/deidentified/deidentified_notes.csv"
output_file = "outputs/ner_entities_transformers.csv"

# === Load de-identified notes from CSV ===
df_notes = pd.read_csv(input_file)

# Ensure required column exists
if 'deidentified_note' not in df_notes.columns:
    raise ValueError(f"'deidentified_note' column not found in {input_file}")

# === Load NER model from Hugging Face Transformers ===
ner_pipeline = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple"  # Group overlapping tokens into full entities
)

# === Extract entities from each note ===
results = []
for i, note in enumerate(df_notes['deidentified_note']):
    entities = ner_pipeline(note)
    for ent in entities:
        results.append({
            "note_id": df_notes.loc[i, "note_id"],  # Preserve original note ID
            "entity": ent['word'],
            "entity_group": ent['entity_group'],  # Entity type (e.g., PERSON, ORG)
            "start": ent['start'],
            "end": ent['end'],
            "score": round(ent['score'], 3)  # Confidence score
        })

# === Save extracted entities to CSV ===
os.makedirs("outputs", exist_ok=True)
df = pd.DataFrame(results)
df.to_csv(output_file, index=False)

print(f"Entity extraction complete. Output saved to {output_file}")
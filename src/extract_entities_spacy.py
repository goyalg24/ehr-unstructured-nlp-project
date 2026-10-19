import os
import spacy
import pandas as pd

# === Load spaCy model ===
nlp = spacy.load("en_core_web_sm")

# === Define file paths ===
input_csv = "data/deidentified/deidentified_notes.csv"
output_dir = "output/entities_spacy"
os.makedirs(output_dir, exist_ok=True)

# === Load de-identified notes ===
df = pd.read_csv(input_csv)

# === Identify the column containing the text ===
# Defaults to the last column if 'note' is not explicitly present
text_column = 'note' if 'note' in df.columns else df.columns[-1]

# === Loop over each note and extract entities ===
for i, text in enumerate(df[text_column]):
    # Skip non-string or empty inputs
    if not isinstance(text, str) or not text.strip():
        continue

    # Run NLP pipeline
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Save results to file if entities were found
    if entities:
        out_path = os.path.join(output_dir, f"note_{i+1}_entities.txt")
        with open(out_path, "w") as f:
            for ent_text, ent_label in entities:
                f.write(f"{ent_text}\t{ent_label}\n")

print("Entity extraction complete.")
# EHR Unstructured NLP Pipeline (GCP + AI)

This project extracts structured insights from synthetic EHR notes using de-identification and NER techniques. Synthetic FHIR bundles are parsed into structured tables, turned into free-text clinical notes, de-identified with the Google Cloud DLP API, and then run through several entity-extraction approaches (regex, spaCy, medspaCy, Hugging Face BERT NER, and the Google Healthcare Natural Language API). De-identified notes can be loaded into BigQuery. It demonstrates full-stack data engineering and AI/ML skills.

## Features
- FHIR parsing and note generation
- DLP API-based de-identification
- Regex, spaCy, medspaCy and Hugging Face NER (BERT-based)
- Healthcare Natural Language API entity analysis (via Vertex AI / Healthcare API)
- Outputs pushed to CSV for BigQuery ingestion

## Tech Stack
- Python, pandas, spaCy, medspaCy, transformers
- GCP: Cloud Storage, DLP, BigQuery, Vertex AI
- Airflow/Dagster (planned for orchestration)
- IAM roles configured via service accounts

## Project Structure

```
ehr-unstructured-nlp-project/
├── configs/
│   └── vertex_config.yaml              # placeholder for Vertex AI settings
├── orchestration/
│   └── dag_pipeline.py                 # placeholder for an Airflow DAG
├── output/
│   └── interim_output.csv              # sample de-identified notes (note_id, deidentified_note)
├── src/
│   ├── fhir_parser.py                  # data/fhir/*.json -> data/structured/*.csv
│   ├── generate_notes.py               # data/structured -> data/unstructured/clinical_notes.csv
│   ├── deidentify_notes.py             # DLP API -> data/deidentified/deidentified_notes.csv
│   ├── extract_entities_regex.py       # regex NER -> outputs/ner_entities_regex.csv
│   ├── extract_entities_transformers.py# dslim/bert-base-NER -> outputs/ner_entities_transformers.csv
│   ├── extract_entities_spacy.py       # en_core_web_sm -> output/entities_spacy/*.txt
│   ├── extract_entities_medspacy.py    # medspaCy rule-based NER (prints results)
│   ├── extract_entities_vertexai.py    # Healthcare NLP API (prints results)
│   ├── load_to_bigquery.py             # de-identified notes -> BigQuery ehr_pipeline.deidentified_notes
│   └── ocr_pipeline.py                 # placeholder for a Document AI OCR step
├── requirements.txt
└── README.md
```

The `data/` folder (FHIR input and intermediate CSVs) and `credentials/` are not committed; they are created locally.

## Setup

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install torch                 # backend required by the transformers pipeline
python -m spacy download en_core_web_sm
```

GCP steps (DLP, BigQuery, Healthcare NLP) need a GCP project (`ehr-unstructured-nlp-project` is hard-coded in the scripts) and credentials:
- `deidentify_notes.py` and `load_to_bigquery.py` use Application Default Credentials (`gcloud auth application-default login` or `GOOGLE_APPLICATION_CREDENTIALS`).
- `extract_entities_vertexai.py` reads a service account key from `credentials/ehr-dlp-access.json` (ignored by git; never commit it).

## Usage

Run every script from the repository root. Place synthetic FHIR bundles (e.g. from Synthea) as JSON files under `data/fhir/`, then:

```bash
python src/fhir_parser.py                    # parse FHIR bundles
python src/generate_notes.py                 # build synthetic clinical notes (up to 5000 patients)
python src/deidentify_notes.py               # redact PHI with DLP (first 400 notes)
python src/extract_entities_regex.py         # regex entities
python src/extract_entities_transformers.py  # BERT NER entities
python src/extract_entities_spacy.py         # spaCy entities
python src/extract_entities_medspacy.py      # medspaCy entities (first 5 notes)
python src/extract_entities_vertexai.py      # Healthcare NLP entities (first 5 notes)
python src/load_to_bigquery.py               # upload de-identified notes to BigQuery
```

## Outputs
- `output/interim_output.csv` — a committed sample of de-identified notes (`note_id`, `deidentified_note`), with names replaced by `Patient-<uuid>` and DOBs redacted as `[DATE_OF_BIRTH]`.
- Running the pipeline additionally produces `data/structured/*.csv`, `data/unstructured/clinical_notes.csv`, `data/deidentified/deidentified_notes.csv`, `outputs/ner_entities_*.csv` and `output/entities_spacy/`.

## Next Steps
- Orchestrate using Cloud Composer or Dagster (`orchestration/dag_pipeline.py` is a placeholder)
- Add an OCR step with Document AI (`src/ocr_pipeline.py` is a placeholder)
- Evaluate clinical NER models via Vertex AI Model Garden
- Deploy model APIs via Cloud Run

## GCP Security & IAM
- Secure buckets, private service endpoints
- Scoped IAM for DLP + NLP
- Uses `ehr-dlp-access@...` for fine-grained access

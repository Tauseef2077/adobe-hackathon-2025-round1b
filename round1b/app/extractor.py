import os
import json
from datetime import datetime
from utils import extract_text_from_pdf, infer_persona_and_job, rank_sections_by_relevance, summarize_text

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "challenge1b_output.json")

def main():
    all_sections = []
    documents = []

    for filename in sorted(os.listdir(INPUT_DIR)):
        if filename.endswith(".pdf"):
            filepath = os.path.join(INPUT_DIR, filename)
            sections = extract_text_from_pdf(filepath)
            for s in sections:
                s["document"] = filename
            all_sections.extend(sections)
            documents.append(filename)

    persona, job = infer_persona_and_job(all_sections)
    ranked = rank_sections_by_relevance(all_sections, persona, job)

    extracted_sections = []
    seen_docs = set()
    extracted_keys = set()

    for score, sec in ranked:
        key = (sec["document"], sec["page"])
        if sec["document"] not in seen_docs:
            seen_docs.add(sec["document"])
            extracted_keys.add(key)
            extracted_sections.append({
                "document": sec["document"],
                "section_title": sec["title"],
                "importance_rank": len(extracted_sections) + 1,
                "page_number": sec["page"]
            })
        if len(extracted_sections) >= len(documents):
            break

    subsection_analysis = []
    docs_used = set()

    for doc in documents:
        for score, sec in ranked:
            if sec["document"] != doc:
                continue
            key = (sec["document"], sec["page"])
            already_used = key in extracted_keys or (sec["document"] in docs_used)

            if already_used:
                continue

            if len(sec["content"].split()) >= 15:
                subsection_analysis.append({
                    "document": sec["document"],
                    "refined_text": summarize_text(sec["content"]),
                    "page_number": sec["page"]
                })
                docs_used.add(sec["document"])
                break  

    for doc in documents:
        if doc not in docs_used:
            for score, sec in ranked:
                if sec["document"] == doc:
                    subsection_analysis.append({
                        "document": sec["document"],
                        "refined_text": summarize_text(sec["content"]),
                        "page_number": sec["page"]
                    })
                    break

    output = {
        "metadata": {
            "input_documents": documents,
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=4)

if __name__ == "__main__":
    main()

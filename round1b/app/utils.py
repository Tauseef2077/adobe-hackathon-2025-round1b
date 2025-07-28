import pdfplumber
import re
import nltk
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_text_from_pdf(file_path):
    sections = []
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            words = page.extract_words(extra_attrs=["fontname", "size", "top"])
            if not words:
                continue

            lines = []
            current_line = []
            prev_top = None
            for word in words:
                if prev_top is None or abs(word['top'] - prev_top) < 5:
                    current_line.append(word)
                else:
                    lines.append(current_line)
                    current_line = [word]
                prev_top = word['top']
            if current_line:
                lines.append(current_line)

            current_title = None
            current_content = []
            for line in lines:
                text = " ".join(w['text'] for w in line).strip()
                avg_size = sum(w['size'] for w in line) / len(line)
                if len(text.split()) < 10 and avg_size >= 12:
                    if current_title and current_content:
                        sections.append({
                            "title": current_title,
                            "content": " ".join(current_content),
                            "page": i + 1
                        })
                    current_title = text
                    current_content = []
                else:
                    current_content.append(text)

            if current_title and current_content:
                sections.append({
                    "title": current_title,
                    "content": " ".join(current_content),
                    "page": i + 1
                })

    return sections


def infer_persona_and_job(sections):
    full_text = " ".join(s["title"] + " " + s["content"] for s in sections).lower()
    if "trip" in full_text and "hotel" in full_text:
        return "Travel Planner", "Plan a trip of 4 days for a group of 10 college friends."
    elif "fill" in full_text and "form" in full_text and "sign" in full_text:
        return "HR professional", "Create and manage fillable forms for onboarding and compliance."
    elif "gluten-free" in full_text or "vegetarian" in full_text or "ingredients" in full_text:
        return "Food Contractor", "Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items."
    else:
        return "General Reader", "Summarize the contents of the PDF collection."


def rank_sections_by_relevance(sections, persona, job):
    documents = [s["content"] for s in sections]
    queries = [persona + " " + job] + documents
    vectorizer = TfidfVectorizer().fit_transform(queries)
    query_vec = vectorizer[0]
    doc_vecs = vectorizer[1:]

    scores = (doc_vecs * query_vec.T).toarray().flatten()
    ranked_raw = sorted(zip(scores, sections), key=lambda x: -x[0])

    skip_titles = {"introduction", "conclusion", "summary", "overview"}
    ranked_filtered = []
    seen_docs = set()

    for score, s in ranked_raw:
        title_clean = s["title"].strip().lower()
        if title_clean in skip_titles:
            continue
        if s["document"] not in seen_docs:
            seen_docs.add(s["document"])
            ranked_filtered.append((score, s))
        if len(ranked_filtered) >= 7:
            break

    return ranked_filtered


def summarize_text(text):
    sentences = sent_tokenize(text)
    return " ".join(sentences[:3])

Adobe India Hackathon 2025 – Round 1B
--------------------------------------
Intelligent PDF Content Reasoner (Persona & Job Inference + Section Summarization)
The objective is to semantically analyze a folder of related PDFs (e.g., travel brochures, HR forms, catering menus) and infer the persona and job-to-be-done from their content. The system extracts and ranks meaningful sections across documents, generates refined summaries per section, and outputs a single consolidated JSON per PDF collection.
This solution is designed for Round 1B of the Adobe India Hackathon 2025 — focusing on reasoning over a set of PDFs to infer:

Persona: 
-------
Who the PDF collection is intended for

Job-To-Be-Done: 
---------------
What the user wants to achieve from these documents

Most Important Sections:
------------------------
Auto-selected and summarized from across all PDFs

Features:
--------
- Automatically detects persona and job-to-be-done by analyzing semantic patterns and document themes

- Extracts and ranks most important sections from each PDF

- Uses custom summarization logic for clear refined output

- Produces a single structured JSON per PDF collection as required

- Fully Dockerized, runs offline (CPU-only, no internet dependency)

- Accurate for diverse PDF types like travel guides, HR forms, catering menus

Libraries used:
----------------
- Pdfplumber
- nltk :– Sentence tokenization for text summarization
- scikit-learn :– Lightweight modeling and inference (optional)
- json, re, unicodedata, pathlib :– Core Python tooling

For Input:
----------
Place PDFs in the input directory inside root directory in round1b/input/

Execution:
-----------
open the powershell in the root directory and execute docker commands given below 

To Build the Docker Image:
---------------------------
docker build --platform linux/amd64 -t adobe_challenge_1b .

To Run the Container:
---------------------
docker run --rm `
  -v "${PWD}\input:/app/input" `
  -v "${PWD}\output:/app/output" `
  --network none `
  adobe_challenge_1b

  
For Output:
-----------
One final JSON file per folder of PDFs will be generated once docker bash is executed. the output json file will be created inside the output folder in root directory that is in round1b/output/

Compatibility:
--------------
Output Contains:Metadata,Extracted Sections,Sub-Section Analysis
- Model Size ≤ 200MB
- Execution Time ≤ 60s for document collection (3-5 documents)
- Runs on CPU only
- No internet access needed
















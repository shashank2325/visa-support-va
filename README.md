# F1 and H1B Visa Support Virtual Assistant

This project provides a Retrieval-Augmented Generation (RAG)-based Virtual Assistant to help users with F1 and H1B visa queries. It leverages state-of-the-art language models (LLaMA 3.1-8B and Mistral 7B) to generate precise and accurate answers based on official visa-related documents.

---

## Features

- Retrieves relevant visa-related content from official documents and FAQs.
- Provides accurate answers using advanced Large Language Models (LLMs).
- Supports efficient retrieval using FAISS and Sentence Transformers.

---

## Usage

### 1. Scrape and Prepare Data
Run the `scrape_files.py` script to scrape the required visa-related documents:
```bash
python scrape_files.py
```

### 2. Clean the Data
Clean the scraped data to remove unnecessary text using the `cleaning_txt.py` script:
```bash
python cleaning_txt.py
```

### 3. Combine Cleaned Data
Combine the cleaned data into a single JSON file using:
```bash
python combine_cleaned_json.py
```

### 4. Build the RAG Pipeline
Run the main retrieval and generation pipeline using:
```bash
python RetrievalNGenerator.py
```

You can query the system by modifying the `queries` list in `RetrievalNGenerator.py` or adding an interface to input queries dynamically.

---

## Project Structure

```
├── cleaned_data/          # Directory for cleaned files
├── scraped_data/          # Directory for scraped raw files
├── combined_corpus.json   # Combined corpus for FAISS retrieval
├── scrape_files.py        # Script to scrape visa-related documents
├── cleaning_txt.py        # Script to clean scraped data
├── combine_cleaned_json.py# Script to combine cleaned files into a JSON corpus
├── RetrievalNGenerator.py # Main script to run the RAG pipeline
├── requirements.txt       # List of dependencies
└── README.md              # Project documentation
```

---

## Future Work

- Add a user-friendly interface (e.g., web or CLI-based).
- Extend support for other visa categories (e.g., J1, O1).
- Implement multilingual support for non-English-speaking users.

---

## License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).

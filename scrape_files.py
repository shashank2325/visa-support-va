import os
import requests
from bs4 import BeautifulSoup
import time
import fitz  
from urllib.parse import urlparse


output_dir = "scraped_data"
os.makedirs(output_dir, exist_ok=True) 


websites = [
    {
        "url": "https://www.uscis.gov/working-in-the-united-states/students-and-exchange-visitors/students-and-employment",
        "output_file": "uscis_f1_visa.txt"
    },
    {
        "url": "https://www.uscis.gov/working-in-the-united-states/h-1b-specialty-occupations",
        "output_file": "uscis_h1b_visa.txt"
    },
    {
        "url": "https://travel.state.gov/content/travel/en/us-visas/study/student-visa.html",
        "output_file": "state_department_student_visa.txt"
    },
    {
        "url": "https://www.dol.gov/agencies/whd/immigration/h1b",
        "output_file": "dol_h1b_overview.txt"
    },
    {
        "url": "https://educationusa.state.gov/your-5-steps-us-study/apply-your-student-visa",
        "output_file": "educationusa_student_visa_faq.txt"
    },
    {
        "url": "https://www.murthy.com/h1b/",
        "output_file": "murthy_h1b_faq.txt"
    },
    {
        "url": "https://www.fragomen.com/insights.html",
        "output_file": "fragomen_insights.txt"
    },
    {
        "url": "https://shorelight.com/student-stories/student-visa-usa-f1/",
        "output_file": "shorelight_student_visa.txt"
    },
    {
        "url": "https://www.ashoorilaw.com/h1b-visa/",
        "output_file": "ashoori_law_h1b.txt"
    },
    {
        "url": "https://studyinthestates.dhs.gov/guide/f-1/f-1-postsecondary",
        "output_file": "studyinthestates.txt"
    },
    {
        "url":"https://bechtel.stanford.edu/navigate-international-life/visas/f-1-and-j-1-student-visas",
        "output_file": "bechtel.stanford.edu.txt"
    },
    {
        "url":"https://isso.ucsf.edu/travel-and-us-re-entry-f-1",
        "output_file": "isso.ucsf.edu.txt"
    },
    {
        "url":"https://iss.washington.edu/travel/visas/",
        "output_file": "iss.washington.edu.txt"
    },
    {
        "url": "https://internationalization.du.edu/sites/default/files/2022-06/h-1b-handbook-12-11-17.pdf",
        "output_file": "h1b_handbook.pdf"
    }
]

def scrape_and_save(url, output_file):
    headers = {"User-Agent": "Mozilla/5.0"}
    
    
    if url.endswith('.pdf'):
        save_pdf(url, output_file)
        return

    try:
        
        if os.path.exists(output_file):
            print(f"File {output_file} already exists. Skipping download.")
            return

        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        
        soup = BeautifulSoup(response.text, 'html.parser')

        
        paragraphs = soup.find_all('p')
        text_content = "\n".join([p.get_text(strip=True) for p in paragraphs])

        
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(text_content)

        print(f"Scraped and saved content from {url} to {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")


def save_pdf(url, output_file):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        
        with open(output_file, "wb") as pdf_file:
            pdf_file.write(response.content)
        print(f"Downloaded PDF from {url} to {output_file}")
        
        
        extract_text_from_pdf(output_file)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")


def extract_text_from_pdf(pdf_file):
    import fitz
    try:
        doc = fitz.open(pdf_file)
        text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text()

        
        text_file = pdf_file.replace(".pdf", ".txt")
        with open(text_file, "w", encoding="utf-8") as file:
            file.write(text)
        
        print(f"Extracted text from PDF and saved to {text_file}")

    except Exception as e:
        print(f"Error extracting text from {pdf_file}: {e}")


for site in websites:
    output_file_path = os.path.join(output_dir, site["output_file"])
    scrape_and_save(site["url"], output_file_path)
    time.sleep(10)

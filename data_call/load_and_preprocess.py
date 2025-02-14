import json
import re

DATA_FILE = "bites_articles_fr.json"
RESPONSE_CLEAN_FILE = "bites_articles_fr_cleaned.json"
FAISS_INDEX_PATH = "faiss_index"

def clean_text(text):
    """ Cleans text by removing newlines and trimming spaces. """
    text = re.sub(r'\s+', ' ', text).strip()
    
    text = re.sub(r'[^\w\s,.!?-]', '', text)
    
    text = re.sub(r'\s([?.!,"](?:\s|$))', r'\1', text)

    if isinstance(text, str):
        return text.replace("\n", " ").strip()
    return text

def clean_authors(authors):
    """ Cleans author list by removing unwanted characters from names and affiliations. """
    if isinstance(authors, list):
        for author in authors:
            if isinstance(author, dict):
                author["affiliation"] = clean_text(author.get("affiliation", ""))
                author["lastname"] = clean_text(author.get("lastname", ""))
                author["firstname"] = clean_text(author.get("firstname", ""))
    return authors

def clean_data():
    """ Loads, cleans, and saves the dataset. """
    input_file = "C:/antidote/data_call/bites_articles_fr.json"
    output_file = "C:/antidote/data_call/bites_articles_fr_cleaned.json"
    
    with open(input_file, "r", encoding="utf-8") as f:
        articles = json.load(f)

    for article in articles:
        article["Title"] = clean_text(article.get("Title", ""))
        article["Abstract"] = clean_text(article.get("Abstract", ""))

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    clean_data()
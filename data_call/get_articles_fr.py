from deep_translator import GoogleTranslator
import json
from pymed import PubMed

pubMed = PubMed(tool="MyTool", email="malika.vagapova@epitech.digital")

search_term = "morsures"

results = pubMed.query(search_term, max_results=1000)

articles_list = []
translator = GoogleTranslator(source="auto", target="fr")

# Traduction 
for article in results:
    article_dict = article.toDict()

    title = article_dict.get('title', "No Title")
    abstract = article_dict.get('abstract', "No Abstract")

    title_fr = translator.translate(title) if title != "No Title" else "Aucun titre"
    if abstract and isinstance(abstract, str) and abstract.strip():
        abstract_fr = translator.translate(abstract)
    else:
        abstract_fr = "Aucun résumé"

    publication_date = article_dict.get('publication_date', "No Date")
    if publication_date != "No Date":
        publication_date = publication_date.strftime('%Y-%m-%d')

    articles_list.append({
        "Title": title_fr,
        "Abstract": abstract_fr,
        "PubMed ID": article_dict.get('pubmed_id', "No ID"),
        "Publication Date": publication_date,
        "Authors": article_dict.get('authors', "No Authors")
    })

with open("bites_articles_fr.json", "w", encoding="utf-8") as json_file:
    json.dump(articles_list, json_file, indent=4, ensure_ascii=False)

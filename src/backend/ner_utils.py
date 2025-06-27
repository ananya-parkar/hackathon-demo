import spacy
import re
# Use a better model if downloaded, else fallback to small
nlp = spacy.load("xx_ent_wiki_sm")
def extract_entities(text, labels=["DATE", "ORG", "PERSON"]):
    doc = nlp(text)
    entities = [(ent.text.strip(), ent.label_) for ent in doc.ents if ent.label_ in labels]
    # 🔍 Add regex-detected dates (dd-mm-yyyy, dd/mm/yyyy, yyyy-mm-dd)
    regex_dates = re.findall(r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2})\b', text)
    for date in regex_dates:
        if (date, "DATE") not in entities:  # Avoid duplicates
            entities.append((date, "DATE"))
    return entities
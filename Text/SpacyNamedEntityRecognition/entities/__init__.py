import azure.functions as func
import spacy
import json

from spacy import displacy
from spacy.lang.nl.examples import sentences

# Load all Spacy models in memory, instead of during runtime
nlp_en = spacy.load("en_core_web_sm")
nlp_nl = spacy.load("nl_core_news_sm")

# Endpoint /


def main(req: func.HttpRequest) -> func.HttpResponse:
    text = req.params.get('text')
    lang = req.params.get('lang')

    if not text:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            text = req_body.get('text')

    if not lang:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            lang = req_body.get('lang')

    if not lang:
        lang = "nl"

    # doc = nlp(text)
    doc = extract_from_text(text, lang)

    # TODO Multiple endpoint and format result as LUIS
    if text:
        return func.HttpResponse(
            json.dumps(doc),
            headers={
                "Content-Type": "application/json",
            }
        )
    else:
        return func.HttpResponse(
            "Please pass a text on the query string or in the request body",
            status_code=400,
        )


def extract_from_text(text: str, lang: str):
    """Extract Spacy Named Entities from raw text"""
    if lang == "en":
        nlp = nlp_en
    else:
        nlp = nlp_nl

    entities = []
    
    doc = nlp(u"Apple is looking at buying U.K. startup for $1 billion")

    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)

        match = {
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char,
        }

        entities.append(match)
    return entities

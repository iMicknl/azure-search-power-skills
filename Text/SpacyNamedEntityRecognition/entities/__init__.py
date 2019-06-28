import azure.functions as func
import spacy
import json

from spacy import displacy
from spacy.lang.nl.examples import sentences

# Cache all Spacy models in memory
# https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python?view=aspnetcore-2.2#global-variables
SPACY_EN = None
SPACY_NL = None

supported_languages = {
    'en': 'en_core_web_sm',
    'nl': 'nl_core_news_sm',
}

def main(req: func.HttpRequest) -> func.HttpResponse:

    # Load settings
    default_language = list(supported_languages)[0]

    text = get_parameter(req, 'text')
    categories = get_parameter(req, 'categories', [])
    language = get_parameter(req, 'languageCode', default_language)

    # Check if language is supported
    if language not in supported_languages:
        return

    # Load Spacy Model if not in memory
    model_name = ('spacy_' + language).upper()
    model = globals()[model_name]

    if model is None:
        globals()[model_name] = spacy.load(supported_languages[language])

    doc = extract_from_text(text, model_name)

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


def get_parameter(req: func.HttpRequest, param: str, default: object = None):

    value = req.params.get(param)

    if not value:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            value = req_body.get(param)
    
    if not value:
        value = default

    return value

def extract_from_text(text: str, model_name: str):
    """Extract Spacy Named Entities from raw text"""
    nlp = globals()[model_name]
    entities = []

    doc = nlp(text)

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

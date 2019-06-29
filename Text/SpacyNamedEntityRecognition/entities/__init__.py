import azure.functions as func
import spacy
import json
import logging

from spacy import displacy
from spacy.lang.nl.examples import sentences
from .models import *

# Cache all Spacy models in memory
# https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python?view=aspnetcore-2.2#global-variables

# Multi-language Supports identification of PER, LOC, ORG and MISC entities for English, German, 
# Spanish, French, Italian, Portuguese and Russian.
SPACY_XX = None
SPACY_EN = None
SPACY_NL = None
SPACY_DE = None
SPACY_FR = None
SPACY_ES = None
SPACY_PT = None
SPACY_IT = None

SUPPORTED_LANGUAGES = {
    'xx': 'xx_ent_wiki_sm',
    'en': 'en_core_web_sm',
    'nl': 'nl_core_news_sm',
    'de': 'de_core_news_sm',
    'fr' : 'fr_core_news_sm',
    'es' : 'es_core_news_sm',
    'pt' : 'pt_core_news_sm',
    'it' : 'it_core_news_sm',
    'el' : 'el_core_news_sm'
}


SPACY_NER_LABELS = {
    'PERSON': 'People, including fictional.',
    'NORP': 'Nationalities or religious or political groups.',
    'FAC': 'Buildings, airports, highways, bridges, etc.',
    'ORG': 'Companies, agencies, institutions, etc.',
    'GPE': 'Countries, cities, states.',
    'LOC': 'Non-GPE locations, mountain ranges, bodies of water.',
    'PRODUCT': 'Objects, vehicles, foods, etc. (Not services.)',
    'EVENT': 'Named hurricanes, battles, wars, sports events, etc.',
    'WORK_OF_ART': 'Titles of books, songs, etc.',
    'LAW': 'Named documents made into laws.',
    'LANGUAGE': 'Any named language.',
    'DATE': 'Absolute or relative dates or periods.',
    'TIME': 'Times smaller than a day.',
    'PERCENT': 'Percentage, including "%".',
    'MONEY': 'Monetary values, including unit.',
    'QUANTITY': 'Measurements, as of weight or distance.',
    'ORDINAL': '"first", "second", etc.',
    'CARDINAL': 'Numerals that do not fall under another type.',
}

# Dutch is using PER instead of Person, MISC 
SPACY_NER_MAPPING = {
    'PER' : 'PERSON'
}

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Endpoint used by Azure Search"""

    # Load Skill parameters
    default_language = get_parameter(
        req, 'defaultLanguageCode', list(SUPPORTED_LANGUAGES)[0])
    categories = get_parameter(req, 'categories', [])

    # Validate request body
    try:
        body = RecordsRequest(**req.get_json())
    except ValueError:
        return func.HttpResponse("Please pass a valid request body", status_code=400)

    # Return results
    if body:
        logging.info(f"Extracting entities from {len(body.values)} record(s).")
        result = extract_from_records(body.values)

        return func.HttpResponse(
            result.json(),
            headers={
                "Content-Type": "application/json",
            }
        )


def get_parameter(req: func.HttpRequest, param: str, default: object = None):
    """Retrieve parameters from GET or POST request"""

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


def extract_from_record(
    record: RecordRequest
):
    """Extract Skills from a single RecordRequest"""

    res = {
        "recordId": record.recordId,
        "data": {"entities": []},
        "warnings": None,
        "errors": None,
    }
    if len(record.data.text) == 0:
        res['warnings'] = [{"message": "Record text is empty."}]
    else:
        try:
            default_language = list(SUPPORTED_LANGUAGES)[0]
            language = record.data.languageCode

            if not language:
                language = default_language

            # Check if language is supported
            if language not in SUPPORTED_LANGUAGES:
                raise ValueError('Language "' + language + '" not supported')

            data = extract_from_text(record.data.text, language)
            if data:
                res['data']['entities'] = data
            else:
                res['warnings'] = [{"message": "No entities found."}]
        except ValueError as e:
            res['errors'] = [
                {"message": f"There was an error parsing this record. Error: {e}"}]

    return res


def extract_from_records(
    records: RecordsRequest
) -> RecordsResponse:
    """Logic to extract skills from each record."""
    # TODO MAKE ASYNC

    results = []
    for record in records:
        result = extract_from_record(record)
        results.append(result)

    logging.warning(result)

    values_res = {"values": results}

    return RecordsResponse(**values_res)

def extract_from_text(text: str, language: str):
    """Extract Spacy Named Entities from raw text"""

    # Load Spacy Model if not in memory
    model_name = ('spacy_' + language).upper()
    model = globals()[model_name]

    if model is None:
        model = globals()[model_name] = spacy.load(
            SUPPORTED_LANGUAGES[language])

    entities = []
    result = model(text)

    for ent in result.ents:
        match = {
            "text": ent.text,
            "type_": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char,
        }

        entities.append(match)
    return entities

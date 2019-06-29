# SpacyNamedEntityRecognition Function

>spaCy features an extremely fast statistical entity recognition system, that assigns labels to contiguous spans of tokens. The default model identifies a variety of named and numeric entities, including companies, locations, organizations and products. You can add arbitrary classes to the entity recognition system, and update the model with new examples.

This custom skill utilizes Spacy entity recognition system. It has been modelled against the built-in [Entity Recognition cognitive skill
](https://docs.microsoft.com/en-us/azure/search/cognitive-search-skill-entity-recognition).

[![Deploy to Azure](https://azuredeploy.net/deploybutton.svg)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure-Samples%2Fazure-search-power-skills%2Fmaster%2FText%2FSpacyNamedEntityRecognition%2Fazuredeploy.json)

## Requirements
(TODO: Python Azure function)
python -m spacy download en_core_web_sm
python -m spacy download nl_core_news_sm
how tu use on Serverless?

# SpacyNamedEntityRecognition Skill

## @odata.type  
Microsoft.CustomSkills.Text.SpacyNamedEntityRecognitionSkill

## Data limits
The maximum size of a record should be 50,000 characters as measured by `String.Length`. If you need to break up your data before sending it to the key phrase extractor, consider using the [Text Split skill](https://docs.microsoft.com/en-us/azure/search/cognitive-search-skill-textsplit).

## Skill parameters

Parameters are case-sensitive and are all optional.

| Parameter name	 | Description |
|--------------------|-------------|
| categories	| Array of categories that should be extracted.  Possible category types: `"Person"`, `"Location"`, `"Organization"`, `"Quantity"`, `"Datetime"`, `"URL"`, `"Email"`. If no category is provided, all types are returned.|
|defaultLanguageCode |	Language code of the input text. The following languages are supported: `en, nl, xx (multi-language)`|
|minimumPrecision | Unused. Reserved for future use. |
|includeTypelessEntities | When set to true if the text contains a well known entity, but cannot be categorized into one of the supported categories, it will be returned as part of the `"entities"` complex output field. 
These are entities that are well known but not classified as part of the current supported "categories". For instance "Windows 10" is a well known entity (a product), but "Products" are not in the categories supported today. Default is `false` |


## Skill inputs

| Input name	  | Description                   |
|---------------|-------------------------------|
| languageCode	| Optional. Default is `"xx"` (multi-language).  |
| text          | The text to analyze.          |

## Skill outputs
> Not all entity categories are supported for all [languages supported by Spacy](https://spacy.io/usage/models).

| Output name	  | Description                   |
|---------------|-------------------------------|
| entities | An array of complex types that contains rich information about the entities extracted from text, with the following fields <ul><li> name (the actual entity name. This represents a "normalized" form)</li><li>type (the category of the entity recognized)</li><li> matches (a complex collection that contains)<ul><li>text (the raw text for the entity)</li><li>offset (the location where it was found)</li><li>length (the length of the raw entity text)</li></ul></li></ul> |

##	Sample definition

```json
  {
    "@odata.type": "#Microsoft.CustomSkills.Text.SpacyNamedEntityRecognitionSkill",
    "description": "Spacy Entity Recognition",
     "uri": "https://[hostname].azurewebsites.net/api/entities?code=API_KEY",
    "categories": [ "Person", "Email"],
    "defaultLanguageCode": "en",
    "inputs": [
      {
        "name": "text",
        "source": "/document/content"
      }
    ],
    "outputs": [
      {
        "name": "persons",
        "targetName": "people"
      },
      {
        "name": "emails",
        "targetName": "contact"
      },
      {
        "name": "entities"
      }
    ]
  }
```
##	Sample input

```json
{
    "values": [
      {
        "recordId": "1",
        "data":
           {
             "text": "Microsoft Corporation is an American multinational technology company with headquarters in Redmond, Washington. Microsoft was founded by Bill Gates and Paul Allen on April 4, 1975, to develop and sell BASIC interpreters for the Altair 8800.",
             "languageCode": "en"
           }
      },
           {
        "recordId": "2",
        "data":
           {
             "text": "Microsoft Corporation (vaak afgekort als MS) is een Amerikaans bedrijf uit Redmond in Washington. Microsoft ontwikkelt, verspreidt, licentieert en ondersteunt een breed scala aan computergerelateerde producten. Het bedrijf werd opgericht door Bill Gates en Paul Allen op 4 april 1975.",
             "languageCode": "nl"
           }
      },
      {
        "recordId": "3",
        "data":
           {
             "text": "How are expections handled for unsupported languages?",
             "languageCode": "be"
           }
      }
    ]
}
```

##	Sample output

```json
{
    "values": [
        {
            "recordId": "1",
            "data": {
                "entities": [
                    {
                        "text": "Microsoft Corporation",
                        "type_": "ORG",
                        "start": 0,
                        "end": 21
                    },
                    {
                        "text": "American",
                        "type_": "NORP",
                        "start": 28,
                        "end": 36
                    },
                    {
                        "text": "Redmond",
                        "type_": "GPE",
                        "start": 91,
                        "end": 98
                    },
                    {
                        "text": "Washington",
                        "type_": "GPE",
                        "start": 100,
                        "end": 110
                    },
                    {
                        "text": "Microsoft",
                        "type_": "ORG",
                        "start": 112,
                        "end": 121
                    },
                    {
                        "text": "Bill Gates",
                        "type_": "PERSON",
                        "start": 137,
                        "end": 147
                    },
                    {
                        "text": "Paul Allen",
                        "type_": "PERSON",
                        "start": 152,
                        "end": 162
                    },
                    {
                        "text": "April 4, 1975",
                        "type_": "DATE",
                        "start": 166,
                        "end": 179
                    },
                    {
                        "text": "BASIC",
                        "type_": "ORG",
                        "start": 201,
                        "end": 206
                    },
                    {
                        "text": "Altair",
                        "type_": "PERSON",
                        "start": 228,
                        "end": 234
                    },
                    {
                        "text": "8800",
                        "type_": "CARDINAL",
                        "start": 235,
                        "end": 239
                    }
                ]
            },
            "errors": null,
            "warnings": null
        },
        {
            "recordId": "2",
            "data": {
                "entities": [
                    {
                        "text": "Microsoft Corporation",
                        "type_": "ORG",
                        "start": 0,
                        "end": 21
                    },
                    {
                        "text": "MS",
                        "type_": "ORG",
                        "start": 41,
                        "end": 43
                    },
                    {
                        "text": "Amerikaans",
                        "type_": "LOC",
                        "start": 52,
                        "end": 62
                    },
                    {
                        "text": "Redmond",
                        "type_": "LOC",
                        "start": 75,
                        "end": 82
                    },
                    {
                        "text": "Washington",
                        "type_": "LOC",
                        "start": 86,
                        "end": 96
                    },
                    {
                        "text": "Microsoft",
                        "type_": "ORG",
                        "start": 98,
                        "end": 107
                    },
                    {
                        "text": "Bill Gates",
                        "type_": "PER",
                        "start": 243,
                        "end": 253
                    },
                    {
                        "text": "Paul Allen",
                        "type_": "PER",
                        "start": 257,
                        "end": 267
                    }
                ]
            },
            "errors": null,
            "warnings": null
        },
        {
            "recordId": "3",
            "data": {
                "entities": []
            },
            "errors": [
                {
                    "message": "There was an error parsing this record. Error: Language \"be\" not supported"
                }
            ],
            "warnings": null
        }
    ]
}
```

## Error cases
If the language code for the document is unsupported, an error is returned and no entities are extracted.
import json
import requests
from flask_babel import _
from app import config


def translate(text, source_language, dest_language):
    if not config.msTranslatorKey:
        return _('Error: the translation service is not configured.')
    headers = {'Ocp-Apim-Subscription-Key': config.msTranslatorKey,
               'Ocp-Apim-Subscription-Region': 'canadacentral',
               'Content-type': 'application/json'}
    url = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from={}&to={}' \
        .format(source_language, dest_language)
    body = [{'text': text}]
    request = requests.post(url, headers=headers, json=body)
    if request.status_code != 200:
        return _('Error: the translation service failed.')
    return json.loads(request.content.decode('utf-8-sig'))[0]['translations'][0]['text']

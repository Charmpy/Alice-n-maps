import os
from flask import Flask, request
import logging
import json
# from deep_translator import GoogleTranslator


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info(f'Response: {response!r}')
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = '(12) Привет! Назови свое имя!'
        sessionStorage[user_id] = {
            'first_name': None
        }
        return

    if sessionStorage[user_id]['first_name'] is None:
        first_name = get_first_name(req)
        if first_name is None:
            res['response']['text'] = \
                'Не расслышала имя. Повтори, пожалуйста!'
        else:
            sessionStorage[user_id]['first_name'] = first_name
            res['response'][
                'text'] = 'Приятно познакомиться, ' \
                          + first_name.title() \
                          + '. Я - Алиса. Могу переводить на английский'

    else:
        if 'Переведи слово'.lower() in req["request"]['command'].lower():
            translation = req["request"]['command'].lower()[15:]
            result = translation
            # result = GoogleTranslator(source='auto',
            #                               target='en').translate(translation)
            res['response']['text'] = result

        else:
            res['response']['text'] = \
                'Неверно. ' + sessionStorage[user_id]['first_name'].title() + ', Попробуй еще разок!'
            # ищем город в сообщение от пользователя


def get_first_name(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            return entity['value'].get('first_name', None)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


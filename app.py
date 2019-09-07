import os
import hashlib
import json
import requests
from settings import load_dotenv
from caesar_cipher import CaesarCipher

load_dotenv()

TOKEN = os.getenv('TOKEN')
API_URL_REQUEST = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data'
API_URL_RESPONSE = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={}'

LETTERS = list(chr(i) for i in range(97, 123))


def decode(message: dict):
    print('decoding message')
    if message:
        shift = int(message.get('numero_casas'))
        ciphertext = str(message.get('cifrado')).lower()

        plaintext = CaesarCipher.decrypt(ciphertext, shift)
        message['decifrado'] = plaintext

        encrypttext = hashlib.sha1(plaintext.encode('utf-8')).hexdigest()
        message['resumo_criptografico'] = encrypttext
        print('decoded message')
        return message
    raise TypeError('decode() argument must be a \'dict\', and cannot be \'None\'')


def save_json(text):
    print('saving .json file...')
    if text:
        with open('answer.json', 'w') as file:
            json.dump(text, file)
        print('saved')
        return
    raise TypeError('decode() argument must be a \'dict\', and cannot be \'None\'')


def get_json_from_api(url, token):
    print('requesting .json file...')
    try:
        req = requests.get(url, {'token': token})
        save_json(req.json())
    except Exception as e:
        print('Exception:', e)


def post_json_to_api(token):
    print('sending .json file...')
    files = {
        'answer': ('answer', open('answer.json', 'rb'))
    }
    try:
        res = requests.post(API_URL_RESPONSE.format(token), files=files)
        print('sended')
        print(res.text)
    except Exception as e:
        print('Exception:', e)


def main():
    get_json_from_api(API_URL_REQUEST, TOKEN)

    with open('answer.json', 'r') as file:
        message = json.load(file)

    updated_message = decode(message)
    save_json(updated_message)

    post_json_to_api(TOKEN)


if __name__ == '__main__':
    main()

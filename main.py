import requests
import configparser
from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.read('config.ini')

URL = 'https://serviceportal.hamburg.de/HamburgGateway/FVP/FV/bezirke/passda/'
STATE_FILE = 'state.json'

def prepare_request(type: str, serial: str, birthdate: str):
    response = requests.get(URL)

    cookies = response.cookies
    soup = BeautifulSoup(response.text, 'html.parser')

    data = {
        '__VIEWSTATE': soup.find('input', {'id': '__VIEWSTATE'}).get('value'),
        '__VIEWSTATEGENERATOR': soup.find('input', {'id': '__VIEWSTATEGENERATOR'}).get('value'),
        '__EVENTVALIDATION': soup.find('input', {'id': '__EVENTVALIDATION'}).get('value'),
        'GatewayMaster:ContentSection:wuc_01_Query:rblAusweisArt': type,
        'GatewayMaster:ContentSection:wuc_01_Query:txtSeriennummer': serial,
        'GatewayMaster:ContentSection:wuc_01_Query:txtGebDat': birthdate,
        'GatewayMaster:ContentSection:wuc_01_Query:btnWeiter': 'Antragsstatus ermitteln',
    }

    return cookies, data

def make_request(cookies, data):
    response = requests.post(URL, cookies=cookies, data=data)

    soup = BeautifulSoup(response.text, 'html.parser')

    status = soup.find('span', {'id': 'GatewayMaster_ContentSection_wuc_02_Response_lblStatus2'}).decode_contents()

    return status

def read_state():
    try:
        state_file = open('state.txt', 'r')
        return state_file.read()
    except FileNotFoundError:
        return None
    
def write_state(state: str):
    state_file = open('state.txt', 'w+')
    state_file.write(state)

def send_to_telegram(text):
    bot_token = config['telegram']['bot_token']
    chat_id = config['telegram']['chat_id']
    params = {
        'chat_id': chat_id,
        'text': text
    }
    foo = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', params=params)


def main():
    cookies, data = prepare_request(
        type=config['Serviceportal']['type'],
        serial=config['Serviceportal']['serial'],
        birthdate=config['Serviceportal']['birthdate'],
    )
    status = make_request(cookies, data)

    state = read_state()
    if (status != state):
        text = f"New status: {status} (Serial: {config['Serviceportal']['serial']})"
        print(text)
        send_to_telegram(text)
    write_state(status)


if __name__ == '__main__':
    main()

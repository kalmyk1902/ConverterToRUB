import requests
import re
from datetime import datetime
from time import sleep
from lxml import html

def getCurrencies(currencyCollection, nameCollection, mnCollection):
    try:
        r = requests.get('https://www.cbr.ru/currency_base/daily/')
        tree = html.fromstring(r.content)
        currencyCollection.extend(tree.xpath('//tr/td[5]/text()'))
        nameCollection.extend(tree.xpath('//tr/td[2]/text()'))
        mnCollection.extend(tree.xpath('//tr/td[3]/text()'))
    except requests.exceptions.ConnectionError:
        print('Проверьте подключение к Интернету')
        sleep(5)
        exit(2)

now = datetime.now()
today = now.strftime('%d.%m.%Y')

print(f'Курсы ЦБ РФ на {today}')
sleep(1)

mask = re.compile('[A-Z]{3}')
is_correct_input = False
ch = 'empty'

while (not is_correct_input) and (ch != ''):
    ch = input('Введите валюту в формате USD, EUR: ')
    is_correct_input = mask.fullmatch(ch)
    if (not is_correct_input) and (ch != ''):
        print('Некорректный ввод!', end='\n\n')

    if ch == '':
        ch = 'USD'
        print('Присвоено USD по умолчанию.')
        sleep(1)
        break

while True:
    try:
        amount = int(input('Введите сумму для перевода в рубли: '))
        print()
        break
    except ValueError:
        print('Цифрами введите', end='\n')

currencies = []
names = []
mn = []
getCurrencies(currencies, names, mn)

try:
    x = names.index(ch)
except ValueError:
    print(f'Не найдено валюты {ch}')
    sleep(3)
    exit(1)

y = currencies[x]
y = y.replace(',', '.')
final = 0.0

if mn[x] == 1:
    final = float(y) * amount
else:
    final = (float(y) / int(mn[x]) * amount)

print(f'Перевод успешный! {amount} {ch} = {"{:.3f}".format(final)} рублей')
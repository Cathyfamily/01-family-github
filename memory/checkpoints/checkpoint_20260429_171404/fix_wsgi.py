import requests
USERNAME = 'Cathyfamily'
TOKEN = '1f990874775a217546087f86f661c02f637d0c02'
DOMAIN = 'cathyfamily.pythonanywhere.com'

wsgi = '''import sys

path = '/home/Cathyfamily/family'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
'''

res = requests.post(
    f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path/var/www/cathyfamily_pythonanywhere_com_wsgi.py',
    files={'content': wsgi},
    headers={'Authorization': f'Token {TOKEN}'}
)
print('WSGI Update:', res.status_code, res.content)

res = requests.post(
    f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/webapps/{DOMAIN}/reload/',
    headers={'Authorization': f'Token {TOKEN}'}
)
print('Reload:', res.status_code, res.content)

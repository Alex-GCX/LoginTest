import requests
from bs4 import BeautifulSoup

base_url = 'https://github.com/login'
login_url = 'https://github.com/session'


def get_github_html(url):
    response = requests.get(url)
    first_cookies = response.cookies.get_dict()
    return response.text, first_cookies


def get_token(html):
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find('input', attrs={'name': 'authenticity_token'})
    token = res['value']
    return token


def get_login_cookies(url, token, cookies):
    data = {'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': token,
            'login': 'gongchengxue',
            'password': '962464huang612',
            'webauthn-support': 'supported'}
    response = requests.post(url, data=data, cookies=cookies)
    print(response.status_code)
    cookies = response.cookies.get_dict()
    return cookies


if __name__ == '__main__':
    html, cookies = get_github_html(base_url)
    token = get_token(html)
    login_cookies = get_login_cookies(login_url, token, cookies)
    print(login_cookies)
    response = requests.get('https://github.com/settings/repositories',cookies=login_cookies)
    print(response.status_code,response.reason)
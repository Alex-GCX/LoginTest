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
    response = requests.post(url, data=data, cookies=cookies)#222 #333
    print(response.status_code, response.reason)
    cookies = response.cookies.get_dict()
    return cookies

if __name__ == '__main__':
    html, cookies = get_github_html(base_url)
    token = get_token(html)
    login_cookies = get_login_cookies(login_url, token, cookies)
    print(login_cookies)
    response = requests.get('https://github.com/settings/repositories', cookies=login_cookies)#1111
    print(response.status_code, response.reason)
'''
1.最终程序能够访问到 'https://github.com/settings/repositories' ,重点就是如何得到请求中的 login_cookies
2.如何拿到 login_cookies,就是通过模拟登陆,再拿到登录后response中的cookies
3.如何模拟登陆,就是先手动登录,然后通过看登录form表单中通过POST请求的登录Form Data(重点是其中的 authenticity_token),
  拿到data,cookies就是登录之前登录页面的response的cookies
'''

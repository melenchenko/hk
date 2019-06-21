import requests
import os
import wget


def save_url(url, path_to_save='uploads/tmp/'):
    # url = 'https://api.github.com/some/endpoint'
    # payload = {'some': 'data'}
    # r = requests.post(url, json=payload)
    filename = wget.download(url)
    full_path = u'' + os.getcwd() + '/' + path_to_save + filename
    if os.path.exists(full_path):
        os.remove(full_path)
    os.rename(filename, full_path)
    # (dirname, filename) = os.path.split(url)
    # f = open(path_to_save + filename, 'wb')
    # f.write(content)
    # f.close()

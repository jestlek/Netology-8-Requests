import requests
import json
from pprint import pprint


def download_file_with_superheroes():
    """This function creates json file in project with information about all heroes"""
    with open('superheroes.json', 'w') as f:
        url = 'https://akabab.github.io/superhero-api/api/all.json'
        resp = requests.get(url)
        json.dump(resp.json(), f, ensure_ascii=False, indent=2)


def search_most_clever_hero(heroes_list):
    """This function prints hero from heroes_list by most quantity of intelligence"""
    with open('superheroes.json', encoding='utf-8') as f:
        data = json.load(f)
        my_heroes_dict = {}
        for hero in data:
            if hero['name'] in heroes_list:
                my_heroes_dict[hero['name']] = hero['powerstats']['intelligence']
        most_clever_hero = max(my_heroes_dict.items(), key=lambda x: x[1])
        print(f'Самый умный супергерой {most_clever_hero[0]}, его показатель интеллекта равен {most_clever_hero[1]}!')


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def _upload_link(self, file_path: str):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': file_path, 'owerwrite': 'true'}
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def upload(self, file_path, filename):
        link_dict = self._upload_link(file_path)
        href = link_dict['href']
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print('Success')


def questions_with_tag_python():
    '''This function gets all questions from stackoverflow by last 2 days with tagged "Python"'''
    url = 'https://api.stackexchange.com/2.3/questions?fromdate=1663632000&todate=1663804800&order=desc&sort=activity&tagged=Python&site=stackoverflow'
    resp = requests.get(url)
    resp.raise_for_status()
    result = resp.json()
    pprint(result)


if __name__ == '__main__':
    download_file_with_superheroes()
    search_most_clever_hero(['Hulk', 'Captain America', 'Thanos'])
    path_to_file = 'superheroes.json'
    file_name = 'superheroes.json'
    token = '123'
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file, file_name)
    questions_with_tag_python()

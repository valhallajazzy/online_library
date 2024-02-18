import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError("Произошел redirect")


def create_path_to_file(number, folder='books/'):
    os.makedirs(f'{folder}', exist_ok=True)
    url = f'https://tululu.org/b{number}'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    author_and_title = soup.find('title').text.split('-')
    title = author_and_title[1].split(',')[0].strip()
    title = sanitize_filename(title)
    title_with_id = f"{number}. {title}.txt"
    path = os.path.join(folder, title_with_id)
    return path


def download_books():
    for number in range(1, 11):
        url = f'https://tululu.org/txt.php?id={number}'
        response = requests.get(url)
        response.raise_for_status()
        try:
            check_for_redirect(response)
            filepath = create_path_to_file(number, folder='books/')
            with open(f"{filepath}", 'w') as file:
                file.write(response.text)
        except requests.HTTPError:
            continue


if __name__ == '__main__':
    download_books()
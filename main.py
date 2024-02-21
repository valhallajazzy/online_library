import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit, unquote


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


def download_txt():
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


def download_picture(folder='pictures'):
    for number in range(1, 11):
        os.makedirs(f'{folder}', exist_ok=True)
        url = f'https://tululu.org/b{number}'
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            url = urlsplit(url)
            path = unquote(soup.find('table', class_='d_book').find('img')['src'])
            pic_extension = path.split('.')[1]
            base_url = url.scheme + '://' + url.netloc
            picture_link = urljoin(base_url, path)
            img_response = requests.get(picture_link)
            img_response.raise_for_status()
            with open(f"{folder}/{number}.{pic_extension}", 'wb') as file:
                file.write(img_response.content)
        except AttributeError:
            continue


def download_comments(folder='comments'):
    for number in range(1, 11):
        os.makedirs(f'{folder}', exist_ok=True)
        url = f'https://tululu.org/b{number}'
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        divs_with_comments = soup.find_all('div', class_='texts')
        comments = ""
        for div in divs_with_comments:
            comment = div.find('span')
            if comment:
                comments += f"{comment.text} \n"
        if comments != "":
            with open(f"{folder}/{number}.txt", 'w') as file:
                file.write(comments)


if __name__ == '__main__':
    download_txt()
    download_picture()
    download_comments()
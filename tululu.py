import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, unquote
import argparse
import logging
from time import sleep


class RedirectException(Exception):
    pass


def check_for_redirect(response):
    if response.history:
        raise RedirectException("Произошел redirect")


def parse_book_page(soup):
    if soup.find('div', id='content') is not None:
        author_and_title = soup.find('div', id='content').find('h1').text.split(' \xa0 :: \xa0 ')
        title = sanitize_filename(author_and_title[0].strip())
        author = sanitize_filename(author_and_title[1].strip())
        links_with_genres = soup.find('span', class_='d_book').find_all('a')
        genres = [link.text for link in links_with_genres]
        img_path = unquote(soup.find('table', class_='d_book').find('img')['src'])
        divs_with_comments = soup.find_all('div', class_='texts')
        comments = []
        for div in divs_with_comments:
            comment = div.find('span')
            if comment:
                comments.append(comment.text)

        return {'title': title,
                'author': author,
                'genres': genres,
                'comments': comments,
                'img_path': img_path}


def create_path_to_file(book_id, title, folder='books/'):
    os.makedirs(f'{folder}', exist_ok=True)
    title_with_id = f"{book_id}. {title}.txt"
    path = os.path.join(folder, title_with_id)
    return path


def download_picture(book_id, soup, folder='pictures'):
    os.makedirs(f'{folder}', exist_ok=True)
    path = parse_book_page(soup)['img_path']
    pic_extension = path.split('.')[1]
    base_url = f'https://tululu.org/b{book_id}'
    picture_link = urljoin(base_url, path)
    img_response = requests.get(picture_link)
    img_response.raise_for_status()
    with open(f"{folder}/{book_id}.{pic_extension}", 'wb') as file:
        file.write(img_response.content)


def download_book(book_id):
    url_text = f'https://tululu.org/txt.php'
    params = {'id': book_id}
    text_response = requests.get(url_text, params=params)
    text_response.raise_for_status()
    check_for_redirect(text_response)
    url_book_page = f'https://tululu.org/b{book_id}'
    book_page_response = requests.get(url_book_page)
    book_page_response.raise_for_status()
    soup = BeautifulSoup(book_page_response.text, 'lxml')
    about_book = parse_book_page(soup)
    filepath = create_path_to_file(book_id, about_book['title'], folder='books/')
    with open(f"{filepath}", 'w') as file:
        file.write(text_response.text)
    download_picture(book_id, soup)
    print(f"Название: {about_book['title']} \nАвтор: {about_book['author']} \n")



def download_books_in_range(start_id, end_id):
    for book_id in range(start_id, end_id + 1):
        try:
            download_book(book_id)
        except requests.ConnectionError:
            logging.error('Ошибка интернет-соединения, переподключаюсь')
            sleep(5)
        except requests.HTTPError:
            logging.error(f'Ошибка http-подключения к серверу с id книги - {book_id}, переподключаюсь')
            sleep(5)
        except RedirectException:
            logging.warning(f'На странице с ожидаемым id книги - {book_id}, '
                            f'обложки не сущетсвует. Картинка не скачана.')
            continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Данная программа скачивает книги с сайта https://tululu.org/ в указанном диапазоне id'
    )
    parser.add_argument('-s', '--start_id', help='id книги с которой начнется скачивание',
                        default=1, type=int)
    parser.add_argument('-e', '--end_id', help='id книги на которой окончится скачивание',
                        default=10, type=int)
    args = parser.parse_args()
    download_books_in_range(args.start_id, args.end_id)

import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit, unquote
import argparse


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError("Произошел redirect")


def parse_book_page(soup):
    try:
        author_and_title = soup.find('div', id='content').find('h1').text.split(' \xa0 :: \xa0 ')
        title = sanitize_filename(author_and_title[0].strip())
        author = sanitize_filename(author_and_title[1].strip())
        genres = []
        links_with_genres = soup.find('span', class_='d_book').find_all('a')
        for link in links_with_genres:
            genres.append(link.text)
        divs_with_comments = soup.find_all('div', class_='texts')
        comments = []
        for div in divs_with_comments:
            comment = div.find('span')
            if comment:
                comments.append(comment.text)
        return {
                'title': title,
                'author': author,
                'genres': genres,
                'comments': comments
                }
    except AttributeError:
        return None


def get_page(book_id):
    url = f'https://tululu.org/b{book_id}'
    response = requests.get(url)
    response.raise_for_status()
    return response


def create_path_to_file(book_id, title, folder='books/'):
    os.makedirs(f'{folder}', exist_ok=True)
    title_with_id = f"{book_id}. {title}.txt"
    path = os.path.join(folder, title_with_id)
    return path


def download_picture(book_id, soup, folder='pictures'):
    os.makedirs(f'{folder}', exist_ok=True)
    url = urlsplit(f'https://tululu.org/b{book_id}')
    path = unquote(soup.find('table', class_='d_book').find('img')['src'])
    pic_extension = path.split('.')[1]
    base_url = url.scheme + '://' + url.netloc
    picture_link = urljoin(base_url, path)
    img_response = requests.get(picture_link)
    img_response.raise_for_status()
    with open(f"{folder}/{book_id}.{pic_extension}", 'wb') as file:
        file.write(img_response.content)


def download_books(start_id, end_id):
    for book_id in range(start_id, end_id + 1):
        url = f'https://tululu.org/txt.php?id={book_id}'
        response = requests.get(url)
        response.raise_for_status()
        try:
            check_for_redirect(response)
            book_page_response = get_page(book_id)
            soup = BeautifulSoup(book_page_response.text, 'lxml')
            book_info = parse_book_page(soup)
            filepath = create_path_to_file(book_id, book_info['title'], folder='books/')
            with open(f"{filepath}", 'w') as file:
                file.write(response.text)
            download_picture(book_id, soup)
            print(f"Название: {book_info['title']} \nАвтор: {book_info['author']} \n")

        except requests.HTTPError:
            continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Данная программа скачивает книги с сайта https://tululu.org/ в указанном диапазоне id'
    )
    parser.add_argument('start_id', help='id книги с которой начнется скачивание', type=int)
    parser.add_argument('end_id', help='id книги на которой окончится скачивание', type=int)
    args = parser.parse_args()
    download_books(args.start_id, args.end_id)

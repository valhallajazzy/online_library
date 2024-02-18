import requests
import os


os.makedirs('books', exist_ok=True)
for numbers in range(1, 10):
    url = f'https://tululu.org/txt.php?id={numbers}'
    response = requests.get(url)
    response.raise_for_status()
    with open(f"books/id{numbers}.txt", 'w') as file:
        file.write(response.text)
    # print(response.text)
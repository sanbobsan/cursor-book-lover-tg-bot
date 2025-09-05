
import json
from random import randint


def find_book_by_title(title: str, mode=0):
    """Возвращает найденную книгу
    mode = 0 -- нестрогий; mode = 1 -- строгий"""
    with open('books.json',encoding='utf-8') as file:
        data = json.load(file)
        title = title.lower()
        'нестрогий поиск'
        if not mode:
            for i in range(len(data)):
                if  title in data[i]['title'].lower().strip(" ,./?|!@#$%^&*()';:"):
                    return data[i]
        'строгий поиск'
        if mode:
            for i in range(len(data)):
                if  title == data[i]['title'].lower():
                    return data[i]
        return None


def find_books_by_genre(genre):
    "Возвращает список книг в зависимости от жанра"
    with open('books.json',encoding='utf-8') as file:
        data = json.load(file)
        books = []
        for i in range(len(data)):
            if genre.lower() in data[i]['genre'].lower():
                books.append(data[i])
        return books


def get_top_of_books() -> list:
    "Возвращает список с лучшими книгами"
    with open('books.json',encoding='utf-8') as file:
        data = json.load(file)
        rate = []
        name = []
        for i in range(len(data)):
            rate.append(data[i]['mark'])
            name.append(data[i]['title'])
        dictionary = dict(zip(rate,name))
        rating_pass = []
        rating = []
        for i in range(20):
            rating_pass.append(dictionary[sorted(dictionary,reverse=True)[i]])
        for i in range(len(rating_pass)):
            rating.append(find_book_by_title(rating_pass[i],1))
        return rating


def get_random_book() -> dict:
    "Возвращает случайную книгу"
    i = randint(0,81)
    with open('books.json',encoding='utf-8') as file:
        data = json.load(file)
        return data[i]


def get_all_genres():
    "Возвращает список со всеми возможными жанрами"
    with open("genres.json", "r", encoding="utf-8") as f:
        return json.load(f)


def add_book_rating(title: str, rating: int):
    """
    Добавляет оценку книге и обновляет агрегаты в JSON.
    Возвращает обновленный объект книги или None, если книга не найдена
    """
    with open('books.json', encoding='utf-8') as file:
        data = json.load(file)

    normalized_title = title.strip().lower()
    updated = None

    for book in data:
        if book.get('title', '').strip().lower() == normalized_title:
            marks = book.get('marks')
            marks[rating - 1] = int(marks[rating - 1]) + 1
            book['marks'] = marks

            number_of_marks = int(book.get('number_of_marks')) + 1
            sum_of_marks = int(book.get('sum_of_marks')) + rating
            book['number_of_marks'] = number_of_marks
            book['sum_of_marks'] = sum_of_marks
            book['mark'] = sum_of_marks / number_of_marks

            updated = book
            break

    with open('books.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    return updated
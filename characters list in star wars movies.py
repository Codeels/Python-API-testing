from pprint import pprint
import requests

print('------------Начало работы------------')
base_url = 'https://swapi.dev/api/'
get_darth_vader = 'people/4/'

# отправка запроса на получение информации о Дарт Вейдере
result_get_people = requests.get(base_url+get_darth_vader)
result_darth_vader = result_get_people.json()
print('------------Запрос персонажа ДВ------------')
print('------------Результат запроса персонажа------------\n')
pprint(result_darth_vader, indent=4)

# получаем список фильмов, в которых был Дарт Вейдер
print('\n------------Получение списка фильмов с ДВ------------')
movies_list_darth_vader = (result_darth_vader.get('films'))

# получаем список персонажей из списка с фильмами
characters_list = []
print('------------Получение ссылок на персонажей из фильмов с ДВ------------')
for movie in movies_list_darth_vader:
    result = requests.get(movie)
    character = result.json().get('characters')
    characters_list.extend(character)

# перевод списка с ссылками на персонажей в множество и наоборот, чтобы убрать лишних персонажей
characters_set = set(characters_list)
characters_list = list(characters_set)

# получаем имена из списка с ссылками на персонажей
names = []
print('------------Получение имен персонажей из фильмов с ДВ------------')
for character in characters_list:
    result = requests.get(character)
    names.append(result.json().get('name'))

# записываем имена в файл
print('------------Запись имен персонажей в файл "names.txt"------------')
for name in names:
    with open('names.txt', 'a', encoding='UTF-8') as file:
        file.write(f'{name}\n')
print('------------Завершение работы------------')



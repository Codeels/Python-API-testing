from pprint import pprint

import requests


class Test_new_location():

    def test_create_new_location(self):
        # создание новое локации

        base_url = 'https://rahulshettyacademy.com'
        key = '?key=qaclick123'  # параметр для всех запросов
        post_resource = '/maps/api/place/add/json'  # ресурс метода POST

        post_url = base_url + post_resource + key
        # print(post_url)

        json_for_create_new_location = {
            "location": {
                "lat": -38.383494,
                "lng": 33.427362
            }, "accuracy": 50,
            "name": "Frontline house",
            "phone_number": "(+91) 983 893 3937",
            "address": "29, side layout, cohen 09",
            "types": [
                "shoe park",
                "shop"
            ],
            "website": "http://google.com",
            "language": "French-IN"

        }

        result_post = requests.post(post_url, json=json_for_create_new_location)
        pprint(result_post.json(), indent=4)
        print(f'Статус код: {result_post.status_code}')
        assert result_post.status_code == 200, 'Запрос ошибочный'
        print('Запрос правильный')
        check_post = result_post.json()
        check_info_post = check_post.get('status')
        print(f'Статус код ответа: {check_info_post}')
        assert check_info_post == 'OK', 'Статус код ответа неверен'
        print('Статус код ответа верен')
        place_id = check_post.get('place_id')
        print(f'Place_id: {place_id}')
        print('Создание локации прошло успешно\n')

        # проверка созданной локации

        get_resource = '/maps/api/place/get/json'
        get_url = base_url + get_resource + key + '&place_id=' + place_id
        # print(get_url)
        result_get = requests.get(get_url)
        pprint(result_get.json(), indent=4)
        print(f'Статус код ответа: {result_get.status_code}')
        print('Проверка создания новой локации прошла успешно\n')

        # проверка изменения локации
        base_url = 'https://rahulshettyacademy.com'
        put_resource = '/maps/api/place/update/json'
        put_url = base_url + put_resource + key
        # print(put_url)

        json_for_update_new_location = {
            "place_id": f"{place_id}",
            "address": "100 Lenina street, RU",
            "key": "qaclick123"
        }

        result_put = requests.put(put_url, json=json_for_update_new_location)
        pprint(result_put.json(), indent=4)
        print(f'Статус код: {result_put.status_code}')
        assert result_put.status_code == 200, 'Запрос ошибочный'
        print('Запрос правильный')
        check_put = result_put.json()
        check_put_info = check_put.get('msg')
        print(f'Сообщение: {check_put_info}')
        assert check_put_info == 'Address successfully updated', 'wrong'
        print('Сообщение верно')
        print('Изменение данных локации прошло успешно\n')

        # проверка изменений в локации после обновления данных
        get_url = base_url + get_resource + key + '&place_id=' + place_id
        # print(get_url)
        result_get = requests.get(get_url)
        pprint(result_get.json(), indent=4)
        print(f'Статус код: {result_get.status_code}')
        assert result_get.status_code == 200, 'Статус код неверный'
        print('Статус код верный')
        assert result_get.json().get('address') == '100 Lenina street, RU', 'Адрес неверный'
        print('Адрес изменён верно')
        print('Проверка изменений в локации после изменения данных прошла успешно\n')

        # проверка удаления локации
        delete_resource = '/maps/api/place/delete/json'
        delete_url = base_url + delete_resource + key
        # print(delete_url)

        json_for_delete_location = {
            "place_id": f"{place_id}"
        }

        result_delete = requests.delete(delete_url, json=json_for_delete_location)
        print(result_delete.text)
        assert result_delete.status_code == 200, 'Статус код неверный'
        print(f'Статус код: {result_delete.status_code}')
        assert result_delete.json().get('status') == 'OK', 'Статус неверный'
        print(f'Статус в ответе: {result_delete.json().get("status")}')
        print('Удаление локации произведено успешно\n')

        # проверка правильности удаления локации
        get_url = base_url + get_resource + key + '&place_id=' + place_id
        # print(get_url)
        result_get = requests.get(get_url)
        pprint(result_get.json(), indent=4)
        print(f'Статус код: {result_get.status_code}')
        assert result_get.status_code == 404, 'Статус код неверный'
        print('Статус код верный')
        print('Проверка правильности удаления локации успешна\n')

        print('---------Тестирование завершено успешно---------')


if __name__ == "__main__":
    new_place = Test_new_location()
    new_place.test_create_new_location()

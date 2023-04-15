import time
import requests
import pytest
import allure

app_id = "637c795e029551b0a109d55b"
headers = {'app-id': app_id}
base_url = "https://dummyapi.io/data/v1/"

limit_list = [4, 5, 6, 25, 49, 50, 51]
pages_list = [-1, 0, 1, 500, 998, 999, 1000]
test_email = f"test{time.strftime('%H%M%S')}@mail.com"


class Check():
    @staticmethod
    def status_code(response: object, status_code: int):
        assert response.status_code == status_code, \
            f'Неверный статус код. Получен {response.status_code} вместо {status_code}\n'
        print(f'Статус код верный - {response.status_code}\n')

    @staticmethod
    def first_name(response: object, first_name: str):
        assert response.json().get('firstName') == first_name, f'Неверное имя: {response.json().get("firstName")}\n'
        print(f'Имя верное - {response.json().get("firstName")}\n')

    @staticmethod
    def last_name(response: object, last_name: str):
        assert response.json().get('lastName') == last_name, f'Неверная фамилия: {response.json().get("lastName")}\n'
        print(f'Фамилия верная - {response.json().get("lastName")}\n')

    @staticmethod
    def page(response: object, page: int):
        assert response.json().get('page') == page, \
            f'Неверная страница. Получена {response.json().get("page")} вместо {page}\n'
        print(f'Страница верная - {response.json().get("page")}\n')

    @staticmethod
    def limit(response: object, limit: int):
        assert response.json().get('limit') == limit, \
            f'Неверный лимит. Получен {response.json().get("limit")} вместо {limit}\n'
        print(f'Лимит верный - {response.json().get("limit")}\n')


@allure.title("Paging test")
class TestPaging():
    @staticmethod
    @pytest.mark.parametrize("limit",
                             [pytest.param(limit_list[0], marks=pytest.mark.xfail),
                              *limit_list[1:-1],
                              pytest.param(limit_list[-1], marks=pytest.mark.xfail)])
    def test_paging_limits(limit):
        limit_url = base_url + f'user?limit={limit}'
        response = requests.get(limit_url, headers=headers)
        Check.limit(response, limit)

    @staticmethod
    @pytest.mark.parametrize("page",
                             [pytest.param(pages_list[0], marks=pytest.mark.xfail),
                              *pages_list[1:-1],
                              pytest.param(pages_list[-1], marks=pytest.mark.xfail)])
    def test_paging_pages(page):
        page_url = base_url + f'user?page={page}'
        response = requests.get(page_url, headers=headers)
        Check.page(response, page)


@allure.title("Posts get tests")
class TestGetPosts():
    @staticmethod
    @pytest.mark.parametrize("user_id,status_code",
                             [("60d0fe4f5311236168a10a27", 200),
                              pytest.param("637c795e029551b0a109d55b", 404, marks=pytest.mark.xfail)])
    def test_get_posts_by_user(user_id, status_code):
        post_by_user_url = base_url + f'user/{user_id}/post'
        response = requests.get(post_by_user_url, headers=headers)
        Check.status_code(response, status_code)

    @staticmethod
    @pytest.mark.parametrize("post_id,status_code",
                             [("638cfe32996f1266347911fb", 200),
                              pytest.param("638cfe32996f1266347911fb11111", 400, marks=pytest.mark.xfail)])
    def test_get_post_by_id(post_id, status_code):
        post_by_id_url = base_url + f'post/{post_id}'
        response = requests.get(post_by_id_url, headers=headers)
        Check.status_code(response, status_code)


@allure.title("CRUD steps test")
class TestUser():

    @pytest.mark.parametrize("first_name, last_name, email, status_code",
                             [("firstname", "lastname", test_email, 200),
                              pytest.param("test1", "test1", test_email, 400, marks=pytest.mark.xfail),
                              pytest.param("test1", "test1", f"test{time.strftime('%H%M%S1')}@mail.com", 200,
                                           marks=pytest.mark.xfail),
                              pytest.param("", "test1", f"test{time.strftime('%H%M%S2')}@mail.com", 400,
                                           marks=pytest.mark.xfail),
                              pytest.param("test1", "", f"test{time.strftime('%H%M%S3')}@mail.com", 400,
                                           marks=pytest.mark.xfail),
                              pytest.param("test1", "test1", "", 400, marks=pytest.mark.xfail),
                              pytest.param("", "", "", 400, marks=pytest.mark.xfail)])
    @allure.step("user create")
    def test_create_user(self, first_name, last_name, email, status_code):
        body = {
            'firstName': f'{first_name}',
            'lastName': f'{last_name}',
            'email': f'{email}'
        }
        create_user_url = base_url + "user/create"
        response = requests.post(create_user_url, headers=headers, data=body)
        result = response.json()
        user_id = result.get('id')
        Check.status_code(response, status_code)
        return user_id

    user_id = test_create_user("self", "test1", "test1", f"test{time.strftime('%H%M%S1')}@mail.com", 200)

    @staticmethod
    @pytest.mark.parametrize("first_name, last_name, status_code",
                             [("firstname_edit", "lastname_edit", 200),
                              ("", "lastname_edit", 200),
                              ("firstname_edit", "", 200),
                              ("", "", 200)])
    @pytest.mark.parametrize("user_id",
                             [user_id,
                              pytest.param(f"{user_id}bad", marks=pytest.mark.xfail)])
    @allure.step("user edit")
    def test_edit_user(first_name, last_name, status_code, user_id):
        body = {
            'firstName': f'{first_name}',
            'lastName': f'{last_name}'
        }
        edit_user_url = base_url + f"user/{user_id}"
        response = requests.put(edit_user_url, headers=headers, data=body)
        Check.status_code(response, status_code)
        Check.first_name(response, first_name)
        Check.last_name(response, last_name)

    @staticmethod
    @pytest.mark.parametrize("user_id, status_code",
                             [(user_id, 200),
                              pytest.param(f"{user_id}bad", 400, marks=pytest.mark.xfail)])
    @allure.step("user get")
    def test_get_user(user_id, status_code):
        get_user_url = base_url + f'user/{user_id}'
        response = requests.get(get_user_url, headers=headers)
        Check.status_code(response, status_code)

    @staticmethod
    @pytest.mark.parametrize("user_id, status_code",
                             [(user_id, 200),
                              pytest.param(f"{user_id}bad", 400, marks=pytest.mark.xfail)])
    @allure.step("user delete")
    def test_delete_user(user_id, status_code):
        delete_user_url = base_url + f'user/{user_id}'
        response = requests.delete(delete_user_url, headers=headers)
        Check.status_code(response, status_code)


@allure.title("User CRUD - Smoke test")
class TestCRUD():

    @staticmethod
    def test_user_crud():
        test_email = f"test{time.strftime('%H%M%S')}@mail.com"
        test = TestUser()
        user_id = test.test_create_user("firstname", "lastname", test_email, 200)
        test.test_get_user(user_id, 200)
        test.test_edit_user("new_firstname", "new_lastname", 200, user_id)
        test.test_get_user(user_id, 200)
        test.test_delete_user(user_id, 200)
        test.test_get_user(user_id, 404)

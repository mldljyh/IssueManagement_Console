import getpass
import requests

class AuthManager:
    """
    사용자 인증 및 권한을 관리하는 클래스
    """
    def __init__(self, base_url, session):
        self.base_url = base_url
        self.session = session

    def login(self, username, password):
        """
        사용자의 로그인을 처리하고 성공하면 쿠키를 반환한다.
        """
        data = {"username": username, "password": password}
        response = requests.post(f'{self.base_url}/users/login', json=data)

        if response.status_code == 200:
            return response.cookies
        return None

    def logout(self):
        """
        현재 사용자를 로그아웃한다.
        """
        response = requests.post(
            f'{self.base_url}/users/logout', headers=self.session.get_headers()
        )
        return response.status_code == 200

    def signup(self, username, password, role):
        """
        새로운 사용자 계정을 생성한다. (관리자용)
        """
        data = {"username": username, "password": password, "role": role}
        response = requests.post(
            f'{self.base_url}/users/signup', json=data, headers=self.session.get_headers()
        )
        return response.status_code == 201

    @staticmethod
    def get_credentials():
        """
        사용자로부터 로그인 정보를 입력받는다.
        """
        username = input("아이디: ")
        password = getpass.getpass("비밀번호: ")
        return username, password

    @staticmethod
    def get_new_user_info():
        """
        새로운 사용자 계정 정보를 입력받는다.
        """
        username = input("새로운 아이디: ")
        password = getpass.getpass("새로운 비밀번호: ")
        role = input("역할 (ADMIN, PL, DEV, TESTER): ")
        return username, password, role
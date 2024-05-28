import datetime
import os

import requests

from issuemanagement.auth import AuthManager
from issuemanagement.project import ProjectManager
from issuemanagement.issue import IssueManager
from issuemanagement.comment import CommentManager
from issuemanagement.statistics import StatisticsManager
from issuemanagement.recommendation import RecommendationManager

# API 기본 URL 설정
API_BASE_URL = 'https://swe.mldljyh.tech/api'  

class Session:
    """
    사용자 세션을 나타내는 클래스. 쿠키, 인증 관리자 및 기타 관리자 인스턴스를 저장한다.
    """
    def __init__(self, cookies=None):
        # 사용자 세션 쿠키
        self.cookies = cookies
        # API 호출에 사용될 헤더
        self.auth_manager = AuthManager(API_BASE_URL, self)
        self.project_manager = ProjectManager(API_BASE_URL, self)
        self.issue_manager = IssueManager(API_BASE_URL, self)
        self.comment_manager = CommentManager(API_BASE_URL, self)
        self.statistics_manager = StatisticsManager(API_BASE_URL, self)
        self.recommendation_manager = RecommendationManager(API_BASE_URL, self)

    def get_headers(self):
        """
        JWT 쿠키를 포함한 HTTP 헤더를 반환한다.
        """
        if self.cookies:
            return {'Cookie': f'jwt={self.cookies["jwt"]}'}
        return {}
    
def clear_console():
    """
    콘솔 화면을 지운다.(화면 초기화용)
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def login(session):
    """
    사용자 로그인을 처리한다.
    """
    username, password = AuthManager.get_credentials()
    session.cookies = session.auth_manager.login(username, password)
    if session.cookies:
        print("로그인 성공")
    else:
        print("로그인 실패. 아이디와 비밀번호를 확인하세요.")

def logout(session):
    """
    현재 사용자를 로그아웃한다.
    """
    if session.auth_manager.logout():
        print("로그아웃 되었습니다.")
        session.cookies = None
    else:
        print("로그아웃에 실패했습니다.")

def add_user(session):
    """
    새로운 사용자를 시스템에 추가한다. (관리자용)
    """
    if not session.cookies:
        print("로그인이 필요합니다.")
        return

    username, password, role = AuthManager.get_new_user_info()
    if session.auth_manager.signup(username, password, role):
        print("사용자 계정이 성공적으로 추가되었습니다.")
    else:
        print("사용자 계정 추가에 실패했습니다.")

def manage_projects(session):
    """
    프로젝트 생성 및 삭제 기능을 제공하는 화면
    """
    while True:
        print("\n--- 프로젝트 관리 ---")
        print("1. 프로젝트 생성")
        print("2. 프로젝트 삭제")
        print("3. 돌아가기")
        choice = input("원하는 기능을 선택하세요: ")

        if choice == '1':
            project_name = input("새로운 프로젝트 이름: ")
            if session.project_manager.create_project(project_name):
                print("프로젝트가 성공적으로 생성되었습니다.")
            else:
                print("프로젝트 생성에 실패했습니다.")
        elif choice == '2':
            projects = session.project_manager.load_projects()
            if projects:
                project_index = int(input("삭제할 프로젝트 번호를 선택하세요: ")) - 1
                if 0 <= project_index < len(projects):
                    selected_project_id = projects[project_index]['id']
                    if session.project_manager.delete_project(selected_project_id):
                        print("프로젝트가 성공적으로 삭제되었습니다.")
                    else:
                        print(f"프로젝트 삭제에 실패했습니다.")
                else:
                    print("잘못된 프로젝트 번호입니다.")
            
        elif choice == '3':
            break
        else:
            print("잘못된 입력입니다.")

def project_screen(session, project_id):
    """
    선택한 프로젝트 내에서 이슈를 관리하는 화면
    """
    while True:
        print("\n--- 프로젝트 화면 ---")
        print("1. 이슈 목록보기")
        print("2. 이슈 등록")
        print("3. 이슈 탐색 및 검색")
        print("4. 이슈 자연어 검색")
        print("5. 이슈 통계 분석")
        print("6. 돌아가기")
        choice = input("원하는 기능을 선택하세요: ")

        if choice == '1':
            while True:
                issue_id = session.issue_manager.select_issue(project_id)
                if issue_id is None:
                    break
                while session.issue_manager.view_issue_details(project_id, issue_id):
                    choice = session.comment_manager.handle_comment_actions(session, project_id, issue_id)
                    if choice == '4':
                        session.issue_manager.edit_issue(project_id, issue_id)
                    elif choice == '5':
                        session.recommendation_manager.recommend_assignee(project_id, issue_id)
                    elif choice == '6':
                        break
                    else:
                        print("잘못된 입력입니다.")
                break
        elif choice == '2':
            session.issue_manager.register_issue(project_id)
        elif choice == '3':
            session.issue_manager.browse_and_search_issues(project_id)
        elif choice == '4':
            session.issue_manager.search_issuesbyNL(project_id)
        elif choice == '5':
            session.statistics_manager.analyze_issue_statistics()
        elif choice == '6':
            break
        else:
            print("잘못된 입력입니다.")


def main():
    """
    이슈 관리 콘솔 프로그램 시작 UI
    """
    session = Session()
    while True:
        clear_console()
        if session.cookies:
            print("\n--- 로그인됨 ---")
            print("1. 프로젝트 선택")
            print("2. 계정 추가 (관리자)")
            print("3. 프로젝트 관리 (관리자)")
            print("4. 로그아웃")
            print("0. 종료")
        else:
            print("\n--- 로그아웃됨 ---")
            print("1. 로그인")
            print("0. 종료")

        choice = input("원하는 기능을 선택하세요: ")
        clear_console()
        if choice == '1' and session.cookies:
            projects = session.project_manager.load_projects()
            if projects:
                project_index = int(input("프로젝트 번호를 선택하세요: ")) - 1
                if 0 <= project_index < len(projects):
                    selected_project_id = projects[project_index]["id"]
                    project_screen(session, selected_project_id)
                else:
                    print("잘못된 프로젝트 번호입니다.")
        elif choice == '1' and not session.cookies:
            login(session)
        elif choice == '2' and session.cookies:
            add_user(session)
        elif choice == '3' and session.cookies:
            manage_projects(session)
        elif choice == '4' and session.cookies:
            logout(session)
        elif choice == '0':
            break
        else:
            print("잘못된 입력입니다.")


if __name__ == "__main__":
    main()
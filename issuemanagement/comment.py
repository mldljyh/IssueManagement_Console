import requests

class CommentManager:
    """
    이슈에 대한 댓글을 관리하는 클래스
    """
    def __init__(self, base_url, session):
        self.base_url = base_url
        self.session = session

    def load_comments(self, project_id, issue_id):
        """
        특정 이슈에 대한 모든 댓글을 불러와서 표시한다.
        """
        response = requests.get(
            f"{self.base_url}/projects/{project_id}/issues/{issue_id}/comments",
            headers=self.session.get_headers(),
        )

        if response.status_code == 200:
            comments = response.json()
            print("코멘트:")
            if comments:
                for i, comment in enumerate(comments):
                    print(
                        f"  {i+1}. {comment['username']} ({comment['createdAt']}): {comment['content']}"
                    )
            else:
                print("  코멘트가 없습니다.")
        else:
            print("코멘트를 불러오는 데 실패했습니다.")

    def add_comment(self, project_id, issue_id):
        """
        이슈에 새 댓글을 추가한다.
        """
        content = input("코멘트 내용: ")

        data = {"content": content}
        response = requests.post(
            f'{self.base_url}/projects/{project_id}/issues/{issue_id}/comments',
            json=data,
            headers=self.session.get_headers(),
        )

        if response.status_code == 201:
            print("코멘트가 성공적으로 추가되었습니다.")
        else:
            print(f"코멘트 추가에 실패했습니다. (상태 코드: {response.status_code})")

    def select_comment(self, project_id, issue_id):
        """
        사용자에게 댓글 목록을 보여주고 선택하도록 한다.
        """
        self.load_comments(project_id, issue_id)
        try:
            comment_index = int(input("코멘트 번호를 선택하세요: ")) - 1
            response = requests.get(
                f"{self.base_url}/projects/{project_id}/issues/{issue_id}/comments",
                headers=self.session.get_headers(),
            )
            if response.status_code == 200:
                comments = response.json()
                if 0 <= comment_index < len(comments):
                    return comments[comment_index]['id']
                else:
                    print("잘못된 코멘트 번호입니다.")
                    return None
            else:
                print("코멘트를 불러오는 데 실패했습니다.")
                return None
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력하세요.")
            return None

    def update_comment(self, project_id, issue_id, comment_id):
        """
        기존 댓글을 수정한다.
        """
        content = input("새로운 코멘트 내용: ")

        if content.strip() == "":
            print("코멘트 내용이 비어있습니다. 유효한 내용을 입력해주세요.")
            return

        data = {"content": content}
        response = requests.put(
            f'{self.base_url}/projects/{project_id}/issues/{issue_id}/comments/{comment_id}',
            json=data,
            headers=self.session.get_headers(),
        )

        if response.status_code == 200:
            print("코멘트가 성공적으로 수정되었습니다.")
        elif response.status_code == 400:
            print("잘못된 요청입니다. 코멘트 내용이 비어있을 수 있습니다.")
        elif response.status_code == 404:
            print("코멘트를 찾을 수 없습니다.")
        else:
            print(
                f"코멘트 수정에 실패했습니다. (상태 코드: {response.status_code})"
            )

    def delete_comment(self, project_id, issue_id, comment_id):
        """
        댓글을 삭제한다.
        """
        response = requests.delete(
            f'{self.base_url}/projects/{project_id}/issues/{issue_id}/comments/{comment_id}',
            headers=self.session.get_headers(),
        )

        if response.status_code == 204:
            print("코멘트가 성공적으로 삭제되었습니다.")
        else:
            print(
                f"코멘트 삭제에 실패했습니다. (상태 코드: {response.status_code})"
            )

    def handle_comment_actions(self, session, project_id, issue_id):
        """
        이슈에 대한 댓글 관리 옵션을 제공한다.. (추가, 수정, 삭제)
        """
        while True:
            self.load_comments(project_id, issue_id)
            print("\n--- 이슈 세부 정보 화면 ---")
            print("1. 코멘트 추가")
            print("2. 코멘트 수정")
            print("3. 코멘트 삭제")
            print("4. 이슈 수정") 
            print("5. 담당자 추천")
            print("6. 돌아가기")  
            choice = input("원하는 기능을 선택하세요: ")
            if choice == '1':
                self.add_comment(project_id, issue_id)
            elif choice == '2':
                comment_id = self.select_comment(project_id, issue_id)
                if comment_id:
                    self.update_comment(project_id, issue_id, comment_id)
            elif choice == '3':
                comment_id = self.select_comment(project_id, issue_id)
                if comment_id:
                    self.delete_comment(project_id, issue_id, comment_id)
            elif choice in ('4', '5', '6'):  # Allow returning to previous menus
                return choice
            else:
                print("잘못된 입력입니다.")
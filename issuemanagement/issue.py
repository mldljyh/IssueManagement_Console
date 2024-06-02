import datetime
import requests

class IssueManager:
    """
    이슈를 관리하는 클래스
    """
    def __init__(self, base_url, session):
        self.base_url = base_url
        self.session = session

    def register_issue(self, project_id):
        """
        지정된 프로젝트에 새 이슈를 등록한다.
        """
        title = input("이슈 제목: ")
        description = input("이슈 설명: ")
        reporterUsername = (
            self.session.get_headers()['Cookie'].split('=')[1]
        )  
        reportedDate = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        issue = {
            "title": title,
            "description": description,
            "reporterUsername": reporterUsername,
            "reportedDate": reportedDate,
            "project_id": project_id
            # other fields can be added here
        }

        response = requests.post(
            f'{self.base_url}/projects/{project_id}/issues',
            json=issue,
            headers=self.session.get_headers(),
        )

        if response.status_code == 201:
            print("이슈가 성공적으로 등록되었습니다.")
        else:
            print("이슈 등록에 실패했습니다.")

    def load_issues(self, project_id):
        """
        주어진 프로젝트에 대한 모든 이슈를 불러온다.
        """
        response = requests.get(
            f'{self.base_url}/projects/{project_id}/issues',
            headers=self.session.get_headers(),
        )

        if response.status_code == 200:
            issues = response.json()
            print("\n--- 이슈 목록 ---")
            for i, issue in enumerate(issues):
                print(f"{i+1}. {issue['title']}")
            return issues
        else:
            print("이슈 목록을 불러오는 데 실패했습니다.")
            return None

    def select_issue(self, project_id):
        """
        사용자가 이슈 목록에서 특정 이슈를 선택하도록 한다.
        """
        issues = self.load_issues(project_id)
        if not issues:
            return None

        try:
            issue_index = int(input("이슈 번호를 선택하세요: ")) - 1
            if 0 <= issue_index < len(issues):
                return issues[issue_index]['id']
            else:
                print("잘못된 이슈 번호입니다.")
                return None
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력하세요.")
            return None

    def browse_and_search_issues(self, project_id):
        """
        다양한 기준 (담당자, 등록자, 상태) 에 따라 이슈를 검색한다.
        """
        search_by = input(
            "검색 기준 (assignee, reporter, status, all): "
        ).lower()

        params = {"projectId": project_id}
        if search_by == "assignee":
            assigneeUsername = input("담당자 이름: ")
            params["assigneeUsername"] = assigneeUsername
        elif search_by == "reporter":
            reporterUsername = input("등록자 이름: ")
            params["reporterUsername"] = reporterUsername
        elif search_by == "status":
            status = input(
                "이슈 상태 (NEW, ASSIGNED, FIXED, RESOLVED, CLOSED, REOPENED): "
            ).upper()
            params["status"] = status

        response = requests.get(
            f'{self.base_url}/projects/{project_id}/issues/search',
            params=params,
            headers=self.session.get_headers(),
        )

        if response.status_code == 200:
            issues = response.json()
            if issues:
                print("\n--- 이슈 목록 ---")
                for i, issue in enumerate(issues):
                    print("-" * 20)
                    print(f"{i+1}. {issue['title']} (ID: {issue['id']})")
                    print(f"  설명: {issue['description']}")
                    print(f"  등록자: {issue['reporterUsername']}")
                    print(
                        f"  담당자: {issue['assigneeUsername'] if issue['assigneeUsername'] else '미지정'}"
                    )
                    print(f"  상태: {issue['status']}")
            else:
                print("해당하는 이슈가 없습니다.")
        else:
            print("이슈 검색에 실패했습니다.")

    def search_issuesbyNL(self, project_id):
        """
        자연어 입력을 기반으로 이슈를 검색한다.
        """
        userMessage = input("검색: ")

        params = {"userMessage": userMessage}

        response = requests.get(
            f'{self.base_url}/projects/{project_id}/issues/searchbynl',
            params=params,
            headers=self.session.get_headers(),
        )

        if response.status_code == 200:
            issues = response.json()
            if issues:
                print("\n--- 이슈 목록 ---")
                for i, issue in enumerate(issues):
                    print("-" * 20)
                    print(f"{i+1}. {issue['title']} (ID: {issue['id']})")
                    print(f"  설명: {issue['description']}")
                    print(f"  등록자: {issue['reporterUsername']}")
                    print(
                        f"  담당자: {issue['assigneeUsername'] if issue['assigneeUsername'] else '미지정'}"
                    )
                    print(f"  상태: {issue['status']}")
            else:
                print("해당하는 이슈가 없습니다.")
        else:
            print("이슈 검색에 실패했습니다.")

    def view_issue_details(self, project_id, issue_id):
        """
        선택한 이슈의 세부 정보를 표시한다.
        """
        response = requests.get(
            f'{self.base_url}/projects/{project_id}/issues/{issue_id}',
            headers=self.session.get_headers(),
        )

        if response.status_code == 200:
            issue = response.json()
            print("-" * 20)
            print(f"ID: {issue['id']}")
            print(f"제목: {issue['title']}")
            print(f"설명: {issue['description']}")
            print(f"등록자: {issue['reporterUsername']}")
            print(f"등록일: {issue['reportedDate']}")
            print(
                f"해결자: {issue['fixerUsername'] if issue['fixerUsername'] else '미지정'}"
            )
            print(
                f"담당자: {issue['assigneeUsername'] if issue['assigneeUsername'] else '미지정'}"
            )
            print(f"우선순위: {issue['priority']}")
            print(f"상태: {issue['status']}")
            print("-" * 20)
            return True
        else:
            print("이슈 정보를 불러오는 데 실패했습니다.")
            return False

    def edit_issue(self, project_id, issue_id):
        """
        기존 이슈의 세부 정보를 수정할 수 있도록 한다. (관리자 및 테스터 전용)
        """
        # Get current issue details
        response = requests.get(
            f'{self.base_url}/projects/{project_id}/issues/{issue_id}',
            headers=self.session.get_headers(),
        )

        if response.status_code != 200:
            print("이슈 정보를 불러오는 데 실패했습니다.")
            return

        issue = response.json()

        print("\n--- 이슈 수정 ---")
        print("1. 제목")
        print("2. 설명")
        print("3. 우선순위 (BLOCKER, CRITICAL, MAJOR, MINOR, TRIVIAL)")
        print("4. 상태 (NEW, ASSIGNED, FIXED, RESOLVED, CLOSED, REOPENED)")
        print("5. 담당자")
        print("6. 돌아가기")

        while True:
            choice = input("수정할 항목을 선택하세요 (1-6): ")
            if choice == '1':
                issue['title'] = input("새로운 제목: ")
                break
            elif choice == '2':
                issue['description'] = input("새로운 설명: ")
                break
            elif choice == '3':
                issue['priority'] = input("새로운 우선순위: ").upper()
                break
            elif choice == '4':
                issue['status'] = input("새로운 상태: ").upper()
                break
            elif choice == '5':
                response = requests.get(
                    f'{self.base_url}/users/devs', headers=self.session.get_headers()
                )
                if response.status_code == 200:
                    devs = response.json()
                    print("개발자 목록:")
                    for dev in devs:
                        print(f'이름: {dev["username"]}')
                    assignee_name = input("담당자를 선택해주세요: ")
                    issue["assigneeUsername"] = assignee_name
                    issue['status'] = 'ASSIGNED'
                else:
                    print("개발자 목록을 불러오는 데 실패했습니다.")
                break
            elif choice == '6':
                return
            else:
                print("잘못된 입력입니다.")

        response = requests.put(
            f'{self.base_url}/projects/{project_id}/issues/{issue_id}',
            json=issue,
            headers=self.session.get_headers(),
        )
        if response.status_code == 200:
            print("이슈가 성공적으로 수정되었습니다.")
        else:
            print("이슈 수정에 실패했습니다.")
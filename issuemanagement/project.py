import requests

class ProjectManager:
    """
    프로젝트를 관리하는 클래스
    """
    def __init__(self, base_url, session):
        self.base_url = base_url
        self.session = session

    def create_project(self, project_name):
        """
        새로운 프로젝트를 생성한다.
        """
        data = {"name": project_name}
        response = requests.post(
            f'{self.base_url}/projects', json=data, headers=self.session.get_headers()
        )
        return response.status_code == 201

    def load_projects(self):
        """
        모든 프로젝트를 불러온다.
        """
        response = requests.get(
            f'{self.base_url}/projects', headers=self.session.get_headers()
        )

        if response.status_code == 200:
            projects = response.json()
            print("\n--- 프로젝트 목록 ---")
            for i, project in enumerate(projects):
                print(f"{i+1}. {project['name']}")
            return projects
        else:
            print("프로젝트 목록을 불러오는 데 실패했습니다.")
            return None

    def delete_project(self, project_id):
        """
        ID를 기반으로 프로젝트를 삭제한다.
        """
        response = requests.delete(
            f'{self.base_url}/projects/{project_id}', headers=self.session.get_headers()
        )
        return response.status_code == 204
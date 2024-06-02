import requests

class RecommendationManager:
    """
    이슈 담당자 추천을 관리하는 클래스
    """
    def __init__(self, base_url, session):
        self.base_url = base_url
        self.session = session

    def recommend_assignee(self, project_id, issue_id):
        """
        이슈에 대한 잠재적인 담당자를 추천한다.
        """
        response = requests.get(
            f'{self.base_url}/projects/{project_id}/issues/{issue_id}/recommendedAssignees',
            headers=self.session.get_headers(),
        )
        if response.status_code == 200:
            recommended_assignees = response.json()
            print("추천 담당자:")
            for i, assignee in enumerate(recommended_assignees):
                print(f"  {i+1}. {assignee['username']}")
        else:
            print("담당자 추천에 실패했습니다.")
import requests

class StatisticsManager:
    """
    이슈 통계 분석을 관리하는 클래스
    """
    def __init__(self, base_url, session):
        self.base_url = base_url
        self.session = session

    def analyze_issue_statistics(self):
        """
        월별 이슈 수 통계를 검색하고 표시한다.
        """
        response = requests.get(
            f'{self.base_url}/statistics/issuesPerMonth',
            headers=self.session.get_headers(),
        )
        if response.status_code == 200:
            issues_per_month = response.json()
            print("월별 이슈 수:")
            for month, count in issues_per_month.items():
                print(f"  - {month}: {count}")
        else:
            print("이슈 통계 정보를 불러오는 데 실패했습니다.")
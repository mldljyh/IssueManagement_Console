import requests
import matplotlib.pyplot as plt
import numpy as np

class StatisticsManager:
    """
    이슈 통계 분석을 관리하는 클래스
    """
    def __init__(self, base_url, session):
        self.base_url = base_url
        self.session = session
        self.project_id = None

    def analyze_issue_statistics(self, project_id):
        """
        다양한 이슈 통계 분석 옵션을 제공한다.
        """
        self.project_id = project_id
        while True:
            print("\n--- 이슈 통계 분석 ---")
            print("1. 월별 이슈 수 (꺾은선 그래프)")
            print("2. 이슈 상태별 수 (막대 그래프)")
            print("3. 이슈 담당자별 해결/미해결 수 (막대 그래프)")
            print("4. 상태별 일주일 간 이슈 수 (꺾은선 그래프)")
            print("5. 댓글 수 상위 3개 이슈 (막대 그래프)")
            print("6. 한 달 동안의 일자별 이슈 수 (꺾은선 그래프)")
            print("7. 우선순위별 일주일 간 이슈 수 (꺾은선 그래프)")
            print("8. 이번 달 우선순위별 이슈 수 (파이 그래프)")
            print("9. 상태별 일주일 간 이슈 수 (막대 그래프)")
            print("10. 돌아가기")

            choice = input("원하는 기능을 선택하세요: ")

            if choice == '1':
                self.get_issues_per_month_chart()
            elif choice == '2':
                self.get_issues_per_status_chart()
            elif choice == '3':
                self.get_issues_per_fixer_chart()
            elif choice == '4':
                self.get_issues_per_day_and_status_in_week_chart()
            elif choice == '5':
                self.get_issues_order_by_comments_chart()
            elif choice == '6':
                self.get_issues_per_day_in_month_chart()
            elif choice == '7':
                self.get_issues_per_day_and_priority_in_week_chart()
            elif choice == '8':
                self.get_issues_per_priority_in_month_chart()
            elif choice == '9':
                self.get_issues_per_day_and_status_in_week()
            elif choice == '10':
                break
            else:
                print("잘못된 입력입니다.")

    def _request_statistics_data(self, endpoint):
        """
        통계 데이터를 요청하는 내부 함수
        """
        response = requests.get(
            f'{self.base_url}/projects/{self.project_id}/statistics/{endpoint}',
            headers=self.session.get_headers(),
        )
        if response.status_code == 200:
            return response.json()
        else:
            print("이슈 통계 정보를 불러오는 데 실패했습니다.")
            return None

    def get_issues_per_month_chart(self):
        """
        월별 이슈 수를 꺾은선 그래프로 표시한다.
        """
        data = self._request_statistics_data('issuesPerMonth')
        if data:
            months = list(data.keys())
            counts = list(data.values())

            plt.figure(figsize=(10, 5))
            plt.plot(months, counts, marker='o')
            plt.xlabel('Month')
            plt.ylabel('Number of Issues')
            plt.title('Number of Issues Per Month')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()

    def get_issues_per_status_chart(self):
        """
        이슈 상태별 수를 막대 그래프로 표시한다.
        """
        data = self._request_statistics_data('issuesPerStatus')
        if data:
            status = list(data.keys())
            counts = list(data.values())

            plt.figure(figsize=(10, 5))
            plt.bar(status, counts)
            plt.xlabel('Issue Status')
            plt.ylabel('Number of Issues')
            plt.title('Number of Issues Per Status')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()

    def get_issues_per_fixer_chart(self):
        """
        이슈 담당자별 해결/미해결 수를 막대 그래프로 표시한다.
        """
        data = self._request_statistics_data('issuesPerFixer')
        if data:
            fixers = list(data.keys())
            resolved_counts = []
            closed_counts = []
            other_counts = []

            for fixer in fixers:
                resolved_counts.append(data[fixer].get('RESOLVED', 0))
                closed_counts.append(data[fixer].get('CLOSED', 0))
                other_counts.append(
                    data[fixer].get('OTHER', 0) if 'OTHER' in data[fixer] else 0
                )

            width = 0.25  # the width of the bars

            fig, ax = plt.subplots(figsize=(10, 5))

            x = range(len(fixers))
            rects1 = ax.bar(x, resolved_counts, width, label='Resolved')
            rects2 = ax.bar(
                [i + width for i in x], closed_counts, width, label='Closed'
            )
            rects3 = ax.bar(
                [i + 2 * width for i in x], other_counts, width, label='Other'
            )

            ax.set_xlabel('Fixer')
            ax.set_ylabel('Number of Issues')
            ax.set_title('Number of Issues Per Fixer (Resolved/Closed)')
            ax.set_xticks([i + width for i in x])
            ax.set_xticklabels(fixers)
            ax.legend()

            fig.tight_layout()
            plt.show()

    def get_issues_per_day_and_status_in_week_chart(self):
        """
        상태별 일주일 간 이슈 수를 꺾은선 그래프로 표시한다.
        """
        status = input(
            "이슈 상태 (NEW, ASSIGNED, FIXED, RESOLVED, CLOSED, REOPENED): "
        ).upper()
        data = self._request_statistics_data(
            f'issuesPerDayAndStatusInWeek/{status}'
        )
        if data:
            days = list(data.keys())
            counts = list(data.values())

            plt.figure(figsize=(10, 5))
            plt.plot(days, counts, marker='o')
            plt.xlabel('Day')
            plt.ylabel('Number of Issues')
            plt.title(f'Number of Issues in a Week (Status: {status})')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()

    def get_issues_order_by_comments_chart(self):
        """
        댓글 수 상위 3개 이슈를 막대 그래프로 표시한다.
        """
        data = self._request_statistics_data('issuesOrderByComments')
        if data:
            issues = list(data.keys())
            comment_counts = list(data.values())

            plt.bar(issues, comment_counts)
            plt.xlabel('Issue Title')
            plt.ylabel('Number of Comments')
            plt.title('Top 3 Issues by Comment Count')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()

    def get_issues_per_day_in_month_chart(self):
        """
        한 달 동안의 일자별 이슈 수를 꺾은선 그래프로 표시한다.
        """
        data = self._request_statistics_data('issuesPerDayInMonth')
        if data:
            days = list(data.keys())
            counts = list(data.values())

            plt.figure(figsize=(10, 5))
            plt.plot(days, counts, marker='o')
            plt.xlabel('Day')
            plt.ylabel('Number of Issues')
            plt.title('Number of Issues Per Day in This Month')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()


    def get_issues_per_day_and_priority_in_week_chart(self):
        """
        우선순위별 일주일 간 이슈 수를 꺾은선 그래프로 표시한다.
        """
        priority = input(
            "이슈 우선순위 (BLOCKER, CRITICAL, MAJOR, MINOR, TRIVIAL): "
        ).upper()
        data = self._request_statistics_data(
            f'issuesPerDayAndPriorityInWeek/{priority}'
        )
        if data:
            days = list(data.keys())
            counts = list(data.values())

            plt.figure(figsize=(10, 5))
            plt.plot(days, counts, marker='o')
            plt.xlabel('Day')
            plt.ylabel('Number of Issues')
            plt.title(f'Number of Issues in a Week (Priority: {priority})')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()

    def get_issues_per_priority_in_month_chart(self):
        """
        이번 달 우선순위별 이슈 수를 파이 그래프로 표시한다.
        """
        data = self._request_statistics_data('issuesPerPriorityInMonth')
        if data:
            priority = list(data.keys())
            counts = list(data.values())

            # 파이 그래프에 개수 표시
            def func(pct, allvals):
                absolute = int(pct / 100. * np.sum(allvals))
                return "{:.1f}%\n({:d} issues)".format(pct, absolute)

            plt.figure(figsize=(10, 5))
            plt.pie(counts, labels=priority, autopct=lambda pct: func(pct, counts), startangle=90)
            plt.title('Number of Issues by Priority (This Month)')
            plt.tight_layout()
            plt.show()


    def get_issues_per_day_and_status_in_week(self):
        """
        일자별, 상태별 이슈 수를 누적 막대 그래프로 표시한다.
        """
        data = self._request_statistics_data('issuesPerDayAndStatusInWeek')
        if data:
            days = list(data.keys())
            status_data = {}
            for day in days:
                for status, count in data[day].items():
                    if status not in status_data:
                        status_data[status] = []
                    status_data[status].append(count)

            colors = {
                'NEW': 'lightblue',
                'ASSIGNED': 'lightgreen',
                'FIXED': 'lightyellow',
                'RESOLVED': 'lightcoral',
                'CLOSED': 'lightgray',
                'REOPENED': 'orange',
            }

            plt.figure(figsize=(10, 5))
            bottom = [0] * len(days) 

            for status, counts in status_data.items():
                bars = plt.bar(days, counts, label=status, bottom=bottom, color=colors.get(status, 'gray')) 
                bottom = [b + c for b, c in zip(bottom, counts)]  

            plt.xlabel('Day')
            plt.ylabel('Number of Issues')
            plt.title('Number of Issues per Day and Status in Week')
            plt.xticks(rotation=45, ha='right')
            plt.legend()
            plt.tight_layout()

            max_issues = max(sum(status_data[status]) for status in status_data)
            plt.ylim(0, max_issues * 1.5) 

            plt.show()

        
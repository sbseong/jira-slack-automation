import requests
from datetime import datetime

# ▶︎ 설정값
JIRA_DOMAIN = "https://huinno.atlassian.net"
API_EMAIL = "sbseong@huinno.com"
API_TOKEN = "JIRA_TOKEN"
SLACK_WEBHOOK = "https://hooks.slack.com/services/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"

# ▶︎ 필터 JQL
JQL = """
created >= -30d
AND project = TEL
AND type IN (Story, Task, BUG)
AND status IN ("In Progress", 신규등록)
AND assignee IN (currentUser(), 61133043fc68c1006947a0f7, 6052a241311e270068d6b369, 70121:303b7e25-b169-4f9a-8b09-bd75e45aae22, 6099d6dd99b21f0070509182)
ORDER BY created DESC
"""

# ▶︎ JIRA API 호출
res = requests.get(
    f"{JIRA_DOMAIN}/rest/api/3/search",
    params={"jql": JQL, "maxResults": 20},
    headers={"Accept": "application/json"},
    auth=(API_EMAIL, API_TOKEN)
)

issues = res.json().get("issues", [])

# ▶︎ 메시지 구성
if not issues:
    message = "📋 오늘의 백로그는 없습니다!"
else:
    message = "📋 *오늘의 TEL 백로그 (최근 30일)*\n"
    for issue in issues:
        key = issue["key"]
        summary = issue["fields"]["summary"]
        status = issue["fields"]["status"]["name"]
        url = f"{JIRA_DOMAIN}/browse/{key}"
        message += f"• <{url}|{key}> - {summary} ({status})\n"

# ▶︎ Slack 전송
slack_res = requests.post(SLACK_WEBHOOK, json={"text": message})
print(f"Slack 전송 결과: {slack_res.status_code}")

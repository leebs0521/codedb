import requests
import os
import json
from db_utils import connect_to_database, find_repository_by_name_and_owner
# GitHub API 토큰 설정
github_token = "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"
headers = {"Authorization": f"token {github_token}"}


def load_repo_info(language):
    # 파일에서 저장된 저장소 정보를 로드합니다.
    file_path = f'/home/lbs/codedb/src/info/repos_api_{language}.json'
    print(file_path)
    
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            repo_data = json.load(file)
        return repo_data
    else:
        # 파일이 없는 경우 GitHub API로부터 데이터를 가져옵니다.
        repo_data = fetch_repo_info(language)
        return repo_data


def fetch_repo_info(language):
    file_path = f'/home/lbs/codedb/src/info/repos_api_{language}.json'
    
    sort = "stars"
    per_page = 100
    
    # GitHub API를 사용하여 저장소 검색
    search_url = f"https://api.github.com/search/repositories?q=language:{language}&sort={sort}&per_page={per_page}"
    response = requests.get(search_url, headers=headers)
    data = response.json()
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    return data


def get_repo_list_by_lagnuage(language):
    repo_info = load_repo_info(language)
    repo_list = []

    for repo in repo_info['items']:
        repo_name = repo['name']
        repo_owner = repo['owner']['login']

        conn = connect_to_database()
        if not find_repository_by_name_and_owner(conn, repo_name, repo_owner):
            repo_list.append(repo['full_name'])
        conn.close()

    return repo_list


if __name__ == '__main__':
    # 언어에 대한 저장소 정보를 로드하고 출력합니다.
    language = 'cpp'

    repo_list = get_repo_list_by_lagnuage(language)
    print(repo_list)
    print(len(repo_list))

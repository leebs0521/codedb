import requests
import os
import json
from db_utils import connect_to_database, find_repository_by_name_and_owner

# GitHub API 토큰 설정
github_token = ""
headers = {"Authorization": f"token {github_token}"}


def load_repo_info(language):
    # 파일에서 저장된 저장소 정보를 로드합니다.
    file_path = f'/home/lbs/codedb/src/info/repos_api_{language}.json'
    print(file_path)
    
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            repo_data = json.load(file)
    
    else:
        # 파일이 없는 경우 GitHub API로부터 데이터를 가져옵니다.
        sort = "stars"
        per_page = 100
        
        # GitHub API를 사용하여 저장소 검색
        search_url = f"https://api.github.com/search/repositories?q=language:{language}&sort={sort}&per_page={per_page}"
        response = requests.get(search_url, headers=headers)
        repo_data = response.json()
        
        with open(file_path, 'w') as f:
            json.dump(repo_data, f, indent=2)
    
    return repo_data


def get_repo_list_by_lagnuage(language):
    # 언어에 해당하는 저장소 정보 로드
    repo_info = load_repo_info(language)
    repo_list = []

    # 각 저장소에 대한 정보 처리
    for repo in repo_info['items']:
        repo_name = repo['name']
        repo_owner = repo['owner']['login']

        # 데이터베이스에 연결
        conn = connect_to_database()
  
        # 저장소가 데이터베이스에 존재하지 않으면 리스트에 추가
        if not find_repository_by_name_and_owner(conn, repo_name, repo_owner):
            repo_list.append(repo['full_name'])

        # 데이터베이스 연결 종료
        conn.close()

    return repo_list


if __name__ == '__main__':
    # 언어에 대한 저장소 정보를 로드하고 출력합니다.
    language = 'c'

    repo_list = get_repo_list_by_lagnuage(language)
    print(repo_list)
    print(len(repo_list))

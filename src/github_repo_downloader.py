import requests, json, os, re
from utils import unzip_file

# GitHub API 토큰 설정
github_token = ""
headers = {"Authorization": f"token {github_token}"}


def generate_version_name(tag_name):
    version = ""
    numbers = re.findall(r'\d+', tag_name)
    if numbers:
        version = 'v' + '.'.join(numbers)
    return version


def fetch_repo_info_from_github(repo_owner, repo_name):

    # GitHub API를 사용하여 저장소 검색
    search_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    response = requests.get(search_url, headers=headers)
    data = response.json()

    return data


def download_github_repo(repo_owner, repo_name):
    data = fetch_repo_info_from_github(repo_owner, repo_name)

    repo_name = data['name']
    repo_owner = data['owner']['login']
    full_name = data['full_name']
    repo_path = f'/home/lbs/codedb/target/{repo_owner}_{repo_name}'
    url = data['url']
    platform = 'github'
    stars_count = data['stargazers_count']


    # 저장소의 태그 정보 가져오기
    tags_url = f"{url}/tags"
    response = requests.get(tags_url, headers=headers)
    tags_data = response.json()
    versions = []

    if len(tags_data) > 0:
        # 각 태그별로 다운로드 링크 생성
        for tag in tags_data:
            tag_name = tag["name"]
            ver = tag_name.replace("/", "_")
            zipball_url = f"{url}/zipball/refs/tags/{tag_name}"
            dir_path = f"/home/lbs/codedb/target/{repo_owner}_{repo_name}/{ver}"

            # 디렉토리 생성 및 다운로드
            os.makedirs(dir_path, exist_ok=True)
            return_code = os.system(f"curl -L {zipball_url} -o {dir_path}/{ver}.zip")
            if return_code == 0:
                print(f"{dir_path}/{ver}.zip 다운로드 성공.")
                zip_file_path = f'{dir_path}/{ver}.zip'
                unzip_file(zip_file_path, dir_path)
                downloaded = True
            else:
                print(f"{dir_path}/{ver}.zip 다운로드 실패. code: {return_code}")
                downloaded = False

            version_name = generate_version_name(tag_name)
            versions.append({"version_name": version_name, "tag_name": tag_name, "dir_path": dir_path,
                             "downloaded": downloaded})
    else:
        tag_name = data["default_branch"]
        base_dir = f"/home/lbs/codedb/target/{repo_owner}_{repo_name}"
        dir_path = f"/home/lbs/codedb/target/{repo_owner}_{repo_name}/{tag_name}"

        # 디렉토리 생성 및 다운로드
        os.makedirs(base_dir, exist_ok=True)
        return_code = os.system(f"git clone {data['clone_url']} {dir_path}")

        if return_code == 0:
            print(f"{dir_path} 다운로드 성공.")
            downloaded = True
        else:
            print(f"{dir_path} 다운로드 실패. code: {return_code}")
            downloaded = False

        version_name = generate_version_name(tag_name)
        versions.append({"version_name": version_name, "tag_name": tag_name, "dir_path": dir_path,
                         "downloaded": downloaded})

    repo_dict = {
        "repo_name": repo_name,
        "repo_owner": repo_owner,
        "full_name": full_name,
        "repo_path": repo_path,
        "url": url,
        "platform": platform,
        "stars_count": stars_count,
        "versions": versions
    }

    # repo_dict 딕셔너리를 JSON 파일로 저장
    output_file = f'{repo_path}/info.json'
    with open(output_file, 'w') as json_file:
        json.dump(repo_dict, json_file, indent=4)

    print(f"Repository 정보가 {output_file}에 저장되었습니다.")


if __name__ == "__main__":
    repo_owner = "gnutls"
    repo_name = "gnutls"
    download_github_repo(repo_owner, repo_name)
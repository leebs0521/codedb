import json
from downloader import generate_version_name
from utils import get_repository_info, unzip_file
import os


# 레포지토리 내의 특정 태그 수동 다운로드 함수
def repository_tag_download(repo_owner, repo_name, tag_list):
    base_dir = '/home/lbs/codedb/target'
    info_json_path = f'{base_dir}/{repo_owner}_{repo_name}/info.json'
    repo_info = get_repository_info(info_json_path)
    url = repo_info['url']

    for tag_name in tag_list:

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
        repo_info['versions'].append(
            {"version_name": version_name, "tag_name": tag_name, "dir_path": dir_path,
            "downloaded": downloaded})

    # repo_dict 딕셔너리를 JSON 파일로 저장
    output_file = f'/home/lbs/codedb/target/{repo_owner}_{repo_name}/info1.json'
    with open(output_file, 'w') as json_file:
        json.dump(repo_info, json_file, indent=4)


    print(f"Repository 정보가 {output_file}에 업데이트 되었습니다.")


if __name__ == "__main__":
    tag_list = ['v3.2.4', 'v3.2.4-with-msvs2012-fix', 'v3.2.3', 'v3.2.3-rc1', 'v3.2.2.1', 'v3.2.2', 'v3.2.2-rc1', 'v3.2.1', 'v3.2.0', 'v3.2.0-rc2']
    repo_owner = 'wxWidgets'
    repo_name = 'wxWidgets'

    repository_tag_download(repo_owner, repo_name, tag_list)
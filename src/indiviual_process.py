import json
import os

from db_utils import insert_data_to_database
from parsing import process_directory, save_dict_to_json
from utils import unzip_file

info = {
    "name": "golang.org/x/sync",
    "versions": [
        {
            "version": "v0.5.0",
            "download_url": "https://go.googlesource.com/sync/+archive/refs/tags/v0.5.0.tar.gz",
        },
		{
            "version": "v0.4.0",
            "download_url": "https://go.googlesource.com/sync/+archive/refs/tags/v0.4.0.tar.gz",
        },
		{
            "version": "v0.3.0",
            "download_url": "https://go.googlesource.com/sync/+archive/refs/tags/v0.3.0.tar.gz",
        },
		{
            "version": "v0.2.0",
            "download_url": "https://go.googlesource.com/sync/+archive/refs/tags/v0.2.0.tar.gz",
        },
		{
            "version": "v0.1.0",
            "download_url": "https://go.googlesource.com/sync/+archive/refs/tags/v0.1.0.tar.gz",
        },
	]
}


def download(info):
    repo_name = info['name']
    repo_owner = ''
    full_name = repo_name
    repo_path = f'/home/lbs/codedb/target/{repo_name.replace("/", "_")}'
    url = ''
    platform = 'other'
    stars_count = 0

    versions = []

    for version_info in info['versions']:
        version = version_info['version']
        download_url = version_info['download_url']
        dir_path = f'{repo_path}/{version.replace("/", "_")}'
        file_name = version_info['download_url'].split('/')[-1]

        # 디렉토리 생성 및 다운로드
        os.makedirs(dir_path, exist_ok=True)

        return_code = os.system(f"curl -L {download_url} -o {dir_path}/{file_name}")
        if return_code == 0:
            print(f"{dir_path}/{file_name} 다운로드 성공.")
            zip_file_path = f'{dir_path}/{file_name}'
            unzip_file(zip_file_path, dir_path)
            downloaded = True
        else:
            print(f"{dir_path}/{file_name} 다운로드 실패. code: {return_code}")
            downloaded = False

        versions.append({"version_name": version, "tag_name": "", "dir_path": dir_path,
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

    #repo_dict 딕셔너리를 JSON 파일로 저장
    output_file = f'{repo_path}/info.json'
    with open(output_file, 'w') as json_file:
        json.dump(repo_dict, json_file, indent=4)

    print(f"Repository 정보가 {output_file}에 저장되었습니다.")

    return repo_dict


def process(repo_info):

    identifier = repo_info['repo_name']

    if repo_info['repo_name']:
        print(
            f"Repository Info: Full Name={repo_info['full_name']}, Platform={repo_info['platform']}, \
                    # of Stars={repo_info['stars_count']}, # of Versions={len(repo_info['versions'])}")

    res_dir = f'/home/lbs/codedb/results/{identifier.replace("/", "_")}'
    os.makedirs(res_dir, exist_ok=True)

    versions = repo_info.pop('versions')
    for version in versions:
        if version.get('downloaded'):
            res_dict = {
                "repository": repo_info,
                "version": version,
                "functions": []
            }
            version_name = version.get('version_name')
            dir_path = version.get('dir_path')

            file_functions = process_directory(dir_path, identifier)
            res_dict['functions'] = file_functions['data']
            save_dict_to_json(res_dict, f'{res_dir}/{version_name.replace("/","_")}.json')
            """json file to database"""
            insert_data_to_database(res_dict)
        else:
            print(f"Tag '{version_name} is not downloaded.")


if __name__ == "__main__":

    result_info = download(info)
    process(result_info)


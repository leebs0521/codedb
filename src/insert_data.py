import os, json
from utils import get_repository_info
from parsing import process_directory
from db_utils import insert_data_to_database


def process(repo_owner, repo_name):
    # identifier 및 repo_path 설정
    identifier = f'{repo_owner}_{repo_name}'
    repo_path = f'/home/lbs/codedb/target/{repo_owner}_{repo_name}'
    json_file_path = f'{repo_path}/info.json'

    # repo_info 가져오기
    repo_info = get_repository_info(json_file_path)

    # repo_info가 존재하는 경우 처리
    if repo_info['repo_name']:
        print(
            f"Repository Info: Full Name={repo_info['full_name']}, Platform={repo_info['platform']}, \
            # of Stars={repo_info['stars_count']}, # of Versions={len(repo_info['versions'])}")

        # 결과 디렉토리 생성
        res_dir = f'/home/lbs/codedb/results/{identifier}'
        os.makedirs(res_dir, exist_ok=True)

        # 버전 정보 가져오기
        versions = repo_info.pop('versions')
        
        # 각 버전에 대한 처리
        for version in versions:
            if version.get('downloaded'):
                res_dict = {
                    "repository": repo_info,
                    "version": version,
                    "functions": []
                }
                # tag_name 및 dir_path 설정
                tag_name = version.get('tag_name').replace("/", "_")
                dir_path = version.get('dir_path')

                 # 디렉토리에서 함수 정보 가져오기
                file_functions = process_directory(dir_path, identifier)
                res_dict['functions'] = file_functions['data']
                
                # JSON 파일로 결과 저장
                with open(f'{res_dir}/{tag_name}.json', 'w') as json_file:
                    json.dump(res_dict, json_file, indent=4)
                
                # 데이터베이스에 JSON 파일 내용 삽입
                insert_data_to_database(res_dict)
                
            else:
                print(f"Tag '{tag_name} is not downloaded.")


if __name__ == "__main__":
    repo_owner = 'xbmc'
    repo_name = 'xbmc'
    process(repo_owner, repo_name)
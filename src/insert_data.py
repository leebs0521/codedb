from utils import unzip_file, get_repository_info
from parsing import process_directory, save_dict_to_json
import os
from db_utils import insert_data_to_database


def process(repo_owner, repo_name):
    identifier = f'{repo_owner}_{repo_name}'
    repo_path = f'/home/lbs/codedb/target/{repo_owner}_{repo_name}'
    json_file_path = f'{repo_path}/info.json'
    repo_info = get_repository_info(json_file_path)

    if repo_info['repo_name']:
        print(
            f"Repository Info: Full Name={repo_info['full_name']}, Platform={repo_info['platform']}, \
            # of Stars={repo_info['stars_count']}, # of Versions={len(repo_info['versions'])}")

        res_dir = f'/home/lbs/codedb/results/{identifier}'
        os.makedirs(res_dir, exist_ok=True)

        versions = repo_info.pop('versions')
        for version in versions:
            if version.get('downloaded'):
                res_dict = {
                    "repository": repo_info,
                    "version": version,
                    "functions": []
                }
                tag_name = version.get('tag_name').replace("/", "_")
                dir_path = version.get('dir_path')

                file_functions = process_directory(dir_path, identifier)
                res_dict['functions'] = file_functions['data']
                save_dict_to_json(res_dict, f'{res_dir}/{tag_name}.json')
                """json file to database"""
                insert_data_to_database(res_dict)
            else:
                print(f"Tag '{tag_name} is not downloaded.")


if __name__ == "__main__":
    repo_owner = 'gnutls'
    repo_name = 'gnutls'
    process(repo_owner, repo_name)
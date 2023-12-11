import shutil
import zipfile
import json


def unzip_file(zipfile_path, extraction_path):
    try:
        shutil.unpack_archive(zipfile_path, extraction_path)
        print(f"Successfully unzipped {zipfile_path} to {extraction_path}")
    except FileNotFoundError:
        print(f"File not found: {zipfile_path}")
    except zipfile.BadZipFile:
        print(f"Invalid zip file: {zipfile_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_repository_info(json_file_path):
    repo_info = {
        'repo_name': '',
        'repo_owner': '',
        'full_name': '',
        'repo_path': '',
        'url': '',
        'platform': '',
        'stars_count': 0,
        'versions': [],
    }

    try:
        with open(json_file_path, 'r') as json_file:
            json_data = json.load(json_file)

        repo_info['repo_name'] = json_data.get('repo_name', '')
        repo_info['repo_owner'] = json_data.get('repo_owner', '')
        repo_info['full_name'] = json_data.get('full_name', '')
        repo_info['repo_path'] = json_data.get('repo_path', '')
        repo_info['url'] = json_data.get('url', '')
        repo_info['platform'] = json_data.get('platform', '')
        repo_info['stars_count'] = json_data.get('stars_count', 0)
        repo_info['versions'] = json_data.get('versions', [])

    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
    except json.JSONDecodeError:
        print(f"Invalid JSON in file: {json_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return repo_info


if __name__ == "__main__":
    info_path = '/home/lbs/codedb/target/gnutls_gnutls/info.json'
    data = get_repository_info(info_path)
    print(data)

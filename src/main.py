import multiprocessing
from datetime import datetime
from pytz import timezone

from github_repo_downloader import get_repo_list_by_lagnuage
from db_utils import connect_to_database, find_repository_by_name_and_owner
import downloader
import insert_data


def write_log(mode, message):
    with open('./progress_log.txt', mode=mode) as f:
        print(message, file=f)


def process_repo(repo):
    repo_owner, repo_name = repo.split('/')

    conn = connect_to_database()
    
    flag = find_repository_by_name_and_owner(conn, repo_name, repo_owner)
    conn.close()
    if not flag:
        start_message = f'{repo_owner}/{repo_name} | {datetime.now(timezone("Asia/Seoul"))} | Start.'
        downloader.download(repo_owner, repo_name)
        insert_data.process(repo_owner, repo_name)

        end_message = f'{repo_owner}/{repo_name} | {datetime.now(timezone("Asia/Seoul"))} | End.'
        write_log('a', start_message)
        write_log('a', end_message)
    
        
if __name__ == "__main__":

    repo_list = get_repo_list_by_lagnuage('cpp')
    message = f'Start time | {datetime.now(timezone("Asia/Seoul"))}'
    write_log('a', message)

    # 프로세스 풀 생성
    num_processes = 5
    pool = multiprocessing.Pool(processes=num_processes)

    # 각 repository에 대한 작업을 병렬로 실행
    pool.map(process_repo, repo_list)

    # 프로세스 풀 종료
    pool.close()
    pool.join()

    message = f'End time | {datetime.now(timezone("Asia/Seoul"))}'
    write_log('a', message)

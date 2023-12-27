import pymysql


def connect_to_database():
    # 데이터베이스 연결 설정
    db_config = {
        "host": "",
        "user": "",
        "password": "",
        "database": "",
        "charset": ""
    }

    try:
        # 연결 시도
        conn = pymysql.connect(**db_config)
        return conn
    except pymysql.Error as e:
        print(f"Database connection error: {e}")
        return None


# 'repositories' 테이블에 데이터 삽입
def insert_repository_data(conn, repo_name, repo_owner, full_name, repo_path, url, platform, stars_count):
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        insert_data = "INSERT INTO repositories (repo_name, repo_owner, full_name, repo_path, url, platform, " \
                      "stars_count) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_data, (repo_name, repo_owner, full_name, repo_path, url, platform, stars_count))
        conn.commit()
        repo_id = cursor.lastrowid  # 새로 추가된 저장소의 ID 가져오기
        cursor.close()
        return repo_id
    except pymysql.Error as e:
        print(f"Error inserting data into 'repositories': {e}")
        return None


# 'repo_version' 테이블에 데이터 삽입
def insert_repo_version_data(conn, repo_id, version_name, tag_name, dir_path):
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        insert_data = "INSERT INTO repo_version (repo_id, version_name, tag_name, dir_path) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_data, (repo_id, version_name, tag_name, dir_path))
        conn.commit()
        version_id = cursor.lastrowid  # 새로 추가된 버전의 ID 가져오기
        cursor.close()
        return version_id
    except pymysql.Error as e:
        print(f"Error inserting data into 'repo_version': {e}")
        return None


# 'functions' 테이블에 데이터 삽입
def insert_function_data(conn, repo_id, ver_id, function_name, return_types, param_types, param_count, file_name,
                         language_type):
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        insert_data = "INSERT INTO functions (repo_id, ver_id, function_name, return_types, param_types, " \
                      "param_count, file_name, language_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_data, (repo_id, ver_id, function_name, return_types, param_types, param_count,
                                     file_name, language_type))
        conn.commit()
        function_id = cursor.lastrowid  # 새로 추가된 함수의 ID 가져오기
        cursor.close()
        return function_id
    except pymysql.Error as e:
        print(f"Error inserting data into 'functions': {e}")
        return None


# 'repo_name'과 'repo_owner'에 따라 'repositories' 테이블에서 데이터 찾기
def find_repository_by_name_and_owner(conn, repo_name, repo_owner):
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        select_query = "SELECT * FROM repositories WHERE repo_name = %s AND repo_owner = %s"
        cursor.execute(select_query, (repo_name, repo_owner))
        repository_data = cursor.fetchone()
        cursor.close()
        return repository_data
    except pymysql.Error as e:
        print(f"Error fetching data from 'repositories': {e}")
        return None


# 파라미터에 따라 'functions' 테이블에서 데이터 찾기
def find_function_by_params(conn, repo_id, ver_id, function_name, return_types, param_types, param_count, file_name,
                            language_type):
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        select_query = "SELECT * FROM functions WHERE repo_id = %s AND ver_id = %s AND function_name = %s AND " \
                       "return_types = %s AND param_types = %s AND param_count = %s AND file_name = %s AND " \
                       "language_type = %s"
        cursor.execute(select_query, (repo_id, ver_id, function_name, return_types, param_types, param_count, file_name,
                                      language_type))
        function_data = cursor.fetchone()
        cursor.close()
        return function_data
    except pymysql.Error as e:
        print(f"Error fetching data from 'functions': {e}")
        return None


# 'repo_id'와 'version_name'에 따라 'repo_version' 테이블에서 데이터 찾기
def find_repo_version_by_name_and_repo_id(conn, repo_id, version_name, tag_name):
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        select_query = "SELECT * FROM repo_version WHERE repo_id = %s AND version_name = %s AND tag_name = %s"
        cursor.execute(select_query, (repo_id, version_name, tag_name))
        version_data = cursor.fetchone()
        cursor.close()
        return version_data
    except pymysql.Error as e:
        print(f"Error fetching data from 'repo_version': {e}")
        return None


def insert_data_to_database(data):
    # 데이터베이스에 연결
    conn = connect_to_database()

    # Repository, Version 및 Function 데이터 추출
    repo_data = data['repository']
    version_data = data['version']
    functions_data = data['functions']

    # Repository 정보 추출
    if repo_data['repo_name']:
        repo_name = repo_data['repo_name']
        repo_owner = repo_data['repo_owner']
        full_name = repo_data['full_name']
        repo_path = repo_data['repo_path']
        url = repo_data['url']
        platform = repo_data['platform']
        stars_count = repo_data['stars_count']

        # Repository가 이미 존재하는지 확인
        repo = find_repository_by_name_and_owner(conn, repo_name, repo_owner)

        if repo:
            repo_id = repo[0]
            print(f"Repository '{repo_name}' by '{repo_owner}' already exists in the database.")
        else:
            # 존재하지 않는 경우 Repository 정보 삽입
            repo_id = insert_repository_data(conn, repo_name, repo_owner, full_name, repo_path, url, platform,
                                             stars_count)
            print(f"Added repository '{repo_name}' by '{repo_owner}' to the database.")

        # Version 데이터 확인
        if version_data:
            version_name = version_data['version_name']
            tag_name = version_data['tag_name']
            dir_path = version_data['dir_path']

            # Version이 이미 존재하는지 확인
            ver = find_repo_version_by_name_and_repo_id(conn, repo_id, version_name, tag_name)

            if ver:
                ver_id = ver[1]
                print(f"Version '{version_name}' and Tag '{tag_name}' for repository '{repo_name}' by '{repo_owner}' "
                      f"already exists in the database.")
            else:
                # 존재하지 않는 경우 Version 정보 삽입
                ver_id = insert_repo_version_data(conn, repo_id, version_name, tag_name, dir_path)
                print(f"Added version '{version_name}' Tag '{tag_name}' for repository '{repo_name}' by '{repo_owner}' "
                      f"to the database.")

            # Function 데이터 처리
            for functions in functions_data:
                file_name = functions['file_name']
                language_type = functions['language_type']

                # 함수 정보 삽입
                for func in functions['functions']:
                    function_name = func['function_name']
                    return_types = func['return_types']
                    param_types = func['param_types']
                    param_count = func['param_count']

                    if not find_function_by_params(conn, repo_id, ver_id, function_name, return_types, param_types,
                                                   param_count, file_name, language_type):
                        insert_function_data(conn, repo_id, ver_id, function_name, return_types, param_types,
                                             param_count, file_name, language_type)
                        print(
                            f"Added function '{function_name}' to version '{version_name}' Tag '{tag_name}' for "
                            f"repository '{repo_name}' by '{repo_owner}'.")

            # 데이터베이스 연결 종료
            conn.close()
        else:
            # Version 정보가 없는 경우 데이터베이스 연결 종료
            conn.close()
    else:
        # Repository 정보가 없는 경우 데이터베이스 연결 종료
        conn.close()


if __name__ == "__main__":
    conn = connect_to_database()
    repo = find_repository_by_name_and_owner(conn, 'gnutls', 'gnutls')
    conn.close()
    print(repo)


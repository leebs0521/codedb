import pymysql
import json


def connect_to_database():
    db_config = {
        "host": "",
        "user": "",
        "password": "",
        "database": "",
        "charset": ""
    }

    try:
        conn = pymysql.connect(**db_config)
        return conn
    except pymysql.Error as e:
        print(f"Database connection error: {e}")
        return None


# Insert data into 'repositories' table
def insert_repository_data(conn, repo_name, repo_owner, full_name, repo_path, url, platform, stars_count):
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        insert_data = "INSERT INTO repositories (repo_name, repo_owner, full_name, repo_path, url, platform, " \
                      "stars_count) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_data, (repo_name, repo_owner, full_name, repo_path, url, platform, stars_count))
        conn.commit()
        repo_id = cursor.lastrowid  # Get the ID of the newly added repo
        cursor.close()
        return repo_id
    except pymysql.Error as e:
        print(f"Error inserting data into 'repositories': {e}")
        return None


# Insert data into 'repo_version' table
def insert_repo_version_data(conn, repo_id, version_name, tag_name, dir_path):
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        insert_data = "INSERT INTO repo_version (repo_id, version_name, tag_name, dir_path) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_data, (repo_id, version_name, tag_name, dir_path))
        conn.commit()
        version_id = cursor.lastrowid  # Get the ID of the newly added version
        cursor.close()
        return version_id
    except pymysql.Error as e:
        print(f"Error inserting data into 'repo_version': {e}")
        return None


# Insert data into 'functions' table
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
        function_id = cursor.lastrowid  # Get the ID of the newly added function
        cursor.close()
        return function_id
    except pymysql.Error as e:
        print(f"Error inserting data into 'functions': {e}")
        return None


# Find a repository by name and owner
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


# Find a function by parameters
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


# Find a repo version by name and repo_id
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
    conn = connect_to_database()

    repo_data = data['repository']
    version_data = data['version']
    functions_data = data['functions']

    if repo_data['repo_name']:
        repo_name = repo_data['repo_name']
        repo_owner = repo_data['repo_owner']
        full_name = repo_data['full_name']
        repo_path = repo_data['repo_path']
        url = repo_data['url']
        platform = repo_data['platform']
        stars_count = repo_data['stars_count']

        repo = find_repository_by_name_and_owner(conn, repo_name, repo_owner)

        if repo:
            repo_id = repo[0]
            print(f"Repository '{repo_name}' by '{repo_owner}' already exists in the database.")
        else:
            repo_id = insert_repository_data(conn, repo_name, repo_owner, full_name, repo_path, url, platform,
                                             stars_count)
            print(f"Added repository '{repo_name}' by '{repo_owner}' to the database.")

        if version_data:
            version_name = version_data['version_name']
            tag_name = version_data['tag_name']
            dir_path = version_data['dir_path']

            ver = find_repo_version_by_name_and_repo_id(conn, repo_id, version_name, tag_name)

            if ver:
                ver_id = ver[1]
                print(f"Version '{version_name}' and Tag '{tag_name}' for repository '{repo_name}' by '{repo_owner}' "
                      f"already exists in the database.")
            else:
                ver_id = insert_repo_version_data(conn, repo_id, version_name, tag_name, dir_path)
                print(f"Added version '{version_name}' Tag '{tag_name}' for repository '{repo_name}' by '{repo_owner}' "
                      f"to the database.")

            for functions in functions_data:
                file_name = functions['file_name']
                language_type = functions['language_type']
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

            conn.close()
        else:
            conn.close()
    else:
        conn.close()


def main():
    path = '/home/lbs/codedb/results/golang.org_x_crypto/v0.0.0-20190308221718-c2843e01d9a2.json'

    with open(path, 'r') as json_file:
        json_data = json.load(json_file)

    #insert_data_to_database(json_data)


if __name__ == "__main__":
    #main()
    conn = connect_to_database()
    repo = find_repository_by_name_and_owner(conn, 'gnutls', 'gnutls')
    if repo:
        print(1)
    else:
        print(2)
    conn.close()
    print(repo)


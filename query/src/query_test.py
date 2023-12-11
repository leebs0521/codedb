import os, re
from collections import defaultdict

# 소스 코드 유형에 대한 파일 확장자 및 키워드 정의
SOURCE_CODE_EXTENSIONS = {
    'go': ['.go'],
    'c': ['.c', '.C'],
    'cpp': ['.cc', '.cpp', '.CPP', '.c++', '.cp', '.cxx', '.h'],
    'swift': ['.swift'],
    'objective-c': ['.m']
}

# 각 언어에 대한 쿼리 파일 경로 정의
QUERY_FILE = {
    'c': '/home/lbs/codedb/query/c.scm',
    'cpp': '/home/lbs/codedb/query/cpp.scm',
    'go': '/home/lbs/codedb/query/go.scm',
    'swift': '/home/lbs/codedb/query/swift.scm',
    'objective-c': '/home/lbs/codedb/query/obj.scm'
}

# Tree-sitter 실행 파일 경로 정의
CUSTOM_TREE_SITTER = '/home/lbs/tree-sitter/target/release/tree-sitter'


# 파일이 소스 코드 파일이며 해당 유형인지 확인하는 함수
def is_source_code_file(file_path):
    _, file_extension = os.path.splitext(file_path)

    # 각 언어에 대한 확장자 확인
    for code_type, extensions in SOURCE_CODE_EXTENSIONS.items():
        if file_extension in extensions:
            return True, code_type

    # 소스 코드 파일이 아닌 경우
    return False, None


# 언어에 따라 코드를 파싱하는 함수
def parse_code_by_language(file_path, language):
    # 언어에 해당하는 쿼리 파일 경로 및 실행 명령어 설정
    query_file_path = QUERY_FILE[language]
    parse_command = f'{CUSTOM_TREE_SITTER} query {query_file_path} {file_path} > result.txt'

    # Tree-sitter를 사용하여 코드 파싱 실행
    os.system(parse_command)

    # 결과 파일 열기 및 내용 읽기
    with open('./result.txt') as result_file:
        file_contents = result_file.read()

    # 추출된 함수 정보 반환
    return extract_function_info(file_contents, language)


# 코드에서 함수 정보를 추출하는 함수
def extract_function_info(file_contents, language):
    functions = []

    # 각 패턴을 정리하여 함수 정보 추출
    patterns = [pattern.strip() for pattern in re.split(r'\s*pattern: \d+\s*', file_contents) if pattern.strip()]

    for pattern in patterns:
        # 각 패턴에서 키와 값을 추출
        keys = re.findall(r'-\s*(.*?)\s*,', pattern)
        values = re.findall(r'`([^`]+)`', pattern)

        # 중복된 키를 처리하기 위해 defaultdict 사용
        merged_dict = defaultdict(list)
        for key, value in zip(keys, values):
            merged_dict[key].append(value)
        result_dict = {key: ', '.join(val) for key, val in merged_dict.items()}

        # 파라미터 리스트 정리 및 파라미터 수 계산
        return_types = re.sub(r'[()]', '', result_dict.get('return_type', ''))

        if language == 'objective-c':
            param_list = re.sub(r'\n\s*', ' ', result_dict.get('param_list', ''))
            parameters_count = len(param_list.split(',')) if param_list else 0

        else:
            param_list = re.sub(r'\n\s*', ' ', re.sub(r'[()]', '', result_dict.get('param_list', '')))
            parameters_count = len(param_list.split(',')) if param_list else 0

        # 결과 딕셔너리 생성
        if result_dict:
            functions.append({
                'function_name': result_dict.get('func_name'),
                'return_types': return_types,
                'param_types': param_list,
                'param_count': parameters_count
            })

    return functions


if __name__ == "__main__":

    file_path = '/home/lbs/codedb/query/test/test.swift'
    funcs = parse_code_by_language(file_path, 'swift')

    for func in funcs:
        print(f"function_name: {func['function_name']}")
        print(f"return_types: {func['return_types']}")
        print(f"param_types: {func['param_types']}")
        print(f"param_count: {func['param_count']}")
        print()


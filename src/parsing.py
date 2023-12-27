import os, json

from parsing_util import is_source_code_file, parse_code_by_language


# 소스코드 파일로부터 함수를 추출하는 함수
def extract_functions_from_file(file_path, language, identifier):
    functions = None

    # 지원하는 언어 목록
    support_language_list = ('c', 'cpp', 'go', 'swift', 'objective-c')

    # 언어가 지원 목록에 있는 경우 코드 파싱
    if language in support_language_list:
        functions = parse_code_by_language(file_path, language, identifier)
    else:
        # 지원하지 않는 언어인 경우 메시지 출력
        print(f"{file_path}: Not supported language: {language}")

    return functions


# 디렉토리를 처리하고 소스 코드 파일에서 함수를 추출하는 함수
def process_directory(directory_path, identifier):
    function_data = {"data": []}

    for root, _, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # 디렉토리 경로를 기준으로 상대 경로 설정
            path = file_path.replace(directory_path + '/', '')

            # 소스 코드 파일 여부 및 언어 확인
            is_source_code, language = is_source_code_file(file_path)
            if is_source_code:
                
                # 파일에서 함수 추출
                extracted_functions = extract_functions_from_file(file_path, language, identifier.replace("/", "_"))
                if extracted_functions:
                    function_data['data'].append(
                        {"file_name": path, "language_type": language, "functions": extracted_functions})

    return function_data


if __name__ == "__main__":
    repository_dir = "/home/lbs/codedb/target/stretchr_testify/v1.8.4"
    file_functions = process_directory(repository_dir, 'a')
    output_file = 'test.json'
    
    with open(output_file, 'w') as json_file:
        json.dump(file_functions, json_file, indent=4)

    print(f"Function information saved to {output_file}")

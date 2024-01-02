# codedb
 - OSS 수집(Using Github REST API)
 - Tree-sitter 기반 함수 정보(함수 명, 리턴 타입, 파라미터 등) 추출 및 DB 저장

## 지원 언어
 - c
 - cpp
 - go
 - objective-c
 - go

 ## 준비물
 - python 3.8.0
 - tree-sitter 0.20.8 [[install link]](https://github.com/leebs0521/tree-sitter)


 ## Directory tree
 ```shell
 /home/lbs/codedb
├── query
│   // Tree-sitter 언어별 쿼리 파일이 존재하는 디렉토리
│   ├── cpp.scm
│   ├── c.scm
│   ├── go.scm
│   ├── obj.scm
│   ├── swift.scm
├── results
│   // 레포지토리 별 함수 추출 결과가 저장되는 디렉토리
│	...
├── src
│   // OSS 수집 및 함수 추출에 필요한 소스코드가 존재하는 디렉토리
│   ├── info
│   ├── __init__.py
│   ├── db_utils.py
│   ├── github_repo_downloader.py
│   ├── indiviual_process.py
│   ├── insert_data.py
│   ├── main.py
│   ├── parsing.py
│   ├── parsing_util.py
│   ├── repo_loader.py
│   ├── repo_tag_downloader.py
│   └── utils.py
├── target
│   // 수집한 레포지토리 저장 위치
│   ...
└── temp
│   // tree-sitter 결과 임시 저장 디렉토리
│   ...
└──
 ```

## results target temp 폴더 생성
```shell
cd tree-sitter
mkdir results target temp
```
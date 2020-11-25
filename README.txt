# sboard 소스코드 활용정보

## 점프투플라스크와 다른점
- 프로젝트 이름 pybo를 main으로 변경
- Question과 Answer를 Post와 Reply로 변경
- 비밀번호 암호화는 bcrypt를 사용
- DBMS는 mariadb를 사용
- 로그인과정은 로그인, 로그인사용자 확인, 로그아웃으로 구분하여 커밋

## 기본환경
- 리눅스(wsl2)
- docker에 마리아디비
- 가상환경 패키지 설치(requitements.txt 참고)
- 마리아디비 연결을 위한 패키지(mariadb) 설치방법은 https://tinyurl.com/y2mxrkc5 참고
- bootatrap 버전 4.5.3

## 처음 시작하는 경우

1. 파이썬 가상환경 구축
- 위 기본환경 참고

2. 도커에 mariadb 설치
- WSL2에서 Docker 원격 컨테이너 시작 https://tinyurl.com/y4yw6535
- 마리아디비 연결을 위한 패키지(mariadb) 설치방법은 https://tinyurl.com/y2mxrkc5 참고

$ docker run --name sboard-db -e MYSQL_ROOT_PASSWORD=qwer1234 -p 3306:3306 -d mariadb:latest

3. 데이터베이스 설정
- sboard_db를 사용하기 위해 db에 sboard_db 데이터베이스 생성

$ . setEnv
$ flask db init
$ flask db migrate
$ flask db upgrade


## 프로젝트 실행
$ . setEnv.sh
$ flask run

## 우분투에서 sqlite3를 사용
- https://www.sitepoint.com/getting-started-sqlite3-basic-commands/
- http://manpages.ubuntu.com/manpages/focal/man1/sqlite3.1.html

### 데이터베이스 확인
> .databases
테이블 확인
> .tables
스키마 확인

### mariadb의 db connector는 mysql을 사용

$ pip install pymysql
$ SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user00:qwer1234@localhost:3306/sboard_db'

### 오류처리

#### migrate와 upgrade
[문제] sqlite3 사용 후 db를 변경하면 migrate시 아래와 같은 에러가 발생함.
ERROR [root] Error: Target database is not up to date.

[해결] https://tinyurl.com/y5wo3dlm
$ flask db stamp head
$ flask db migrate
$ flask db upgrade

참고. db 버전을 alembic_version 테이블에 저장

#### 모델에서 Comment를 Reply로 명칭 변경하기
먼저 텍스트 검색을 통해 Comment를 Reply로, comment를 reply로 변경
comment_voews.py를 reply.py로 변경

flask db migrate와 upgrade를 진행

[문제] 프로젝트를 git애서 받아 새로 진행하는 경우 migrations가 비어 있어 아래 오류발생
ERROR [root] Error: Can't locate revision identified by '71cede82a39e'

[해결] https://tinyurl.com/yy944pyc
지금 디비에 있는 alembic_versions테이블을 삭제하고 초기화부터 다시 진행하면 됨.

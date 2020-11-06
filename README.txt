# sboard 소스코드 활용정보

## 프로젝트 환경설정을 아래와 같이 먼저 실행한다.
$ . setEnv.sh

플라스크 실행
$ flask run

## 우분투에서 sqlite3를 사용하려면
https://www.sitepoint.com/getting-started-sqlite3-basic-commands/
http://manpages.ubuntu.com/manpages/focal/man1/sqlite3.1.html

## 데이터베이스 확인
> .databases
테이블 확인
> .tables
스키마 확인

## sqlite3에서 mariadb(도커위에)로 변경
### 도커에 mariadb 설치
docker pull mariadb
docker run --name sboard-db -e MYSQL_ROOT_PASSWORD=qwer1234 -p 3306:3306 -d mariadb:latest

### user00 사용자 추가 및 sboard_db 작업권한 부여

### mariadb의 db connector는 mysql을 사용
pip install pymysql
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user00:qwer1234@localhost:3306/sboard_db'

### migrate와 upgrade
[문제] sqlite3 사용 후 db를 변경하면 migrate시 아래와 같은 에러가 발생함.
ERROR [root] Error: Target database is not up to date.
[해결] https://tinyurl.com/y5wo3dlm
flask db stamp head
flask db migrate
flask db upgrade

참고. db 버전을 alembic_version 테이블에 저장
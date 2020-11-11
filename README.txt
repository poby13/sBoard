# sboard 소스코드 활용정보

## 점프투플라스크와 다른점
- 프로젝트 이름 pybo를 main으로 변경
- Question과 Answer를 Post와 Comment로 변경
- 비밀번호 암호화는 bcrypt를 사용
- DBMS는 mariadb를 사용

## 기본환경
- 리눅스(wsl2)
- docker에 마리아디비
- 가상환경 패키지 설치(requitements.txt 참고)
- 마리아디비 연결을 위한 패키지(mariadb) 설치방법은 https://tinyurl.com/y2mxrkc5 참고
- bootatrap 버전 4.5.3

## 처음 시작하는 경우
- 데이터베이스명 sboard_db
- db에 sboard_db 데이터베이스 생성

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

## sqlite3에서 mariadb(도커위에)로 데이터베이스 변경

### 도커에 mariadb 설치
- 마리아디비 연결을 위한 패키지(mariadb) 설치방법은 https://tinyurl.com/y2mxrkc5 참고

$ docker pull mariadb
$ docker run --name sboard-db -e MYSQL_ROOT_PASSWORD=qwer1234 -p 3306:3306 -d mariadb:latest

### user00 사용자 추가 및 sboard_db 작업권한 부여

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


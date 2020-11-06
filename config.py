import os

BASE_DIR = os.path.dirname(__file__)

# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'sboard.db'))
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:qwer1234@localhost:3306/sboard_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False # 이벤트들을 처리하기 위한 옵션, 추가적인 메모리를 사용, 게시판에는 필요없는 기능으로 비활성화
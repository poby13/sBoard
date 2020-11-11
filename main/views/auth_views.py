from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from main import db
from main.forms import UserCreateForm, UserLoginForm
from main.models import User

import bcrypt

bp = Blueprint('auth', __name__, url_prefix='/auth')

# 내부함수
def _pwhash(str):
    # 해시코드 https://tinyurl.com/yb3bq6c6
    hashed = bcrypt.hashpw(str.encode('utf-8'), bcrypt.gensalt(14))
    # 언제나 길이가 60인 해시코드를 반환한다.
    # print('='*15, len(hashed), '='*15)
    # decode하는 경우 타입에러가 발생한다. 바이너리로 인코딩된 상태로 전달하면 된다.
    # return hashed.decode() # 쿼리문으로 직업 입력하는 경우 디코딩이 필요함.
    return hashed

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        # 쿼리 결과가 여러개인 경우 첫번째 레코드를 반환한다. one()은 결과 값이 한 개인 경우 사용한다. 여러개이면 예외가 발생한다.
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        # password=generate_password_hash(form.password1.data),
                        password=_pwhash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        # elif not check_password_hash(user.password, form.password.data):
        elif not bcrypt.checkpw(form.password.data.encode('utf-8'), user.password):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)
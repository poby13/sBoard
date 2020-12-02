from flask import Blueprint, url_for, request, render_template, g, flash
from main.models import Post, Reply, User, post_voter
from main.views.auth_views import login_required
from ..forms import PostForm, ReplyForm
from .. import db
from sqlalchemy import func
from werkzeug.utils import redirect
from datetime import datetime

bp = Blueprint('post', __name__, url_prefix='/post')

@bp.route('/list/')
def _list():
    # 입력 파라미터
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')

    # 정렬
    if so == 'recommend':
        sub_query = db.session.query(post_voter.c.post_id, func.count('*').label('num_voter')).group_by(post_voter.c.post_id).subquery()
        post_list = Post.query.outerjoin(sub_query, Post.id == sub_query.c.post_id).order_by(sub_query.c.num_voter.desc(), Post.create_date.desc())
    elif so == 'popular':
        sub_query = db.session.query(Reply.post_id, func.count('*').label('num_reply')).group_by(Reply.post_id).subquery()
        post_list = Post.query.outerjoin(sub_query, Post.id == sub_query.c.post_id).order_by(sub_query.c.num_reply.desc(), Post.create_date.desc())
    else:  # recent
        post_list = Post.query.order_by(Post.create_date.desc())

    # 조회
    # post_list = Post.query.order_by(Post.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Reply.post_id, Reply.content, User.username).join(User, Reply.user_id == User.id).subquery()
        post_list = post_list.join(User).outerjoin(sub_query, sub_query.c.post_id == Post.id).filter(Post.subject.ilike(search) | 
                    Post.content.ilike(search) |  
                    User.username.ilike(search) | 
                    sub_query.c.content.ilike(search) |  
                    sub_query.c.username.ilike(search)).distinct()

    # 페이징
    post_list = post_list.paginate(page, per_page=10)
    return render_template('post/post_list.html', post_list=post_list, page=page, kw=kw)

@bp.route('/detail/<int:post_id>/')
def detail(post_id):
    form = ReplyForm()
    post = Post.query.get_or_404(post_id)
    return render_template('post/post_detail.html', post=post, form=form)

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create(): # 새글 추가시 post_id가 필요없음
    form = PostForm()
    # breakpoint()
    if request.method == 'POST' and form.validate_on_submit():
        post = Post(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('post/post_form.html', form=form)

@bp.route('/modify/<int:post_id>', methods=('GET', 'POST'))
@login_required
def modify(post_id):
    post = Post.query.get_or_404(post_id)
    if g.user != post.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('post.detail', post_id=post_id))
    if request.method == 'POST':
        # POST 요청이면 수정 후 상세보기로 이동
        form = PostForm()
        # 필수사항(DataRequired)과 같이 POST로 전송된 폼 데이터의 정합성을 체크
        if form.validate_on_submit():
            # form으로 전달받은 데이터를 post 객체에 적용
            form.populate_obj(post)
            post.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('post.detail', post_id=post_id))
    else:
        # 수정양식을 보여준다.
        form = PostForm(obj=post)
    return render_template('post/post_form.html', form=form)

@bp.route('/delete/<int:post_id>')
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if g.user != post.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('post.detail', post_id=post_id))
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('post._list'))
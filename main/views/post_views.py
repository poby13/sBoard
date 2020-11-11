from flask import Blueprint, url_for, request, render_template, g
from main.models import Post
from main.views.auth_views import login_required
from ..forms import PostForm, CommentForm
from .. import db
from werkzeug.utils import redirect
from datetime import datetime

bp = Blueprint('post', __name__, url_prefix='/post')

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    post_list = Post.query.order_by(Post.create_date.desc())
    post_list = post_list.paginate(page, per_page=10)
    return render_template('post/post_list.html', post_list=post_list)

@bp.route('/detail/<int:post_id>/')
def detail(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    return render_template('post/post_detail.html', post=post, form=form)

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = PostForm()
    # breakpoint()
    if request.method == 'POST' and form.validate_on_submit():
        post = Post(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('post/post_form.html', form=form)

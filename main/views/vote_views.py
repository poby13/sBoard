from flask import Blueprint, url_for, flash, g
from werkzeug.utils import redirect

from main import db
from main.models import Post, Reply
from main.views.auth_views import login_required

bp = Blueprint('vote', __name__, url_prefix='/vote')


@bp.route('/post/<int:post_id>/')
@login_required
def post(post_id):
    _post = Post.query.get_or_404(post_id)
    if g.user == _post.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _post.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('post.detail', post_id=post_id))

@bp.route('/reply/<int:reply_id>/')
@login_required
def reply(reply_id):
    _reply = Reply.query.get_or_404(reply_id)
    if g.user == _reply.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _reply.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('post.detail', post_id=_reply.post.id))
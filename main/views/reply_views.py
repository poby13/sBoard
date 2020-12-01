from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from main import db
from main.models import Post, Reply
from main.views.auth_views import login_required

from ..forms import ReplyForm

bp = Blueprint('reply', __name__, url_prefix='/reply')

@bp.route('/create/<int:post_id>', methods=('POST',))
@login_required
def create(post_id):
    form = ReplyForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        content = request.form['content']
        reply = Reply(content=content, create_date=datetime.now(), user=g.user)
        post.reply_set.append(reply)
        db.session.commit()
        return redirect('{}#reply_{}'.format(url_for('post.detail', post_id=post_id), reply.id))
    return render_template('post/post_detail.html', post=post, form=form)

@bp.route('/modify/<int:reply_id>', methods=('GET', 'POST'))
@login_required
def modify(reply_id):
    reply = Reply.query.get_or_404(reply_id)
    if g.user != reply.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('post.detail', post_id=reply.post.id))
    if request.method == "POST":
        form = ReplyForm()
        if form.validate_on_submit():
            form.populate_obj(reply)
            reply.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#reply_{}'.format(url_for('post.detail', post_id=post_id), reply.id))
    else:
        form = ReplyForm(obj=reply)
    return render_template('reply/reply_form.html', reply=reply, form=form)

@bp.route('/delete/<int:reply_id>')
@login_required
def delete(reply_id):
    reply = Reply.query.get_or_404(reply_id)
    post_id = reply.post.id
    if g.user != reply.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(reply)
        db.session.commit()
    return redirect(url_for('post.detail', post_id=post_id))
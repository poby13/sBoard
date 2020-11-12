from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from main import db
from main.models import Post, Comment
from main.views.auth_views import login_required

from ..forms import CommentForm

bp = Blueprint('comment', __name__, url_prefix='/comment')

@bp.route('/create/<int:post_id>', methods=('POST',))
@login_required
def create(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        content = request.form['content']
        comment = Comment(content=content, create_date=datetime.now(), user=g.user)
        post.comment_set.append(comment)
        db.session.commit()
        return redirect(url_for('post.detail', post_id=post_id))
    return render_template('post/post_detail.html', post=post, form=form)

@bp.route('/modify/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def modify(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if g.user != comment.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('post.detail', post_id=comment.post.id))
    if request.method == "POST":
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('post.detail', post_id=comment.post.id))
    else:
        form = CommentForm(obj=comment)
    return render_template('comment/comment_form.html', comment=comment, form=form)

@bp.route('/delete/<int:comment_id>')
@login_required
def delete(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post.id
    if g.user != comment.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('post.detail', post_id=post_id))
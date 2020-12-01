from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from main import db
from main.forms import CommentForm
from main.models import Post, Comment, Reply
from main.views.auth_views import login_required

bp = Blueprint('comment', __name__, url_prefix='/comment')


@bp.route('/create/post/<int:post_id>', methods=('GET', 'POST'))
@login_required
def create_post(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST' and form.validate_on_submit():
        comment = Comment(user=g.user, content=form.content.data, create_date=datetime.now(), post=post)
        db.session.add(comment)
        db.session.commit()
        return redirect('{}#comment_{}'.format(url_for('post.detail', post_id=post_id), comment.id))
    return render_template('comment/comment_form.html', form=form)

@bp.route('/modify/post/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def modify_post(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if g.user != comment.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('post.detail', post_id=comment.post.id))
    if request.method == 'POST':
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#comment_{}'.format(url_for('post.detail', post_id=comment.post.id), comment.id))
    else:
        form = CommentForm(obj=comment)
    return render_template('comment/comment_form.html', form=form)

@bp.route('/delete/post/<int:comment_id>')
@login_required
def delete_post(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post.id
    if g.user != comment.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('post.detail', post_id=post_id))
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('post.detail', post_id=post_id))


@bp.route('/create/reply/<int:reply_id>', methods=('GET', 'POST'))
@login_required
def create_reply(reply_id):
    form = CommentForm()
    reply = Reply.query.get_or_404(reply_id)
    if request.method == 'POST' and form.validate_on_submit():
        comment = Comment(user=g.user, content=form.content.data, create_date=datetime.now(), reply=reply)
        db.session.add(comment)
        db.session.commit()
        return redirect('{}#comment_{}'.format(url_for('post.detail', post_id=reply.post.id), comment.id))
    return render_template('comment/comment_form.html', form=form)

@bp.route('/modify/reply/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def modify_reply(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if g.user != comment.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('post.detail', post_id=comment.reply.id))
    if request.method == 'POST':
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#comment_{}'.format(url_for('post.detail', post_id=comment.reply.post.id), comment.id))
    else:
        form = CommentForm(obj=comment)
    return render_template('comment/comment_form.html', form=form)


@bp.route('/delete/reply/<int:comment_id>')
@login_required
def delete_reply(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.reply.post.id
    if g.user != comment.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('post.detail', post_id=post_id))
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('post.detail', post_id=post_id))
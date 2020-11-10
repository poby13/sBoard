from datetime import datetime

from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect

from main import db
from main.models import Post, Comment

from ..forms import CommentForm

bp = Blueprint('comment', __name__, url_prefix='/comment')

@bp.route('/create/<int:post_id>', methods=('POST',))
def create(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        content = request.form['content']
        comment = Comment(content=content, create_date=datetime.now())
        post.comment_set.append(comment)
        db.session.commit()
        return redirect(url_for('post.detail', post_id=post_id))
    return render_template('post/post_detail.html', post=post, form=form)
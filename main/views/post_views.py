from flask import Blueprint, render_template
from main.models import Post

bp = Blueprint('post', __name__, url_prefix='/post')

@bp.route('/list/')
def _list():
    post_list = Post.query.order_by(Post.create_date.desc())
    return render_template('post/post_list.html', post_list=post_list)

@bp.route('/detail/<int:post_id>/')
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post/post_detail.html', post=post)
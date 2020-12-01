from main import db
import mariadb

# '다대다 관계' 테이블을 먼저 작성해 주어야 한다.
post_voter = db.Table(
    'post_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), primary_key=True)
)

reply_voter = db.Table(
    'reply_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('reply_id', db.Integer, db.ForeignKey('reply.id', ondelete='CASCADE'), primary_key=True)
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    # user 속성은 Post모델에서 계정모델(User)을 참조하기 위해서 추가된 속성으로 post.user.username과 같이 사용된다.
    user = db.relationship('User', backref=db.backref('post_set'))
    voter = db.relationship('User', secondary=post_voter, backref=db.backref('post_voter_set'))

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'))
    post = db.relationship('Post', backref=db.backref('reply_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('reply_set'))
    voter = db.relationship('User', secondary=reply_voter, backref=db.backref('reply_voter_set'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.BLOB(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=True)
    post = db.relationship('Post', backref=db.backref('comment_set'))
    reply_id = db.Column(db.Integer, db.ForeignKey('reply.id', ondelete='CASCADE'), nullable=True)
    reply = db.relationship('Reply', backref=db.backref('comment_set'))


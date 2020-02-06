from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

rdb = SQLAlchemy()
ma = Marshmallow()

class PRModel(rdb.Model):
    """
    Pull Request Model
    """
    __tablename__ = 'pull_requests'

    dbid = rdb.Column(rdb.Integer, primary_key = True, unique = True)#, serial = True)
    id = rdb.Column(rdb.Integer)
    num = rdb.Column(rdb.Integer)
    repo = rdb.Column(rdb.String(255))
    pr_diff_url = rdb.Column(rdb.String(255))
    created_at = rdb.Column(rdb.DateTime)
    closed_at = rdb.Column(rdb.DateTime)
    additions = rdb.Column(rdb.Integer)
    changed_files = rdb.Column(rdb.Integer)
    commits = rdb.Column(rdb.Integer)
    deletions = rdb.Column(rdb.Integer)
    merged = rdb.Column(rdb.Boolean)
    num_reviews_requested = rdb.Column(rdb.Integer)
    num_review_comments = rdb.Column(rdb.Integer)

    def __init__(self, data):
        self.id = data.get('id')
        self.num = data.get('num')
        self.repo = data.get('repo')
        self.pr_diff_url = data.get('pr_diff_url')
        self.created_at = data.get('created_at')
        self.closed_at = data.get('closed_at')
        self.additions = data.get('additions')
        self.changed_files = data.get('changed_files')
        self.commits = data.get('commits')
        self.deletions = data.get('deletions')
        self.merged = data.get('merged')
        self.num_reviews_requested = data.get('num_reviews_requested')
        self.num_review_comments = data.get('num_review_comments')

    @staticmethod
    def all_prs():
        return PRModel.query.all()
        
    @staticmethod
    def get_pr_by_id(id):
        return PRModel.query.filter_by(id=id).all()

    @staticmethod
    def get_pr_by_repo(repo):
        return PRModel.query.filter_by(repo=repo).all()


class PRSchema(ma.ModelSchema):
    class Meta:
        model = PRModel

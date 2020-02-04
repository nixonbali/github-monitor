import faust

## github user
class Actor(faust.Record, serializer='json'):
    login: str
    #url: str

# github repo
class Repo(faust.Record, serializer='json'):
    id: int
    name: str
    #url: str

class DetailedRepo(faust.Record, serializer='json'):
    id: int
    name: str
    language: str

# pull request head
class Head(faust.Record, serializer='json'):
    repo: DetailedRepo
    open_issues_count: int = None


# pull request
class PullRequest(faust.Record, serializer='json'):
    id: int # key
    number: int
    diff_url: str
    patch_url: str
    head: Head
    merged: str = None
    commits: int = None
    additions: int = None
    deletions: int = None
    changed_files: int = None
    mergeable: str = None
    mergeable_state: str = None

# pr review request payload
class PRReviewRequestPayload(faust.Record, serializer='json'):
    action: str

class Comment(faust.Record, serializer='json'):
    actor: Actor
    body: str
    created_at: str

# pr review comment payload
class PRReviewCommentPayload(faust.Record, serializer='json'):
    action: str
    comment: Comment

# pull request payload
class PRPayload(faust.Record, serializer='json'):
    action: str
    pull_request: PullRequest


# event
class PREvent(faust.Record, serializer='json'):
    id: str
    type: str
    actor: Actor
    created_at: str # format: "2016-06-05T18:01:26Z"]
    repo: Repo
    payload: PRPayload

class GeneralEvent(faust.Record, serializer='json'):
    actor: Actor
    repo: Repo
    created_at: str # format: "2016-06-05T18:01:26Z"
    type: str



#### PR LOGIC
# if PR event
# if PR Closed
# #

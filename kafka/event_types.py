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
    open_issues_count: int
    repo: DetailedRepo


# pull request
class PullRequest(faust.Record, serializer='json'):
    id: int # key
    merged: str
    diff_url: str
    patch_url: str
    commits: int
    additions: int
    deletions: int
    changed_files: int
    mergeable: str
    mergeable_state: str
    head: Head

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

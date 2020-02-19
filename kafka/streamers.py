import faust
import json
import secrets
from event_types import *
import aredis
from collab_graph import CollabGraph
from topic_names import git_events, pull_requests, collabs, closed_prs
from dateutil.parser import parse
from aiopg.sa import create_engine

"""App and Topic Initialization"""
app = faust.App('git-app', broker=secrets.BROKER1)
events_topic = app.topic(git_events)
pr_events_topic = app.topic(pull_requests, value_type=PREvent)
collab_topic = app.topic(collabs, value_type=GeneralEvent)
pr_closed_topic = app.topic(closed_prs)
pull_request_events = ["PullRequestEvent", "PullRequestReviewEvent", "PullRequestReviewCommentEvent"]

@app.agent(events_topic)
async def process_event(events):
    """
    Events Streamer
    Orchestrates Event Delivery to PR and Graph Topics
    """
    async for event_json in events:
        ### Filter for PR Events and send through to PR Topic
        if (event_json['type'] in pull_request_events):
            await pr_events_topic.send(value=event_json)
        # write all events user + repo to new topic to gather user / repo info to build graph
        # read in event_json as new type
        await collab_topic.send(value=event_json)

@app.agent(pr_events_topic)
async def process_pr_events(pr_events):
    """
    PR Events Stream Processor
    Manages Pull Request Monitoring from Open to Close
    """
    async for pr_event in pr_events:
        client = aredis.StrictRedis(host='localhost', port=6379)
        await client.set(pr_event.payload.pull_request.id, pr_event.dumps()) # pr_event
        if pr_event.type == "PullRequestEvent":
           ### produce to closed pr topic
           if pr_event.payload.action == 'closed':
               await client.set(pr_event.payload.pull_request.id, pr_event.dumps())
               await pr_closed_topic.send(value=pr_event.payload.pull_request.id)
           ### store open time
           elif pr_event.payload.action == 'opened':
               await client.set(str(pr_event.payload.pull_request.id) + 'opentime', pr_event.created_at)
           ### all pr activity incrementer
           else:
               await client.incr(str(pr_event.payload.pull_request.id) + 'events')
        ### review incrementer
        elif pr_event.type == "PullRequestReviewEvent":
           await client.incr(str(pr_event.payload.pull_request.id) + 'reviews')


@app.agent(pr_closed_topic)
async def process_pr_closed(closed_pr_ids):
    """
    PR Closed Events Consumer
    Looks up PR Keys for Closed PR
    Moves Values from Redis to Postgres
    """
    async for pr_id in closed_pr_ids:
        ### Redis reads + processing
        client = aredis.StrictRedis(host='localhost', port=6379)
        opentime = await client.get(str(pr_id) + 'opentime')
        if opentime is not None:
            opentime = parse(opentime)
        num_events = await client.get(str(pr_id) + 'events')
        if num_events:
            num_events = int(num_events)
        num_review = await client.get(str(pr_id) + 'reviews')
        if num_review:
            num_review = int(num_review)
        close_event = await client.get(pr_id)
        close_event = json.loads(close_event)
        closetime = parse(close_event['created_at'])
        ### postgres writes
        async with create_engine(user='gituser', database='gitdb', host=secrets.POSTGRES_BROKER) as engine:
            async with engine.acquire() as conn:
                await conn.execute(
                "insert into pull_requests (id,num,repo,pr_diff_url,created_at,closed_at,additions,changed_files,commits,deletions,merged,num_reviews_requested,num_review_comments) values (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    (pr_id, 0,
                                    close_event['repo']['name'],
                                    close_event['payload']['pull_request']['diff_url'],
                                    opentime, closetime,
                                    close_event['payload']['pull_request']['additions'],
                                    close_event['payload']['pull_request']['changed_files'],
                                    close_event['payload']['pull_request']['commits'],
                                    close_event['payload']['pull_request']['deletions'],
                                    close_event['payload']['pull_request']['merged'],
                                    num_review, num_events))




if __name__ == "__main__":
    """Initialize Topics and Run Faust"""
    app.main()

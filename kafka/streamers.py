import faust
import json
import secrets
from event_types import *
import aredis
from collab_graph import CollabGraph
from topic_names import git_events, pull_requests, collabs, closed_prs
from dateutil.parser import parse
from aiopg.sa import create_engine

app = faust.App('git-app', broker=secrets.BROKER1)

events_topic = app.topic(git_events)
pr_events_topic = app.topic(pull_requests, value_type=PREvent)
collab_topic = app.topic(collabs, value_type=GeneralEvent)
pr_closed_topic = app.topic(closed_prs)

pull_request_events = ["PullRequestEvent", "PullRequestReviewEvent", "PullRequestReviewCommentEvent"]

### Events Streamer
@app.agent(events_topic)
async def process_event(events):
    async for event_json in events:
        #event_json = json.loads(event)
        ### Filter for PR Events and send through to PR Topic
        if (event_json['type'] in pull_request_events):
            await pr_events_topic.send(value=event_json)
        # write all events user + repo to new topic to gather user / repo info to build graph
        # read in event_json as new type
        await collab_topic.send(value=event_json)

### PR Events Stream Processor
@app.agent(pr_events_topic)
async def process_pr_events(pr_events):
   async for pr_event in pr_events:
       #print(pr_event)
       #pr_event = json.loads(pr_event)
       client = aredis.StrictRedis(host='localhost', port=6379)
       await client.set(pr_event.payload.pull_request.id, pr_event.dumps()) # pr_event

       if pr_event.type == "PullRequestEvent":
           if pr_event.payload.action == 'closed':
               #pr_len = await client.llen(pr_event.payload.pull_request.id)
               #full_pr = await client.lrange(pr_event.payload.pull_request.id, 0, pr_len)
               await client.set(pr_event.payload.pull_request.id, pr_event.dumps())
               await pr_closed_topic.send(value=pr_event.payload.pull_request.id)
               #print(full_pr)
           elif pr_event.payload.action == 'opened':
               await client.set(str(pr_event.payload.pull_request.id) + 'opentime', pr_event.created_at)
           else:
               await client.incr(str(pr_event.payload.pull_request.id) + 'events')

       elif pr_event.type == "PullRequestReviewEvent":
           await client.incr(str(pr_event.payload.pull_request.id) + 'reviews')

       # pr_event.type == "PullRequestReviewCommentEvent"
       # else:
       #     async with create_engine(user='ubuntu', database='first_db', host='127.0.0.1', password='ubuntu') as engine:
       #         async with engine.acquire() as conn:
       #             await conn.execute(tbl.insert().values(id=1,name='testpr',repo='testrepo'))




## PR Closed Events (redis->processing->postgres)
@app.agent(pr_closed_topic)
async def process_pr_closed(closed_pr_ids):
    async for pr_id in closed_pr_ids:
        client = aredis.StrictRedis(host='localhost', port=6379)
        #pr_len = await client.llen(pr_id.value)
        #full_pr = await client.lrange(pr_id.value, 0, pr_len)

        opentime = await client.get(str(pr_id) + 'opentime')
        if opentime is not None:
            opentime = parse(opentime)
            # print("HERE")
        num_events = await client.get(str(pr_id) + 'events')
        if num_events:
            num_events = int(num_events)
        num_review = await client.get(str(pr_id) + 'reviews')
        if num_review:
            num_review = int(num_review)


        close_event = await client.get(pr_id)
        close_event = json.loads(close_event)
        closetime = parse(close_event['created_at'])
        #print(close_event)
        ###



        async with create_engine(user='gituser', database='gitdb', host=secrets.POSTGRES_BROKER) as engine:
            async with engine.acquire() as conn:
                #await conn.execute("insert into testtable (num, repo) values (%s, %s)",
                #                    (pr_id, close_event['repo']['name']))

                await conn.execute(
                "insert into pullrequests (id,num,repo,pr_diff_url,created_at,closed_at,additions,changed_files,commits,deletions,merged,num_reviews_requested,num_review_comments) values (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    (pr_id, 0,#close_event['payload']['number'],
                                    close_event['repo']['name'], close_event['payload']['pull_request']['diff_url'],
                                    opentime, closetime, close_event['payload']['pull_request']['additions'],
                                    close_event['payload']['pull_request']['changed_files'],
                                    close_event['payload']['pull_request']['commits'],
                                    close_event['payload']['pull_request']['deletions'],
                                    close_event['payload']['pull_request']['merged'],
                                    num_review, num_events))



       #await client.zadd(activity.user, activity.timestamp, activity.message)
       # if pr closed
       # cache.get -> metrics -> produce to new topic
       # else
       # cache.set


if __name__ == "__main__":
    app.main()

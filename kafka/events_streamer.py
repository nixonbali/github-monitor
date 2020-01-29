import faust
import json
import secrets
from event_types import *
import aredis
from collab_graph import CollabGraph

app = faust.App('git-app', broker=secrets.BROKER1)

events_topic = app.topic("git-events")
pr_events_topic = app.topic("pr-events", value_type=PREvent)
collab_topic = app.topic("collab", value_type=GeneralEvent)
pr_closed_topic = app.topic("pr-closed")

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
       await client.rpush(pr_event.payload.pull_request.id, pr_event)
       if pr_event.payload.action == 'closed':
           pr_len = await client.llen(pr_event.payload.pull_request.id)
           full_pr = await client.lrange(pr_event.payload.pull_request.id, 0, pr_len)
           await pr_closed_topic.send(value=full_pr)
           #print(full_pr)


       #await client.zadd(activity.user, activity.timestamp, activity.message)
       # if pr closed
       # cache.get -> metrics -> produce to new topic
       # else
       # cache.set


if __name__ == "__main__":
    app.main()

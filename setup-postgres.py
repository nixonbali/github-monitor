import psycopg2
from secrets import POSTGRES_BROKER

def create_pr_table():
    """Single Use Script for Creating Pull Request Table in Postgres"""
    conn = psycopg2.connect("dbname=gitdb user=gituser password=gituser host={}".format(POSTGRES_BROKER))
    cur = conn.cursor()
    #cur.execute("drop table pull_requests")
    cur.execute("""create table pull_requests (
      dbid serial primary key unique,
      id integer,
      num integer,
      repo varchar(255),
      pr_diff_url varchar(255),
      created_at timestamp,
      closed_at timestamp,
      additions integer,
      changed_files integer,
      commits integer,
      deletions integer,
      merged boolean,
      num_reviews_requested integer,
      num_review_comments integer
    );""")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_pr_table()

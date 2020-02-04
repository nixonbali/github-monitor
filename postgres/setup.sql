drop table pullrequests;

create table pullrequests (
  id integer primary key unique,
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
)

-- create table comments (
--   id integer primary key unique,
--   pull_request_id integer,
--   user varchar(255),
--   body text,
--   created_at timestamp
-- )

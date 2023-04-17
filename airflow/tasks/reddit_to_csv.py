import configparser
import datetime
import pandas as pd
import pathlib
import praw
import sys
import numpy as np

# aws and reddit credentials from the configuration.conf file are used as variables

config_file = "configuration.conf"
parser = configparser.ConfigParser()
path = pathlib.Path(__file__).parent.resolve()
output_name = sys.argv[1]

parser.read(f"{path}/{config_file}")

secret = parser.get("reddit_config", "secret")
clientid = parser.get("reddit_config", "client_id")

# PRAW parameters

subreddit = "bapcsalescanada"
filter = "day"
lim = None


columns = (
    "id",
    "title",
    "score",
    "num_comments",
    "author",
    "created_utc",
    "url",
    "upvote_ratio"
)

def main():
    reddit_instance = api_connect()
    subreddit_posts_object = subreddit_posts(reddit_instance)
    extracted_data = extract_data(subreddit_posts_object)
    transformed_data = transform(extracted_data)
    save_csv(transformed_data)


def api_connect():
    instance = praw.Reddit(
            client_id=clientid, client_secret=secret, user_agent="My User Agent"
        )
    return instance

def subreddit_posts(reddit_instance):
    sub = reddit_instance.subreddit(subreddit)
    posts = sub.top(time_filter=filter, limit=lim)
    return posts

def extract_data(posts):
    list_of_items = []
    for submission in posts:
        to_dict = vars(submission)
        sub_dict = {field: to_dict[field] for field in columns}
        list_of_items.append(sub_dict)
        extracted_data_df = pd.DataFrame(list_of_items)
    return extracted_data_df

def extract_part(string):
    # no [meta] - return none
    # has no bracket to start - return none
    # has bracket but is not a pc part - leave it
    if string[0] != '[' or string.lower()[0:6] == '[meta]':
        return None
    else:
        part = string[string.find('[')+1 : string.find(']')].upper()
        return part

def extract_seller(string):
    part = string[string.find('//')+2 : string.find('//')+2+string[string.find('//')+2:].find('/')]
    if part[0:4] == 'www.':
        part = part[4:]
    return part 

def transform(df):
    df = df.loc[~df['url'].str.contains('reddit')]
    df['part'] = df['title'].apply(extract_part)
    df['seller'] = df['url'].apply(extract_seller)
    df["created_utc"] = pd.to_datetime(df["created_utc"], unit="s")
    return df

def save_csv(df):
    df.to_csv(f"/tmp/{output_name}.csv", index=False)

if __name__ == "__main__":
    main()

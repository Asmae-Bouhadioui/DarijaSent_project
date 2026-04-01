import snscrape.modules.twitter as sntwitter
import pandas as pd
import time

query = "zwin lang:ar"

tweets = []
limit = 100  # you can increase later

for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i >= limit:
        break

    if tweet.content:
        tweets.append([tweet.date, tweet.content])

    time.sleep(1)  # avoid blocking

df = pd.DataFrame(tweets, columns=["date", "text"])
df.to_csv("darija_tweets.csv", index=False, encoding="utf-8-sig")

print("Collected:", len(df))
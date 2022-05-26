import argparse
import sys
from pathlib import Path

import tweepy
import yaml

parser = argparse.ArgumentParser()
parser.add_argument(
    "--key_file", type=str, default=str(Path(__file__).parent.joinpath("keys.yaml"))
)

COUNT = 200


def confirmation_loop():
    while True:
        confirmed = input(
            "Are you sure you want to permanantly wipe your public Twitter presence? This includes all tweets, retweets, and favorites. (y/n): "
        )
        if confirmed.lower() == "y":
            break
        elif confirmed.lower() == "n":
            sys.exit()


def main(args):
    confirmation_loop()

    with open(args.key_file, "r") as f:
        keys = yaml.safe_load(f)
        assert {
            "consumer_key",
            "consumer_secret",
            "access_token",
            "access_token_secret",
        }.issubset(keys.keys())

    auth = tweepy.OAuth1UserHandler(
        consumer_key=keys["consumer_key"],
        consumer_secret=keys["consumer_secret"],
        access_token=keys["access_token"],
        access_token_secret=keys["access_token_secret"],
    )
    api = tweepy.API(auth, wait_on_rate_limit=True)

    def destroy_status_wrapper(id):
        try:
            api.destroy_status(id)
        except:
            api.unretweet(id)
        finally:
            pass

    def destroy_favorite_wrapper(id):
        try:
            api.destroy_favorite(id)
        except:
            pass

    destroyed_tweets, destroyed_favorites = 0, 0
    requests = 0
    while True:
        user_tweets = api.user_timeline(
            count=COUNT, exclude_replies=False, include_rts=True
        )
        user_favorites = api.get_favorites(count=COUNT)

        if len(user_tweets) == 0 and len(user_favorites) == 0:
            break

        [destroy_status_wrapper(tweet.id) for tweet in user_tweets]
        [destroy_favorite_wrapper(favorite.id) for favorite in user_favorites]

        destroyed_tweets += len(user_tweets)
        destroyed_favorites += len(user_favorites)
        requests += 1

        print(f"Requests: {requests}", end="\r")

    print(f"Destroyed tweets: {destroyed_tweets}")
    print(f"Destroyed favorites: {destroyed_favorites}")


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)

"""
Retrieve tweets, embeddings, and persist the database.
"""

import tweepy
from decouple import config
import basilica
from .models import DB, Tweet, User

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASILICA_KEY'))


def add_or_update_user(username):
    """Add or update a user and their tweets, error if no/private user"""
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id, name=username))
        DB.session.add(db_user)
        # we want as many recent non-retweets/replies as we can get
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False,
            tweet_mode='extended', since_id=db_user.newest_tweet_id)
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            # get embedding for tweet and store in db
            embedding = BASILICA.embed_sentence(tweet.full_text,
                                                model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500],
                             embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e
    else:
        DB.session.commit()


def add_users(users):
    """
    Add/update a list of users (strings of user names).
    May take awhile, so run "offline" (interactive shell).
    """
    for user in users:
        add_or_update_user(user)


def update_all_users():
    """Update all Tweets for all Users in the User table."""
    for user in User.query.all():
        add_or_update_user(user.name)


# TODO write some functions
# twitter_user = TWITTER.get_user('austen')
# tweets = twitter_user.timeline(count=200, exclude_replies=True,
#                                include_rts=False, tweet_mode='extended')
# db_user = User(id=twitter_user.id, name=twitter_user.screen_name,
#                newest_tweet_id=tweets[0].id)
# db_tweets = []
# for tweet in tweets:
#     embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
#     db_tweet = Tweet(
#         id=tweet.id, text=tweet.full_text[:500], embedding=embedding)
#     DB.session.add(db_tweet)
#     db_user.tweets.append(db_tweet)


# >>> twitter_user = TWITTER.get_user('austen')
# >>> tweets = tweets=twitter_user.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode='extended')
# >>> db_user=User(id=twitter_user.id, name=twitter_user.screen_name, newest_tweet_id=tweets[0].id)
# >>> embeddings = [BASILICA.embed_sentence(tweet.full_text, model='twitter') for tweet in tweets]
# >>> #db_tweets = [Twitter(id=tweet.id, text=tweet.full_text[:500], embedding=
# >>> db_tweets = []
# >>> for embedding, tweet in zip(embeddings, tweets):
# ...     db_tweets.append(Tweet(id=tweet.id, text=tweet.full_text[:500], embedding=embedding))
# ...
# >>> db_tweets[0]
# <Tweet I always snarkily ask late-stage CEOs when they’re going public.

#  Sid is the only one who ever responded with a hopeful date.

# I respect so much the way that company is run. https://t.co/ZrsdGmkVy4>
# >>> db_tweets[0].id
# 1173956097754980354
# >>> db_tweets[0].embeddings
# Traceback (most recent call last):
#   File "<console>", line 1, in <module>
# AttributeError: 'Tweet' object has no attribute 'embeddings'
# >>> db_tweets[0].embedding

# >>> for tweet in tweets:
# ...     embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
# ...     db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500], embedding=embedding)
# ...     twitter.user.tweets.append(db_tweet)
# ...     DB.session.add(db_tweet)
# ...
# Traceback (most recent call last):
#   File "<console>", line 4, in <module>
# NameError: name 'twitter' is not defined
# >>> for tweet in tweets:
# ...     embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
# ...     db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500], embedding=embedding)
# ...     DB.session.add(db_tweet)
# ...     db_user.tweets.append(db_tweet)
# ...
# >>> DB.session.add(db_user)
# >>> DB.sesion.commit()
# Traceback (most recent call last):
#   File "<console>", line 1, in <module>
# AttributeError: 'SQLAlchemy' object has no attribute 'sesion'
# >>> DB.session.commit()
# >>>
# KeyboardInterrupt
# >>>
# >>>
# now exiting InteractiveConsole...

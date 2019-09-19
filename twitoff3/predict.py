"""
Prediction of Users based on tweet embeddings.
"""

#import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import BASILICA


# future code to use with caches and pickle
# def predict_user(user1_name, user2_name, tweet_text, cache=None):
#     """Determine and return which user is more likely to write a given
#     tweet text."""
#     if cache and cache.exists(user_set):
#         log_reg = pickle.loads(cache.get(user_set))
#     else:
#         user1 = User.query.filter(User.name == user1_name).one()
#         user2 = User.query.filter(User.name == user2_name).one()
#         user1_embeddings = np.array(
#             [tweet.embeddings for tweet in user1.tweets])
#         user2_embeddings = np.array(
#             [tweet.embeddings for tweet in user2.tweets])
#         embeddings = np.vstack([user1_embeddings, user2_embeddings])
#         labels = np.concatenate([np.ones(len(user1.tweets)),
#                                  np.zeros(len(user2.tweets))])
#         log_reg = LogisticRegression().fit(embeddings, labels)
#         cache and cache.set(user_set, pickle.dumps(log_reg))
#     tweet_embeddings = BASILICA.embed_sentences(tweet_text, model='twitter')
#     return log_reg.predict(np.array(tweet_embeddings).reshape(1, -1))


def predict_user(user1_name, user2_name, tweet_text):
    """Determine and return which user is more likely to write a given 
    tweet text."""
    user1 = User.query.filter(User.name == user1_name).one()
    user2 = User.query.filter(User.name == user2_name).one()
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])
    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    labels = np.concatenate([np.ones(len(user1.tweets)),
                             np.zeros(len(user2.tweets))])
    log_reg = LogisticRegression().fit(embeddings, labels)
    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')

    return log_reg.predict(np.array(tweet_embedding).reshape(1, -1))

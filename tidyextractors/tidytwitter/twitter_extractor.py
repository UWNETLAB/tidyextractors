import tqdm
import nltk
import types
import tweepy
import pandas as pd
from tweepy import OAuthHandler
from tidyextractors import BaseExtractor
from nltk.tokenize import TweetTokenizer
from tidyextractors.tidytwitter.twitter_object_handlers import twitter_object_handlers_lookup


class TwitterExtractor(BaseExtractor):

    def __sub_init__(self, source, *args, **kwargs):
        """
        Subclass initialization routine which runs after BaseExtractor initialization.
        Mutates get_tidy lookup table.
        NOTE: TwitterExtractor requires a complete set of Twitter API credentials
        to initialize: 'access_token', 'access_secret', 'consumer_key', and 'consumer_secret'.

        :param source: A list of user screen names.
        :param args: Arbitrary arguments for extensibility.
        :param kwargs: Arbitrary keyword arguments for extensibility.
        :return: None
        """
        # Populate lookup table:
        self._add_lookup('users', self.users)
        self._add_lookup('tweets', self.tweets)

        # Add lazy short form lookup table:
        self._add_lookup('u', self.users)
        self._add_lookup('t', self.tweets)

    def _extract(self, source, extract_tweets=True, *args, **kwargs):
        """
        Extracts user data Using the twitter API. Mutates _data.
        NOTE: TwitterExtractor requires a complete set of Twitter API credentials
        to initialize: 'access_token', 'access_secret', 'consumer_key', and 'consumer_secret'.

        :param source: A list of user screen names.
        :param args: Arbitrary arguments for extensibility.
        :param kwargs: Arbitrary keyword arguments for extensibility.
        :return: None
        """
        # Check that the proper API keywords were provided.
        for cred in ['access_token', 'access_secret', 'consumer_key', 'consumer_secret']:
            if cred not in kwargs:
                raise ValueError('API credentials missing from keyword arguments: {}'.format(cred))

        # Set up API access
        self._auth = OAuthHandler(kwargs['consumer_key'], kwargs['consumer_secret'])
        self._auth.set_access_token(kwargs['access_token'],kwargs['access_secret'])
        self._api = tweepy.API(self._auth)

        # Make row dictionaries and count tweets
        rows = []
        num_tweets = 0
        pbar1 = tqdm.tqdm(range(0,len(source)))
        pbar1.set_description('Extracting user data...')
        for u in source:
            r = self._make_user_dict(u)
            num_tweets = num_tweets + min(r['statuses_count'], 3200)
            rows.append(r)
            pbar1.update(1)

        if extract_tweets:
            # Extract tweets
            pbar2 = tqdm.tqdm(range(0,num_tweets))
            for r in rows:
                if r['statuses_count'] > 0:
                    r['tweets'] = self._get_user_tweets(r['screen_name'])
                else:
                    r['tweets'] = []
                pbar2.set_description('Extracted tweets by {}'.format(r['screen_name']))
                pbar2.update(r['statuses_count'])

        self._data = pd.DataFrame.from_records(rows)

    def users(self):
        """
        Returns a table of Twitter user data, with "users" as rows/observations.

        :return: pandas.DataFrame
        """
        return self._data

    def tweets(self):
        """
        Returns a table of Twitter user data, with "tweets" as rows/observations.

        :return: pandas.DataFrame
        """

        # I've hard coded these. Seemed like a good idea at the time...
        # TODO: Fix this.
        all_columns = ['contributors_enabled', 'created_at', 'default_profile',
                       'default_profile_image', 'description', 'entities', 'favourites_count',
                       'follow_request_sent', 'followers_count', 'following', 'friends_count',
                       'geo_enabled', 'has_extended_profile', 'id_str',
                       'is_translation_enabled', 'is_translator', 'lang', 'listed_count',
                       'location', 'name', 'needs_phone_verification', 'notifications',
                       'profile_background_color', 'profile_background_image_url',
                       'profile_background_image_url_https', 'profile_background_tile',
                       'profile_banner_url', 'profile_image_url', 'profile_image_url_https',
                       'profile_link_color', 'profile_location',
                       'profile_sidebar_border_color', 'profile_sidebar_fill_color',
                       'profile_text_color', 'profile_use_background_image', 'protected',
                       'screen_name', 'statuses_count', 'suspended', 'time_zone',
                       'translator_type', 'url', 'utc_offset', 'verified', 'tweets/created',
                       'tweets/retweet', 'tweets/rt author', 'tweets/text']

        keep_columns = ['id_str', 'lang', 'location', 'name',
                        'protected', 'screen_name','time_zone',
                        'utc_offset', 'tweets/created', 'tweets/retweet',
                        'tweets/rt author', 'tweets/text']

        drop_columns = list(set(all_columns).difference(set(keep_columns)))

        return self.expand_on('id', 'tweets', ['id','tweet_id'], rename1='id', rename2='tweet_id', drop=drop_columns)

    def _handle_object(self, name, obj):
        """
        Process an object using twitter_object_handlers_lookup.
        Doesn't currently do anything (as of 2017-06-16).

        :param name: String
        :param obj: An object to be processed
        :return: A dictionary of attributes
        """
        if type(obj) in twitter_object_handlers_lookup:
            return twitter_object_handlers_lookup[type(obj)](name, obj)
        else:
            return {name: obj}

    def _make_object_dict(self, obj):
        """
        Processes an object, exporting its data as a nested dictionary.

        :param obj: An object
        :return: A nested dictionary of object data
        """
        data = {}
        for attr in dir(obj):
            if attr[0] is not '_' and attr is not 'status':
                datum = getattr(obj, attr)
                if not isinstance(datum, types.MethodType):
                    data.update(self._handle_object(attr,datum))
        return data

    def _make_user_dict(self, username):
        """
        Processes a Twitter User object, exporting as a nested dictionary.
        Complex values (i.e. objects that aren't int, bool, float, str, or
        a collection of such) are converted to strings (i.e. using __str__
        or __repr__). To access user data only, use make_user_dict(username)['_json'].

        :param username: A Twitter username string.
        :return: A nested dictionary of user data.
        """
        user = self._api.get_user(username)
        return self._make_object_dict(user)

    def _get_user_tweets(self, screen_name):

        # TODO: Implement tweet limit

        # Twitter only allows access to a users most recent 3240 tweets with this method

        # initialize a list to hold all the tweepy Tweets
        alltweets = []

        # make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = self._api.user_timeline(screen_name = screen_name,count=200)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        # keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:

            # all subsequent requests use the max_id param to prevent duplicates
            new_tweets = self._api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

            # save most recent tweets
            alltweets.extend(new_tweets)

            # update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1

        # transform the tweepy tweets into a 2D array that will populate the csv
        outtweets = {tweet.id_str: {'created':tweet.created_at,'text':tweet.text} for tweet in alltweets}

        # Twitter-aware tokenizer
        tknzr = TweetTokenizer()

        # Extend data with linguistic processing
        for tweet_id in outtweets:

            # Get tweet data from dictionary
            tweet = outtweets[tweet_id]

            # Lowercase tokenized tweet text
            tweet_tokens = tknzr.tokenize(tweet['text'])

            # Parts-of-speech tags for tokenized text
            tweet_pos = nltk.pos_tag(tweet_tokens)

            # Is the tweet a rewteet?
            tweet['retweet'] = tweet_pos[0][0] == 'RT'

            # If retweeted, who was the original author?

            if tweet['retweet'] is True:
                tweet['rt_author'] = tweet_pos[1][0]
            else:
                tweet['rt_author'] = ''

        return outtweets
        
# TODO: Might have encoding issues. See: https://stackoverflow.com/questions/6539881/python-converting-from-iso-8859-1-latin1-to-utf-8
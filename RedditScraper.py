import praw
class Scraper:
    def __init__(self):
        #Enter API info
        self.reddit = praw.Reddit(client_id='',client_secret='',username='',password='',user_agent='')
    
    #Gets 'hot' posts of a subreddit, can specify how many posts you want to retrieve
    def getHotPosts(self, subredditName, limit=25):
        #Max limit for api is 100
        if(limit > 100):
            limit = 100
        subreddit = self.reddit.subreddit(subredditName)
        hotPosts = subreddit.hot(limit=limit)
        list = []
        for submission in hotPosts:
            list.append(submission)
        return list
    
    #Gets 'top' posts of a subreddit, can specify time_filter and how many posts you want to retrieve
    def getTopPosts(self, subredditName, time_filter='all', limit=25):
        if(limit > 100):
            limit = 100
        subreddit = self.reddit.subreddit(subredditName)
        topPosts = subreddit.top(limit=limit,time_filter=time_filter)
        list = []
        for submission in topPosts:
            list.append(submission)
        return list
    
    #Gets a post via URL
    def getPostByURL(self, url):
        post = self.reddit.submission(url=url)
        return post
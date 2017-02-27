"""
    reddit.py - A simple REST that returns top or popular lists of reddit image content
"""

# Import the Python Reddit API praw
import praw
# Import flask and flask REST
from flask import Flask, jsonify
from flask_restful import Resource, Api

# Create flask instance and flask_restful instance
app = Flask(__name__)
api = Api(app)


def redditImageType(url):
    """
        redditImageType 
            input: url text
            return: True if its an image, False if not
            
        This function searches the url text to determine if its :
            An imgur asset
            One of the : PNG, JPG, JPEG, GIF (etc.)
            return True
            
        Else return False
        
    """
    # imageType
    imageType=['.jpg','.png','.jpeg','.gif','.gifv','.tiff','.bmp']
    # Check for imgur asset
    if url.find('imgur') != -1:
        return True
    # Find the last . to check for image extension types
    index = url.rfind('.')
    # Check that it was found
    if index != -1:
        # Iterate through the imageType
        for imageExt in imageType:
            if url[index:].find(imageExt) != -1:
                return True
    # Not an image return False
    return False
    
def searchReddit(reddit,search=None):
    """
        searchReddit
            Input:
                reddit - reddit instance
            Output:
                topReddit, popularReddit - list of dictionaries in order of 
                    topReddit - The order returned from 'top'
                    popularReddit - sorted based on 'score'
            Description:
                read through the top LIMIT hot entries
                find image assets
                if an entry is an image asset, append dictionary to topReddit
                sort the list based on each asset's score for popularReddit
    """
    topReddit=[]
    nbrPosts=0
    LIMIT = 200
    # Iterate through the reddit posts
    for post in reddit.subreddit(search).hot(limit=LIMIT):
        # convert to unicode
        redditUrl=unicode(post.url)
        if redditImageType(redditUrl):
            redditPost={}
            redditPost['title']=repr(post.title)
            redditPost['score']=int(post.score)
            redditPost['id']=str(post.id)
            redditPost['url']=redditUrl
            redditPost['nbr']=nbrPosts
            # Append the redditPost to the topReddit list
            topReddit.append(redditPost)
            nbrPosts+=1
    # Create popularReddit, sorted list using the score in reverse order to sort them
    popularReddit = sorted(topReddit, key=lambda item: item['score'], reverse=True)
    return topReddit, popularReddit

def getRedditInstance():
    """
        getRedditInstance
            Input:
                None
            Output:
                reddit instance
            Description:
                create a reddit instance 
    """
    reddit = praw.Reddit(client_id='MK-iwlSasTWGFA',
                         client_secret='vbZ_qAs5O_iJi5sx3VDUeV6glBY',
                         user_agent='flask testscript by /u/tdifilipo')
    #print repr(reddit)
    return reddit

# Create the reddit instance
reddit=getRedditInstance()

# Add a comment
class topRedditApi(Resource):
    """
        REST topRedditApi for resource /topReddit 
    """
    def get(self):
        topReddit, popularReddit = searchReddit(reddit,'all')
        return jsonify(topReddit)

class popularRedditApi(Resource):
    """
        popularRedditApi for resource /popularReddit 
    """
    def get(self):
        topReddit, popularReddit = searchReddit(reddit,'all')
        return jsonify(popularReddit)


# Set up the API resources, / /top returns the topReddit, /popular returns popularReddit
api.add_resource(topRedditApi, '/', '/top')
api.add_resource(popularRedditApi, '/popular')
api.add_resource(popularRedditApi, '/another_link')
# Run main, you run this by executing python reddit.py
if __name__ == '__main__':
    app.run(debug=True)

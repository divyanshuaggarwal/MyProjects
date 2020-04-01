import scripts.textcleaning as tc
from scripts.plot import create_plot
import pickle
import logging
import gensim
import praw
from praw.models import MoreComments
from zipfile import ZipFile 

# file_name = "model/random_forest_model.bin.zip"

# Use pickle to load in the pre-trained model
model = pickle.load(open('model/LR.pkl','rb'))


reddit = praw.Reddit(client_id = "JTqwrVU0MISDWg",
					client_secret = "xe06s55FgF5JDSHABI2AsnrX1Q0",
					user_agent = "reddit_scraper",
					username = "divyanshuggrwl",
					password = "wateringplants")

def prediction(url):
	submission = reddit.submission(url = url)
	data = {}
	data["title"] = str(submission.title)
	data["url"] = str(submission.url)
	data["body"] = str(submission.selftext)

	submission.comments.replace_more(limit=None)
	comment = ''
	count = 0
	for top_level_comment in submission.comments:
		comment = comment + ' ' + top_level_comment.body
		count+=1
		if(count > 10):
		 	break
		
	data["comment"] = str(comment)

	data['title'] = tc.clean_text(str(data['title']))
	data['body'] = tc.clean_text(str(data['body']))
	data['comment'] = tc.clean_text(str(data['comment']))
    
	combined_features = data["title"] + data["comment"] + data["body"] + data["url"]

	return model.predict([combined_features])


import flask
import pickle
import pandas as pd


# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')

# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('main.html'))
    
    if flask.request.method == 'POST':
        # Extract the input
        text = flask.request.form['url']
        
        # Get the model's prediction
        flair = prediction(str(text))
    
        # Render the form again, but add in the prediction and remind user
        # of the values they input before
        return flask.render_template('main.html', original_input={'url':str(text)}, result=flair,)
@app.route("/stats")
def stats():
	bar = create_plot()
	return flask.render_template('graph.html',plot=bar)


if __name__ == '__main__':
    app.run()
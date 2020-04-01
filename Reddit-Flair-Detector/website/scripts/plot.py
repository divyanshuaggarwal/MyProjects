import plotly
from plotly import graph_objs as go

import pandas as pd
import numpy as np
import json

flairs = ["AskIndia", "Non-Political", "[R]eddiquette", 
          "Scheduled", "Photography", "Science/Technology",
          "Politics", "Business/Finance", "Policy/Economy",
          "Sports", "Food", "AMA"]

posts = pd.read_csv('scripts/data.csv')

comments = posts.groupby(['flair'])['comms_num'].agg('sum')
upvotes = posts.groupby(['flair'])['score'].agg('sum')

raw_data = {
			'flair' : ["AskIndia", "Non-Political", "[R]eddiquette", "Scheduled", "Photography", "Science/Technology", "Politics", "Business/Finance", "Policy/Economy", "Sports", "Food", "AMA"],
			'comments' : comments,
			'upvotes' : upvotes				
			}

graph = pd.DataFrame(raw_data,columns=['flair','comments','upvotes'])

def create_plot():
    

    df = graph
    
    trace1 = go.Bar(
                x = flairs,
                y = graph.comments,
                name = "comments",
                marker = dict(color = 'rgba(255, 174, 255, 0.5)',
                             line=dict(color='rgb(0,0,0)',width=1.5)),
                )
    # create trace2 
    trace2 = go.Bar(
                    x = flairs,
                    y = graph.upvotes,
                    name = "upvotes",
                    marker = dict(color = 'rgba(255, 255, 128, 0.5)',
                                line=dict(color='rgb(0,0,0)',width=1.5)),
                    )

    data = [trace1,trace2]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
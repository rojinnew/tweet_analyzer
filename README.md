###Tweets Analyzer
<p align = "justify">
In this project,  Flask framework is used to deploy Twitter API, machine learning, and visualization libraries. A user enters a hashtag or a user and the application return relevant analysis.   
</p>
####Searching a Hashtag:
<p align = "justify">
When a user enters a hashtag in the search box(e.g. fridayfeeling) and clicks the search icon, the app fetches the most recent tweets, in this case, last 50000 tweets, and creates:
(1) A piechart diagram that shows the distribution of collected tweets across weekdays. 
 
(2) It detects the sentiment of the tweets and shows the distribution of collected tweets across weekdays is split based on various sentiments.
</p>
<p align = "center">
	<img src = "https://github.com/rojinnew/tweets_analyzer/blob/master/hashtag.png">
</p>
####Searching a User 
<p align = "justify">
When a user enters a hashtag in the search box (e.g. @username) and clicks the search icon, the app fetches the most recent tweets, in this case, last 90 tweets, and creates:
(1) A piechart diagram that shows the distribution of collected tweets across weekdays. 
</p>
<p align = "justify">
(2) A timeline for the number of retweets and the cumulative value.
</p>
 
<p align = "center">
	<img src = "https://github.com/rojinnew/tweets_analyzer/blob/master/user.png">
</p>
 
#### Running 
 
Create your account for a Twitter API and enter your credential in the credential.py file. Next, Install the required libraries listed in requirements.txt and start up the server in that src directory using the following command: 
 
python app.py 
 
http://localhost:5000/

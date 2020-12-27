"""
code for visulizing twitter hashtags and users using Flask framework
"""
from flask import Flask, render_template, request
from plot_hashtag import plot_grouped_barchart, plot_piechart
from hashtag import hash_tag_get_related_tweets
from twitter_user import get_related_tweets
from plot_user import plot_trend, plot_user_piechart

app = Flask(__name__)

def g_bar(keyword):
    """
    g_bar creates graphs
    keyword is the serached keyword
    """
    if keyword[0] == "#":
        _, _, tail = keyword.partition("#")
        new_graph_name1 = plot_grouped_barchart(tail)
        new_graph_name2 = plot_piechart(tail)
        return render_template("home.html", groupbar=new_graph_name1, piechart=new_graph_name2)
    if keyword[0] == "@":
        _, _, tail = keyword.partition('@')
        new_graph_name1 = plot_trend(tail)
        new_graph_name2 = plot_user_piechart(tail)
        return render_template("home.html", groupbar=new_graph_name1, piechart=new_graph_name2)

def request_results(keyword):
    """
    it fetches the reuslts using twitter api
    and save them in a csv file
    keyword is the serached keyword
    """

    #if os.path.exists('input.csv'):
    #    os.remove('input.csv')
    if keyword.startswith("#"):
        hash_tag_get_related_tweets(keyword)
    elif keyword.startswith("@"):
        get_related_tweets(keyword)

# Use the route() decorator to bind a function to a URL
@app.route('/')
def home():
    """
    render the homepage
    """
    return render_template('index.html')

@app.route('/', methods=['POST', 'GET'])
def get_data():
    """
    receive the seareched keyword by calling the associated function
    """
    if request.method == 'POST':
        keyword = request.form['search']
        if keyword[0] == "@":
            keyword = "@realdonaldtrump"
        elif keyword[0] == "#":
            keyword = "#fridayfeeling"
        render_template("home.html")
        return g_bar(keyword)

if __name__ == '__main__':
    app.run(debug=True)

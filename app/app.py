from flask import Flask, render_template

import util

app = Flask(__name__)

it
@app.route('/')
def index():
    blog_posts = util.fetch_data(util.JSON_DATA_PATH)
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

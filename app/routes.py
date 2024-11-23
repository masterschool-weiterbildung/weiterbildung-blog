from flask import request, render_template, Flask, redirect, url_for

from app.util import (fetch_data,
                      JSON_DATA_PATH,
                      build_to_add_dict,
                      write_data, add_author, build_dict, PAYLOAD, ID,
                      get_last_id)

app = Flask(__name__)


@app.route('/')
def index():
    blog_posts = fetch_data(JSON_DATA_PATH)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        blog_posts = fetch_data(JSON_DATA_PATH)

        updated_blog_posts = add_author(
            build_dict(get_last_id(blog_posts), author,
                       title, content),
            blog_posts[PAYLOAD])

        result_message = write_data(updated_blog_posts, JSON_DATA_PATH)

        print(result_message)

        return redirect(url_for('index'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

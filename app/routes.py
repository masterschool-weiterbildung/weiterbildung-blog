from flask import request, render_template, Flask, redirect, url_for

from app.util import (fetch_data,
                      JSON_DATA_PATH,
                      build_to_add_dict,
                      write_data, add_author, build_dict, PAYLOAD, ID,
                      get_last_id, delete_post, add_post)

app = Flask(__name__)


@app.route('/')
def index():
    blog_posts = fetch_data(JSON_DATA_PATH)
    return render_template('index.html', posts=blog_posts[PAYLOAD])


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        result_message = add_post(author, content, title)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    result_message = delete_post(post_id)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

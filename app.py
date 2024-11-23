from flask import request, render_template, Flask, redirect, url_for

from util import fetch_data, JSON_DATA_PATH, PAYLOAD, add_post, delete_post, \
    fetch_post_by_id, AUTHOR, TITLE, CONTENT, LIKE, update_post, get_like_id

app = Flask(__name__)


@app.route('/')
def index():
    blog_posts = fetch_data(JSON_DATA_PATH)[PAYLOAD]

    blog_posts = list(
        sorted(blog_posts, key=lambda x: x[TITLE], reverse=True))

    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_author = request.form.get("author")
        blog_title = request.form.get("title")
        blog_content = request.form.get("content")

        add_post(blog_author, blog_title, blog_content, 0)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    if post_id is None:
        # Post not found
        return "Post ID not found", 404

    delete_post(post_id)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    if post_id is None:
        # Post not found
        return "Post ID not found", 404

    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)

    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post in the JSON file
        blog_author = request.form.get(AUTHOR)
        blog_title = request.form.get(TITLE)
        blog_content = request.form.get(CONTENT)

        update_post(post_id, blog_author, blog_title, blog_content,
                    post[LIKE])

        # Redirect back to index
        return redirect(url_for('index'))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


@app.route('/like/<int:id>')
def like(id):
    if id is None:
        # Post not found
        return "Post ID not found", 404

    post = fetch_post_by_id(id)

    if post is None:
        # Post not found
        return "Post not found", 404

    update_post(id, post[AUTHOR], post[TITLE], post[CONTENT],
                get_like_id(post[LIKE]))

    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

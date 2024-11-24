from flask import request, render_template, Flask, redirect, url_for

from util import fetch_data, JSON_DATA_PATH, PAYLOAD, add_post, delete_post, \
    fetch_post_by_id, AUTHOR, TITLE, CONTENT, LIKE, update_post, get_like_id

"""
Blog Management Flask Application

This is a simple Flask application to manage blog posts. It supports 
the following features:
- Viewing a list of blog posts
- Adding a new blog post
- Updating an existing blog post
- Deleting a blog post
- Liking a blog post

Routes:
    /                   (GET) Displays a list of all blog posts, sorted in reverse 
                        alphabetical order by title.
    /add                (GET, POST) Handles adding a new blog post. Renders a form 
                        for input and processes form submissions.
    /delete/<int:post_id> (GET) Deletes a blog post with the given ID.
    /update/<int:post_id> (GET, POST) Updates the blog post with the given ID. 
                        Renders a form for editing and processes updates.
    /like/<int:id>      (GET) Adds a "like" to the blog post with the given ID.
    /404                Handles 404 errors and renders a custom "Page Not Found" page.
    /500                Handles 500 errors and renders a custom "Internal Server Error" page.

Templates:
    - `index.html`: Displays the list of blog posts.
    - `add.html`: Form for adding a new post.
    - `update.html`: Form for updating a post.
    - `404.html`: Custom 404 error page.
    - `500.html`: Custom 500 error page.
"""
app = Flask(__name__)


@app.route('/')
def index():
    """
    Homepage Route for Blog Posts

    Fetches all blog posts from the data.json and displays them on the homepage.
    The posts are sorted in reverse alphabetical order by their titles.

    Returns:
        str: Rendered HTML for the homepage, which includes the list of blog posts.

    Template:
        index.html: Expects a `posts` variable containing a list of blog post dictionaries.
    """
    blog_posts = fetch_data(JSON_DATA_PATH)[PAYLOAD]

    blog_posts = list(
        sorted(blog_posts, key=lambda x: x[TITLE], reverse=True))

    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Add a New Blog Post

    Handles adding a new blog post to the blog application. The route supports
    both GET and POST methods:
    - GET: Renders the form for creating a new blog post.
    - POST: Processes the form submission, adding the new post to the data source,
      and redirects to the homepage.

    Form Fields:
        - author (str): The name of the blog post's author.
        - title (str): The title of the blog post.
        - content (str): The content of the blog post.

    Returns:
        - Rendered HTML for the `add.html` page when accessed via GET.
        - Response: A redirect to the homepage (`index.html`) after successfully
                    adding a new blog post via POST.

    Template:
        add.html: Displays a form with fields for `author`, `title`, and `content`.
        index.html: Main page
    """
    if request.method == 'POST':
        blog_author = request.form.get("author")
        blog_title = request.form.get("title")
        blog_content = request.form.get("content")

        add_post(blog_author, blog_title, blog_content, 0)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """
     Delete a Blog Post

     Deletes a blog post identified by its unique `post_id`. If the `post_id`
     is invalid or the post does not exist, returns a 404 error.

     Parameter:
         post_id (int): The ID of the blog post to delete.

     Returns:
         - Response: A redirect to the homepage (`index.html`) after successfully
                     deleting the post.
         - A 404 error message and status code if the `post_id` is invalid
           or the post does not exist.

     Error Handling:
         - If `post_id` is `None` or the post is not found, a 404 error message
           is displayed.
     """
    if post_id is None:
        # Post not found
        return "Post ID not found", 404

    delete_post(post_id)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Update an Existing Blog Post

    Handles the updating of an existing blog post identified by its `post_id`.
    - GET: Displays a form pre-filled with the current details of the blog post.
    - POST: Processes the form submission, updating the blog post with new details.

    Parameter:
        post_id (int): The unique identifier of the blog post to update.

    Returns:
        - Rendered HTML for the `update.html` page (GET), pre-filled with the
          current post data.
        - Response: A redirect to the homepage (`index.html`) after
          successfully updating the post.
        - A 404 error message and status code if the `post_id` is invalid
          or the post does not exist.

    Form Fields (for POST):
        - AUTHOR (str): The updated author name of the blog post.
        - TITLE (str): The updated title of the blog post.
        - CONTENT (str): The updated content of the blog post.

    Template:
        update.html: Displays a form pre-filled with the current blog post details.
    """
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
    """
    Like a Blog Post

    Increments the like count for a blog post identified by its unique `id`. 
    If the post ID is invalid or the post does not exist, a 404 error is returned.

    Parameter:
        id (int): The unique identifier of the blog post to like.

    Returns:
        - A redirect to the homepage (`index.html`) after successfully incrementing
          the like count.
        - A 404 error message and status code if the `id` is invalid 
          or the post does not exist.

    Error Handling:
        - If the `id` is invalid or does not correspond to an existing post, 
          a 404 error message is displayed.
    """
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
    """
     Handle 404 Error (Page Not Found)

     Renders a custom 404 error page when a requested resource or route
     is not found.

     Parameter:
         The error object containing details about the 404 error.

     Returns:
         A rendered HTML response for the `404.html` template and the
         HTTP status code 404.

     Template:
         404.html: Custom template for the "Page Not Found" error.
     """
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(error):
    """
    Handle 500 Error (Internal Server Error)

    Renders a custom 500 error page when an internal server error occurs.

    Parameter:
        error (werkzeug.exceptions.InternalServerError): The error object
        containing details about the 500 error.

    Returns:
        A rendered HTML response for the `500.html` template and the
        HTTP status code 500.

    Template:
        500.html: Custom template for the "Internal Server Error" message.
    """
    return render_template('500.html'), 500


if __name__ == '__main__':
    """
    Run the Flask Application

    It starts the Flask development server on the specified host and port.

    Host:
        - "0.0.0.0": The application will be accessible from all available network 
          interfaces on the host machine.

    Port:
        - 5000: The port the server will listen on by default.
"""
    app.run(host="0.0.0.0", port=5000, debug=True)

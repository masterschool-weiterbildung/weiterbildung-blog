
# Blog Management Application

A simple Flask-based blog management application that allows users to:
- View all blog posts
- Add new blog posts
- Update existing blog posts
- Delete blog posts
- Like blog posts

---

## Features

- **Homepage**: Displays all blog posts sorted by title in descending order.
- **Add Post**: Create a new blog post with an author, title, and content.
- **Edit Post**: Modify the details of an existing blog post.
- **Delete Post**: Remove a blog post by its unique ID.
- **Like Post**: Increment the like count for a blog post.
- **Error Pages**: Custom error pages for 404 (not found) and 500 (server error).

---

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone git@github.com:masterschool-weiterbildung/weiterbildung-masterblog.git
   cd weiterbildung-masterblog
   ```

2. **Install dependencies**:
   Ensure you have Python installed, then run:
   ```bash
   pip install flask
   ```

3. **Set up the data**:
   - Add a JSON file for blog post storage (default: `JSON_DATA_PATH`).
   - The JSON file should follow this structure:
     ```json
       [
         {
           "id": 1,
           "author": "Author Name",
           "title": "Blog Title",
           "content": "Blog content goes here.",
           "like": 0
         }
       ]
     ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the app**:
   Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

---

## Project Structure

```
📂 Project Directory
├── 📂 templates       # HTML templates for Flask views
│   ├── index.html     # Homepage for listing posts
│   ├── add.html       # Form to add a new post
│   ├── update.html    # Form to edit an existing post
│   ├── 404.html       # Custom 404 error page
│   └── 500.html       # Custom 500 error page
├── 📂 static          # Static assets (CSS, JS, images, etc.)
├── app.py             # Main Flask application
├── util.py            # Utility functions for managing JSON data
├── constant_blog.py   # Constants used across the application
└── README.md          # Project documentation
```

---

## API Endpoints

| Route                | Method   | Description                                  |
|----------------------|----------|----------------------------------------------|
| `/`                  | GET      | View all blog posts                         |
| `/add`               | GET/POST | Add a new blog post                         |
| `/update/<post_id>`  | GET/POST | Update an existing blog post                |
| `/delete/<post_id>`  | GET      | Delete a blog post by ID                    |
| `/like/<post_id>`    | GET      | Increment the like count of a blog post     |

---

## Future Enhancements

- Add user authentication for managing posts.
- Implement search and filtering for blog posts.
- Improve the UI/UX with enhanced templates and design.
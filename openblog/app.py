import sqlite3
from datetime import datetime, timezone
from flask import Flask, render_template, request

app = Flask(__name__)
DATABASE = 'database.db'

@app.route("/", methods=["GET", "POST"])
def index():    
    if request.method == "POST":
        conn = sqlite3.connect(DATABASE)

        # Get form data
        name = request.form.get("name")
        title = request.form.get("title")
        content = request.form.get("content")

        timestamp = datetime.now(timezone.utc).isoformat()

        # Create a new post
        conn.execute(f"""INSERT INTO posts 
                        (name, title, content, timestamp) 
                        VALUES ("{name}", "{title}", "{content}", 
                        "{timestamp}")""")
        conn.commit()
        conn.close()

    conn = sqlite3.connect(DATABASE)
    # Retrieve posts from the database
    # Get all the rows from the table posts
    cursor = conn.execute("SELECT * FROM posts")

    # Headings are table column descriptions
    headings = [description[0] for description in cursor.description]

    # List of dictionaries representing table rows
    # Each row contains a blog post
    current_posts = [dict(zip(headings, row)) for row in cursor]
    conn.close()

    # Convert timestamps to a human-friendly format
    for post in current_posts:
        post["timestamp"] = (
            datetime.fromisoformat(post["timestamp"])
            .strftime("%B %d, %Y at %I:%M %p")
        )

    return render_template("blog.html", posts=current_posts)

if __name__ == "__main__":
    app.run(debug=True)

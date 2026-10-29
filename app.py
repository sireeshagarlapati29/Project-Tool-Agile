from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
# Secret key used for session-based flash messaging
app.secret_key = "agile-project-tool-secret-key"

# In-memory storage for projects created during the current application session
projects = []


@app.route("/")
def index():
    """Renders the main page displaying the project creation form and current session projects."""
    return render_template("index.html", projects=projects)


@app.route("/create-project", methods=["POST"])
def create_project():
    """Handles the creation of a new project with field validation."""
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    owner = request.form.get("owner", "").strip()

    # Validation: Ensure all fields are filled
    if not name or not description or not owner:
        flash("All fields (Project Name, Description, and Owner) are required.", "error")
        return redirect(url_for("index"))

    # Create new project record
    new_project = {
        "id": len(projects) + 1,
        "name": name,
        "description": description,
        "owner": owner,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    projects.append(new_project)

    flash(f"Project '{name}' was created successfully!", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Run the application locally on port 5000 as required
    app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "project-tool-agile-v1-secret"

@app.route("/")
def home():
    projects = session.get("projects", [])
    return render_template("index.html", projects=projects)


@app.route("/create-project", methods=["POST"])
def create_project():
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    owner = request.form.get("owner", "").strip()

    if not name or not description or not owner:
        flash("Please fill in all the fields.", "error")
        return redirect(url_for("home"))

    projects = session.get("projects", [])

    project = {
        "id": len(projects) + 1,
        "name": name,
        "description": description,
        "owner": owner
    }

    projects.append(project)
    session["projects"] = projects

    flash(f"Project '{name}' was created successfully!", "success")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
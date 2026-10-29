from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)

app.secret_key = "project-tool-agile-v1-secret"


@app.route("/")
def home():
    projects = session.get("projects", [])
    tasks = session.get("tasks", [])

    return render_template(
        "index.html",
        projects=projects,
        tasks=tasks
    )


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


# V2: Add Task / Assign Task
@app.route("/assign-task", methods=["POST"])
def assign_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    assigned_to = request.form.get("assigned_to", "").strip()
    project_id = request.form.get("project_id", "").strip()

    if not title or not description or not assigned_to or not project_id:
        flash("Please fill in all task fields.", "error")
        return redirect(url_for("home"))

    projects = session.get("projects", [])

    selected_project = next(
        (project for project in projects
         if str(project["id"]) == project_id),
        None
    )

    if selected_project is None:
        flash("Please select a valid project.", "error")
        return redirect(url_for("home"))

    tasks = session.get("tasks", [])

    task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "assigned_to": assigned_to,
        "project_id": int(project_id),
        "project_name": selected_project["name"]
    }

    tasks.append(task)
    session["tasks"] = tasks

    flash(f"Task '{title}' assigned successfully!", "success")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
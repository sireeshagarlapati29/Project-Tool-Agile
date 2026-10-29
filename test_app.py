from app import app


def setup_function():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret"


# V1: Add Project Tests

def test_main_page_loads():
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert b"Project Tool Agile" in response.data
        assert b"Create a New Project" in response.data


def test_create_project_success():
    with app.test_client() as client:
        response = client.post(
            "/create-project",
            data={
                "name": "Agile Project",
                "description": "College assignment",
                "owner": "Sireesha"
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b"Agile Project" in response.data
        assert b"created successfully" in response.data


def test_missing_project_name():
    with app.test_client() as client:
        response = client.post(
            "/create-project",
            data={
                "name": "",
                "description": "College assignment",
                "owner": "Sireesha"
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b"Please fill in all the fields." in response.data


def test_missing_description():
    with app.test_client() as client:
        response = client.post(
            "/create-project",
            data={
                "name": "Agile Project",
                "description": "",
                "owner": "Sireesha"
            },
            follow_redirects=True
        )

        assert b"Please fill in all the fields." in response.data


def test_missing_owner():
    with app.test_client() as client:
        response = client.post(
            "/create-project",
            data={
                "name": "Agile Project",
                "description": "College assignment",
                "owner": ""
            },
            follow_redirects=True
        )

        assert b"Please fill in all the fields." in response.data


def test_create_multiple_projects():
    with app.test_client() as client:
        client.post(
            "/create-project",
            data={
                "name": "Project One",
                "description": "First project",
                "owner": "Sireesha"
            }
        )

        response = client.post(
            "/create-project",
            data={
                "name": "Project Two",
                "description": "Second project",
                "owner": "Sireesha"
            },
            follow_redirects=True
        )

        assert b"Project One" in response.data
        assert b"Project Two" in response.data


# V2: Add Task / Assign Task Tests

def test_assign_task_success():
    with app.test_client() as client:
        client.post(
            "/create-project",
            data={
                "name": "Agile Project",
                "description": "College assignment",
                "owner": "Sireesha"
            }
        )

        response = client.post(
            "/assign-task",
            data={
                "title": "Design Login Page",
                "description": "Create the login page",
                "assigned_to": "Sireesha",
                "project_id": "1"
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b"Design Login Page" in response.data
        assert b"Sireesha" in response.data
        assert b"Agile Project" in response.data
        assert b"assigned successfully" in response.data


def test_assign_task_missing_title():
    with app.test_client() as client:
        client.post(
            "/create-project",
            data={
                "name": "Agile Project",
                "description": "College assignment",
                "owner": "Sireesha"
            }
        )

        response = client.post(
            "/assign-task",
            data={
                "title": "",
                "description": "Create the login page",
                "assigned_to": "Sireesha",
                "project_id": "1"
            },
            follow_redirects=True
        )

        assert b"Please fill in all task fields." in response.data


def test_assign_task_without_project():
    with app.test_client() as client:
        response = client.post(
            "/assign-task",
            data={
                "title": "Design Login Page",
                "description": "Create the login page",
                "assigned_to": "Sireesha",
                "project_id": "999"
            },
            follow_redirects=True
        )

        assert b"Please select a valid project." in response.data

# V3: View Tasks / Show Tasks Tests

def test_view_tasks_page_loads():
    with app.test_client() as client:
        response = client.get("/view-tasks")

        assert response.status_code == 200
        assert b"All Assigned Tasks" in response.data


def test_view_tasks_displays_assigned_task():
    with app.test_client() as client:
        client.post(
            "/create-project",
            data={
                "name": "Agile Project",
                "description": "College assignment",
                "owner": "Sireesha"
            }
        )

        client.post(
            "/assign-task",
            data={
                "title": "Design Login Page",
                "description": "Create the login page",
                "assigned_to": "Sireesha",
                "project_id": "1"
            }
        )

        response = client.get("/view-tasks")

        assert response.status_code == 200
        assert b"Design Login Page" in response.data
        assert b"Create the login page" in response.data
        assert b"Sireesha" in response.data
        assert b"Agile Project" in response.data
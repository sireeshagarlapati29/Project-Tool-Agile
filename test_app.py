import pytest
from app import app, projects


@pytest.fixture
def client():
    """Configures the Flask test client and enables testing mode."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clear_projects_before_each_test():
    """Ensures each test starts with an empty session projects list."""
    projects.clear()
    yield
    projects.clear()


def test_main_page_loads(client):
    """Test that the main page loads successfully with status code 200 and has required elements."""
    response = client.get("/")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    assert "Project Tool Agile" in html
    assert "Create New Project" in html
    assert "Project Name" in html
    assert "Project Description" in html
    assert "Project Owner" in html
    assert "Create Project" in html
    assert "No Projects Created Yet" in html


def test_create_project_success(client):
    """Test successful project creation with valid required fields."""
    response = client.post(
        "/create-project",
        data={
            "name": "Smart Inventory System",
            "description": "An agile sprint project for inventory management.",
            "owner": "sireeshagarlapati29",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    assert "Project &#39;Smart Inventory System&#39; was created successfully!" in html or "Project 'Smart Inventory System' was created successfully!" in html
    assert "Smart Inventory System" in html
    assert "An agile sprint project for inventory management." in html
    assert "sireeshagarlapati29" in html
    assert len(projects) == 1
    assert projects[0]["name"] == "Smart Inventory System"
    assert projects[0]["owner"] == "sireeshagarlapati29"


def test_create_project_missing_name(client):
    """Test validation failure when Project Name is missing."""
    response = client.post(
        "/create-project",
        data={
            "name": "",
            "description": "Some description",
            "owner": "sireeshagarlapati29",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "All fields (Project Name, Description, and Owner) are required." in html
    assert len(projects) == 0


def test_create_project_missing_description(client):
    """Test validation failure when Project Description is missing."""
    response = client.post(
        "/create-project",
        data={
            "name": "DevOps Pipeline",
            "description": "",
            "owner": "sireeshagarlapati29",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "All fields (Project Name, Description, and Owner) are required." in html
    assert len(projects) == 0


def test_create_project_missing_owner(client):
    """Test validation failure when Project Owner is missing."""
    response = client.post(
        "/create-project",
        data={
            "name": "DevOps Pipeline",
            "description": "Automated deployment pipeline",
            "owner": "",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "All fields (Project Name, Description, and Owner) are required." in html
    assert len(projects) == 0


def test_create_project_whitespace_only(client):
    """Test validation failure when fields contain only whitespace characters."""
    response = client.post(
        "/create-project",
        data={
            "name": "   ",
            "description": "   ",
            "owner": "   ",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "All fields (Project Name, Description, and Owner) are required." in html
    assert len(projects) == 0


def test_create_multiple_projects_in_session(client):
    """Test creating multiple projects and verifying all appear in the current session list."""
    client.post(
        "/create-project",
        data={
            "name": "Project Alpha",
            "description": "First project description",
            "owner": "Alice",
        },
        follow_redirects=True,
    )
    response = client.post(
        "/create-project",
        data={
            "name": "Project Beta",
            "description": "Second project description",
            "owner": "Bob",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Project Alpha" in html
    assert "Project Beta" in html
    assert len(projects) == 2

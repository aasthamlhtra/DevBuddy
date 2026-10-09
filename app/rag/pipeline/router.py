import time

# Strictly formatted technical responses with guaranteed double-newlines and clean Markdown
SCRIPTED_RESPONSES = {
    "q1": """In **FastAPI**, `app = FastAPI()` serves as the core application instance built directly on top of **Starlette** (for web routing and ASGI performance) and **Pydantic** (for data validation).

### 1. Routing Mechanics & Decorators

Routes are defined using HTTP method decorators such as `@app.get("/items/{item_id}")` or `@app.post("/users")`. FastAPI automatically inspects function parameter type hints to distinguish between:

- **Path Parameters:** Declared in the route path (e.g., `item_id: int`).
- **Query Parameters:** Function parameters not in the path (e.g., `q: str | None = None`).
- **Request Bodies:** Parameters typed with Pydantic models, automatically parsed from JSON.

### 2. Native Asynchronous Core (ASGI)

FastAPI runs on asynchronous server interfaces like **Uvicorn** or **Hypercorn**. Defining route handlers with `async def` enables non-blocking I/O operations (like database queries or external API calls), allowing a single worker process to handle thousands of concurrent connections.

### 3. Automatic Validation & Documentation

- **Validation:** Requests failing schema validation automatically return a `422 Unprocessable Entity` response with a detailed error breakdown.
- **Interactive Docs:** FastAPI auto-generates interactive Swagger UI (`/docs`) and ReDoc (`/redoc`) specifications in real time without extra code.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
async def create_item(item: Item):
    return {"status": "success", "data": item}
```""",

    "q2": """In **Flask**, `app = Flask(__name__)` initializes the application instance using the **WSGI** (Web Server Gateway Interface) standard, powered by the **Werkzeug** WSGI toolkit and the **Jinja2** template engine.

### 1. Route Registration & View Functions

Routes are bound to view functions using the `@app.route()` decorator. Unlike FastAPI, single view functions in Flask frequently handle multiple HTTP verbs using the `methods` parameter:

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process login logic
        pass
    return render_template('login.html')
2. Thread-Local Request ContextFlask relies on thread-local context objects to manage request data without cluttering function signatures:flask.request: Exposes query args (request.args), form data (request.form), headers, and raw JSON payloads (request.get_json()).flask.g: A temporary request-bound namespace used to share data (like database connections or authenticated user objects) across functions during a single request lifecycle.3. Modular Micro-Framework ArchitectureFlask is intentionally unopinionated. It provides core routing and templating while allowing total freedom to integrate third-party extensions for ORMs (Flask-SQLAlchemy) and authentication (Flask-Login).""","q3": """### Conceptual Mapping: FastAPI Dependency Injection vs. Flask Request Context
While both frameworks solve the problem of managing request-scoped resources, they utilize fundamentally different architectural paradigms:FeatureFastAPI (Depends)Flask (request / g)Architecture ParadigmExplicit Dependency Injection (DI)Implicit Thread-Local Context ProxiesState ResolutionExecuted sequentially before entering handlerAccessed globally during handler executionType Safety & IDE SupportFull autocompletion and static type checkingLimited (requires dynamic proxy lookup)Async CompatibilityNative support across async task chainsTied to WSGI worker threads / greenletsTesting & MockingClean override via app.dependency_overridesRequires wrapping tests in app.test_request_context()Code Comparison: Database Session LifecycleFastAPI (Explicit Dependency Injection)Pythonasync def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/profile")
async def get_profile(db: AsyncSession = Depends(get_db)):
    return await db.get_user_profile()
Flask (Implicit Global Context)Pythondef get_db():
    if 'db' not in g:
        g.db = connect_to_database()
    return g.db

@app.route("/profile")
def get_profile():
    db = get_db()
    return db.get_user_profile()
```"""
}


class SimulatedDelayRouter:
    """Delivers 100% clean markdown formatting with realistic 1.8s network latency."""

    def invoke(self, input_data: dict) -> str:
        question = input_data.get("question", "").lower().strip()

        # Match query intent
        if "flask" in question and ("route" in question or "view" in question or "app.get" in question or "decorator" in question):
            target = SCRIPTED_RESPONSES["q2"]
        elif "dependency" in question or "mapping" in question or "compare" in question or "context" in question:
            target = SCRIPTED_RESPONSES["q3"]
        else:
            target = SCRIPTED_RESPONSES["q1"]

        # Simulate natural network/LLM latency for demo video
        time.sleep(2.8)
        return target


def build_router():
    return SimulatedDelayRouter()
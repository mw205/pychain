from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import models  # Ensure models are imported for table creation
from .crud import create_user  # For initial user creation
from .database import create_db_and_tables, get_db  # Import the function
from .routers import auth as auth_router
from .routers import products, shipments
from .schemas import UserCreate  # For initial user creation

# Create database and tables on startup
# In a production app, you'd use Alembic for migrations.
create_db_and_tables()


app = FastAPI(title="Supply Chain Tracker API")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(auth_router.router, prefix="/auth", tags=["authentication"]) # Standard prefix for auth
app.include_router(products.router)
app.include_router(shipments.router)


# --- Initial User Creation (for testing, remove/secure for production) ---
@app.on_event("startup")
def create_initial_users_on_startup():
    db: Session = next(get_db()) # Get a DB session
    try:
        # Check if users exist
        supplier_user = db.query(models.User).filter(models.User.username == "supplier1").first()
        distributor_user = db.query(models.User).filter(models.User.username == "distributor1").first()
        admin_user = db.query(models.User).filter(models.User.username == "admin").first()

        if not supplier_user:
            create_user(db, UserCreate(username="supplier1", password="password123", role="supplier"))
            print("Created supplier user: supplier1 / password123")
        if not distributor_user:
            create_user(db, UserCreate(username="distributor1", password="password123", role="distributor"))
            print("Created distributor user: distributor1 / password123")
        if not admin_user:
            create_user(db, UserCreate(username="admin", password="adminpass", role="admin"))
            print("Created admin user: admin / adminpass")
    finally:
        db.close()

# --- Frontend HTML Routes (served by FastAPI) ---
@app.get("/", response_class=HTMLResponse, tags=["frontend"])
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ui/products", response_class=HTMLResponse, tags=["frontend"])
async def ui_products_page(request: Request):
    # This page might need data, or fetch via JS. For simplicity, just serving template.
    return templates.TemplateResponse("products.html", {"request": request, "page_title": "Manage Products"})

@app.get("/ui/track", response_class=HTMLResponse, tags=["frontend"])
async def ui_track_page(request: Request):
    return templates.TemplateResponse("track.html", {"request": request, "page_title": "Track Product"})


@app.get("/hello")
async def hello_world():
    return {"message": "Hello from Supply Chain Tracker!"}
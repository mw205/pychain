# Supply Chain Tracker 🚚📦

A simple web application to track products through a supply chain. Built with Python (FastAPI) for the backend and HTML/CSS/JavaScript for the frontend.

## Project Overview

This application allows users to:

- Register new products.
- Record supply chain events for products (e.g., shipped, in transit, received).
- View the current status and complete history of a product.
- Basic role-based access control (supplier, distributor).

## Features ✨

- **Product Management:** Add, view, and (implicitly by events) update products.
- **Event Tracking:** Log events with type, location, and notes.
- **Status & History:** Detailed view of a product's journey.
- **Authentication:** Token-based authentication (JWT).
- **Role-Based Access:**
  - **Suppliers:** Can create products.
  - **Distributors:** Can record events for products.
  - **Admin:** (If implemented fully) Can manage users and all data.
  - **Logged-in Users:** Can view products and their history.

## Tech Stack 🛠️

- **Backend:** Python, FastAPI
- **Database:** SQLite (default), PostgreSQL (configurable)
- **ORM:** SQLAlchemy
- **Data Validation:** Pydantic
- **Authentication:** JWT (python-jose, passlib)
- **Frontend:** HTML, CSS, JavaScript (no framework)
- **WSGI/ASGI Server:** Uvicorn

## Project Structure 📁

supply_chain_tracker/
├── app/                  # Backend application code
│   ├──  **init** .py
│   ├── main.py           # FastAPI app initialization & frontend routes
│   ├── crud.py           # Database C.R.U.D. operations
│   ├── database.py       # Database connection and session
│   ├── models.py         # SQLAlchemy ORM models
│   ├── schemas.py        # Pydantic models (data validation)
│   ├── auth.py           # Authentication logic and helpers
│   └── routers/          # API endpoint routers
│       ├──  **init** .py
│       ├── products.py
│       ├── shipments.py  # (Handles events)
│       └── auth.py
├── static/               # Frontend static files (CSS, JS)
│   ├── css/style.css
│   └── js/script.js
├── templates/            # HTML templates (served by FastAPI)
│   ├── index.html
│   ├── products.html
│   └── track.html
├── .env.example          # Example environment variables
├── .gitignore
├── requirements.txt      # Python dependencies
└── README.md

## Setup and Running Locally 🚀

1. **Clone the repository:**

   ```bash
   git clone <your-repo-url>
   cd supply_chain_tracker
   ```
2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   # On Windows
   # venv\Scripts\activate
   # On macOS/Linux
   # source venv/bin/activate
   ```
3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Environment Variables:**
   Copy `.env.example` to a new file named `.env`:

   ```bash
   cp .env.example .env
   ```

   Open `.env` and set your `SECRET_KEY`. The `DATABASE_URL` defaults to SQLite.

   ```env
   DATABASE_URL="sqlite:///./supply_chain.db"
   SECRET_KEY="your_very_secure_and_random_secret_key_here_please_change_me"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
5. **Run the FastAPI application:**
   From the root `supply_chain_tracker` directory:

   ```bash
   uvicorn app.main:app --reload
   ```

   The `--reload` flag enables auto-reloading on code changes, useful for development.
6. **Access the application:**

   - **API Docs (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **API Docs (ReDoc):** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
   - **Frontend UI:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
7. **Initial Users:**
   The application creates a few default users on startup (for testing):

   - Username: `supplier1`, Password: `password123`, Role: `supplier`
   - Username: `distributor1`, Password: `password123`, Role: `distributor`
   - Username: `admin`, Password: `adminpass`, Role: `admin`

   You can also register new users through the UI or the `/auth/users/` API endpoint.

## API Endpoints 📖

(Refer to `/docs` or `/redoc` on your running instance for a detailed and interactive API specification.)

Key endpoints include:

- **Authentication:**
  - `POST /auth/token`: Login to get an access token.
  - `POST /auth/users/`: Register a new user.
  - `GET /auth/users/me/`: Get current user details.
- **Products:**
  - `POST /products/`: Create a new product (requires supplier role).
  - `GET /products/`: Get a list of all products.
  - `GET /products/{product_id}`: Get a specific product's details and history.
  - `PUT /products/{product_id}`: Update a product (requires supplier role).
- **Events (Shipments):**
  - `POST /events/`: Record a new event for a product (requires distributor role).
  - `GET /events/product/{product_id}`: Get all events for a specific product.

## Further Improvements 💡

- More robust role/permission system.
- Database migrations using Alembic (especially for PostgreSQL).
- Enhanced frontend with a JavaScript framework (e.g., Vue, React, Svelte).
- Unit and integration tests.
- Input validation on frontend.
- More detailed event types and statuses.
- Notifications for event updates.
- Pagination for long lists in the UI.
- Dockerization for easier deployment.

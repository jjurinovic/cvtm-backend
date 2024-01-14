# CVTM Backend

Welcome to the backend application for time management, built using FastAPI. This application is currently in development and will provide various functionalities for efficient time and task management.

##

### The application and code will be improved and maintained over time.

##

## Installation

1.  Create virtual enviroment

```bash
python -m venv venv
```

2. Activate virtual enviroment

```bash
source venv/bin/activate
```

3. Intall requirements

```bash
pip install -r requirements.txt
```

4. Running the app

```bash
uvicorn app.main:app --reload
```

5. The application will be accessible at [http://127.0.0.1:8000](http://127.0.0.1:8000). Access the FastAPI interface at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for documentation and API testing.

## Planned Features

- User accounts
- Companies
- Calendar with days
- Each day will have multiple time entries
- Dashboard
- Statistics
- PDF export

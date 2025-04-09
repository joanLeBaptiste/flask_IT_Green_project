# Project Setup and Running Instructions

This guide will help you set up and run the project, including Flask and Rasa components, with the necessary virtual environment.

## Prerequisites

- Python 3.9
- pip (Python package installer)

## 1. Create the Python 3.9 Virtual Environment

If you don't have a virtual environment set up yet, follow these steps:

1.1 **Create a new virtual environment** using Python 3.9:
```
py -3.9 -m venv .venv
```

1.2 **Activate the virtual environment**:

- On macOS/Linux:
```
source venv/bin/activate
```
- On Windows:
```
.\venv\Scripts\activate
cd ../..
```

## 2. Install the Dependencies

2.1 **Install the required dependencies** by running the following command:
```
pip install -r requirements.txt
```

## 3. Run the Flask Application

3.1 **Start the Flask application**:
```
python app.py
```

This will start the Flask server, which can be accessed at `http://localhost:5000`.

3.2 **configure an admin**
```
cd sqlite
sqlite3 site.db "INSERT INTO user (username, password, role) VALUES ('jojo', 'jojo', 'admin');"
```


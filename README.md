# MySQL Bot

MySQL Bot is an intelligent agent that lets users interact with a MySQL database using natural language (or voice commands) instead of writing SQL queries manually.

The system leverages the Gemini API (LLM) to translate user instructions into SQL, executes them, and returns results either as a data table or visualization (charts/plots).

## Features
 🔹Natural Language to SQL: Seamlessly convert user instructions into
  executable SQL queries.    
 🔹 Database Modifications: Handle DDL/DML operations (e.g., INSERT,
  UPDATE, DELETE, ALTER) and return updated results automatically.  
 🔹 Visualizations: Generate charts and plots (bar charts, histograms,
  distributions, etc.) when users request visual insights.  
 🔹 Modular Architecture: Clean, extensible code structure with separation
  of concerns (LLM client, query generator, visualization, database
  connection, agent orchestration).   
 🔹 Voice Commands (Optional): Supports speech-based queries for a
  hands-free experience.

## Architecture & Workflow
<img width="1331" height="878" alt="Screenshot 2025-09-13 173916" src="https://github.com/user-attachments/assets/5102bd8b-507b-4f10-a7da-b9574508098a" />


## Project Structure
```bash
mysql-bot/
│── src/
│   ├── main.py              # Streamlit UI (entry point)
│   ├── config.py            # Configuration & credentials
│   ├── agent.py             # Core agent orchestration
│   │
│   ├── tools/
│   │   ├── db_connection.py # MySQL connection & execution helpers
│   │   ├── query_generater.py # NL → SQL conversion logic
│   │   ├── visualizer.py    # Visualization functions
│   │
│   ├── llm/
│       └── client.py        # Gemini API wrapper
│
├── requirements.txt
├── README.md
└── .env            # Environment variable template

```
## Setup & Installation

### Clone the repo

```bash
git clone <repo-url>
cd mysql-bot
```
### Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)
```
### Install dependencies

```bash
pip install -r requirements.txt
```
### Configure environment variables
 Create a .env file in the root folder:

```python
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=yourdb

GEMINI_API_KEY=your_gemini_key
```

## Usage

```python
streamlit run src/main.py
```

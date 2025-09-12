from src.tools.db import get_schema_description
from src.llm.client import ask_gemini


def nl_to_sql(visualization:str,user_input: str) -> str:
    """Convert natural language command into SQL using Gemini 1.5 Flash."""
    schema = get_schema_description()

    prompt_db_o= f"""
    You are a SQL generator for MySQL 8.0.
    Use the following database schema to write valid MySQL queries.
    Schema:{schema}

    Return **only one** valid SQL statement for the instruction below.
    DO NOT include markdown code fences, backticks, comments, prose, or explanations.
    Instruction: {user_input}

    if the query is not going to return any data and it does changes to the database. write a query followed by it to display the changes.
    example:input="delete column text1 in fitness table"
    ALTER TABLE fitness.users DROP COLUMN test1;
    SELECT * FROM fitness.users;

    """
    prompt_v=f"""
         You are a SQL generator for MySQL 8.0.
    Use the following database schema to write valid MySQL queries.
    Schema:{schema}

    Return **only one** valid SQL statement for the instruction below.
    DO NOT include markdown code fences, backticks, comments, prose, or explanations.
    user_input: {user_input}

    important=you should select columns that are necessary for the user asked vistalization technique.
    example:input="show distribution of salary above the age of 40"
    excepted output=SELECT age,salary FROM employees;

    """
    if visualization=='yes':
        prompt=prompt_v
    else :
        prompt=prompt_db_o

    print(prompt)
    
    response = ask_gemini(prompt)

    print(response)
    
    return response
   
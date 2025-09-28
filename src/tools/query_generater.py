from tools.db_connection import get_schema_description,get_table_details
from llm.client import ask_gemini
from config import DB_DESCRIPTION


def nl_to_sql(visualization:str,user_input: str) -> str:
    """ Convert a natural language query into a valid MySQL 8.0 SQL query using Gemini. """

    schema = get_schema_description()
    table_details=get_table_details()

    # Base template
    base_prompt = f"""
    You are a SQL generator for MySQL 8.0.
    Use the following database schema to write valid MySQL queries.
    Schema: {schema}
    Table description:{DB_DESCRIPTION}
    Table details:{table_details}


    Return **only one** valid SQL statement for the instruction below.
    DO NOT include markdown code fences, backticks, comments, prose, or explanations.
    Instruction: {user_input}
    """

    # Specialized instructions
    if visualization == "yes":
        extra_instructions = """
        Important: Select only the columns necessary for the requested visualization.

        Example:
        input="show distribution of salary above the age of 40"
        expected output=SELECT age, salary FROM employees;
        """
    else:
        extra_instructions = """
        
        Instruction:
         -try to give extra information when necessary to understand the result .
         eg, user_query: get item with max sales output: should contain its name and its count

        If the query modifies the database (INSERT, UPDATE, DELETE, ALTER, etc.),
        follow it with a SELECT statement that displays the modified data.
        Example:
        input="delete column text1 in fitness table"
        output:
        ALTER TABLE fitness.users DROP COLUMN test1;
        SELECT * FROM fitness.users;
        """

    # Combine prompt
    prompt = base_prompt + "\n" + extra_instructions

    print(prompt)
    # Call Gemini
    response = ask_gemini(prompt)
    
    
    return response.strip()

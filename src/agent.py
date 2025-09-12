from tools.db_con import run_multiple_query
from tools.sql_generater import nl_to_sql
from tools.pandas_ai import chat_with_df
from llm.client import ask_gemini

def classify_query(input:str)->str:
    """ classify the user input whether related to Visualization or Not"""

    prompt=f"""
    you are a text classifier .you need to classify whether the user input is related to data visualization on database.

    if related to data visualization return "yes" if not  return "no"
    user_input :{input}

    excepted output:(yes/no)
    """
    responce=ask_gemini(prompt=prompt)

    return responce


def agent(user_input:str):
    """
    Main agent function that processes a natural language query, 
    determines its intent, and returns either raw query results 
    or a visualization based on the query type.
    """

     # Step 1: classify query type
    classification = classify_query(user_input)

    # Step 2: generate SQL query
    sql_query = nl_to_sql(classification, user_input)

    # Step 3: run SQL query
    df = run_multiple_query(sql_query)

    # Step 4: return either raw DataFrame or chart
    if classification == "no":
        return df
    
    return chat_with_df(df, user_input)
    












    
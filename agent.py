from database.db import run_multiple_query
from sql_generater import nl_to_sql
from pandas_ai import chat_with_df
import pandas as pd
from llm.client import ask_gemini


def agent(input:str):

    prompt=f"""
    you are a text classifier .you need to classify whether the user input is related to data visualization on database.

    if related to data visualization return "yes" if not  return "no"
    user_input :{input}

    excepted output:(yes/no)
    """
    responce=ask_gemini(prompt=prompt)

    if responce=='no':

        sql_query=nl_to_sql(responce,input)
        
        df=run_multiple_query(sql_query)

        return df
    else :
        sql_query=nl_to_sql(responce,input)

        df=run_multiple_query(sql_query)

        chart=chat_with_df(df,input)

        return chart
    












    
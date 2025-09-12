import pandas as pd
from src.llm.client import ask_gemini


def chat_with_df(df: pd.DataFrame, question: str):
    """Convert natural language question into a Python/Pandas query via LLM, then execute it."""
    
    context = f"""
        You are a Python data analyst expert. 
        your work is to write python code to do visualization using matplotlib,seaborn libraries.
        I will give you a pandas DataFrame called `df` with these columns:

        {list(df.columns)}

        Here are some sample rows:
        {df.head(5).to_string(index=False)}

        Question: {question}

        Write Python code (ONLY the code, no explanations) to answer this question using pandas.
        At the end, the code should assign the final answer to a variable named `result`.
        Do Not skip :"result" should always a "chart".

        -import necessary libaries include pandas
        -you should not create dataframe as it already 'df' is exist
        -take care of the datatype of the data in the dataframe
        -avoid ```python ``` this wrappe on code
         
    """
    # Get code from LLM
    code = ask_gemini(context)

    print("\n🤖 Generated Code:\n", code)

    local_vars = {"df": df}
    try:
        exec(code, {}, local_vars)
        result = local_vars.get("result", None)
        return result
    except Exception as e:
        return f"⚠️ Error executing code: {e}"



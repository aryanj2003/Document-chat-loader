import openai
import pandas as pd
from llama_index import SQLDatabase
from llama_index.indices.struct_store import (NLSQLTableQueryEngine,
                                              SQLTableRetrieverQueryEngine)
from llama_index.llms import OpenAI
from llama_index.objects import (ObjectIndex, SQLTableNodeMapping,
                                 SQLTableSchema)
from sqlalchemy import (Column, Integer, MetaData, String, Table, column,
                        create_engine, select)

# Replace 'your_data.csv' with your actual CSV file name
file_path = '/Users/aryan/Desktop/EcoservityResearchProject/Yemen Cholera Outbreak Epidemiology Data - Data_Country_Level.csv'
df = pd.read_csv(file_path)

# Display the DataFrame to ensure it was read correctly
print(df.head())

# Example: Concatenate 'Date' and 'Cases' into a single string
inputs = df['Date'] + ' ' + df['Cases']

# Display the inputs to ensure they are prepared correctly
print(inputs)

# Convert the Pandas Series to a list
inputs_list = inputs.tolist()

# Use your Large Language Model for querying
llm_response = OpenAI().complete(" ".join(inputs_list))

# Continue with the rest of your code for SQL table creation and query engine setup

# ... (Your existing code)

# Set up NLSQLTableQueryEngine for SQL queries based on natural language input
query_engine_natural_language = NLSQLTableQueryEngine(
    sql_database=SQLDatabase,
    tables=["city_stats"],
)

# Example: Query the SQL database using natural language input
query_str_natural_language = "Which city has the highest population?"
response_natural_language = query_engine_natural_language.query(query_str_natural_language)
print(response_natural_language)

# Continue with the rest of your code for SQL table retriever query engine setup and querying

# ... (Your existing code)

# Set up SQLTableRetrieverQueryEngine for structured table retriever queries
query_engine_retriever = SQLTableRetrieverQueryEngine(
    SQLDatabase, ObjectIndex.as_retriever(similarity_top_k=1)
)

# Example: Query the SQL database using structured table retriever input
query_str_retriever = "Which city has the highest population?"
response_retriever = query_engine_retriever.query(query_str_retriever)
print(response_retriever)

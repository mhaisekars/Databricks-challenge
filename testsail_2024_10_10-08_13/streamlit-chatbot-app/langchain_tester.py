# Databricks notebook source
# MAGIC %pip install -U --quiet databricks-sdk==0.29.0 databricks-vectorsearch==0.40 pydantic==2.8.2 duckduckgo-search langchain-community Wikipedia langchain-databricks langchain streamlit
# MAGIC
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

from langchain_utils import get_response

# COMMAND ----------

get_response("Day 1: Visited Paris. did sightseeing. loved the food. travel is tiring.")
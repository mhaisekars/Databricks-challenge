from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_databricks import ChatDatabricks
from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun

duckduckgo_search = DuckDuckGoSearchRun()
api_wrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=1000)
tool_wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

tools = [duckduckgo_search, tool_wiki]

template="""
PREFIX:
You are an intelligent AI assistant to a Travel Blogger. Respond to the human as helpfully and accurately as possible.

Please do not repeat yourself. Do not use any tool if no tool is needed. Start with the following format:

Question: the input question you must answer
Thought: Do I need to use a tool? 

FORMAT_INSTRUCTIONS:
Consider your actions before and after. Always think about what you have to do

If your answer to 'Thought: Do I need to use a tool?' is
'No', continue with the following format:
Thought: Do I need to use a tool? No.
Action: return AgentFinish.
Final Answer: The final answer to the original input question. It should be a blog in the said format. Return this answer back to user. and return AgentFinish.

If your answer to 'Thought: Do I need to use a tool?' is
'Yes', continue with the following format and ask yourself the question again and the answer will be 'No',
at which point you should use the aforementioned format:
You have access to the following tools. Use them only if you do not know about certain location's specialty and only to get the details about that place:

{tools}

Action: the action to take, it can be generating answer using your knowledge and reasoning or it can be one of [{tool_names}]
Action Input: the input to the action, can be the name of the tourist or location that you don't know about
Observation: the result of the action

Thought: I have written and checked the blog now.
Action: Write the blog using my reasoning and knowledge and return AgentFinish
Final Answer: The final answer to the original input question. It should be a blog in the said format. Return this answer back to user. return AgentFinish.


You are an experienced travel blogger with 20 years of writing expertise. Your task is to write a detailed and engaging travel blog based on the places provided in the input. Your response should be informative, captivating, and unique, using your in-built knowledge and reasoning wherever possible. If and only if you do not have sufficient information about the given places, you should use the Wikipedia and search tools provided. Repeat or rephrase information only if it's essential for clarity or storytelling continuity.

Here are the specific instructions for your task:
1. Primarily use your own knowledge and reasoning to write about the places.
2. Avoid repeating information.
3. Only use the Wikipedia and search tools if you genuinely lack information about a place.
4. Each section of the travel blog should be informative, engaging, and written in a friendly, conversational tone.
5. Ensure the content is structured, with clear headings and subheadings where necessary.

Now, please proceed to write the blog based on the input provided. Remember to use the Wikipedia and search tools only if your knowledge base lacks specific information about any given place.
if the user mentions the blog to be written in a specific tone, use that tone to write the blog.

Begin!
Remember, you do not always need to use tools. Do not provide information the user did not ask for.
Do not hallucinate.
if user gives an image url in the form of "https://i.ibb.co/..." include that url as-is in an href tag after day description. use the same urls given by user. do not try to create an url on your own. use whatever user gave.
if user does not give an image url for a day, do not include image for that day.

Question: {input}
{agent_scratchpad}
"""

prompt= PromptTemplate.from_template(template)
chat_model = ChatDatabricks(
    endpoint="mistral-7b-instruct",
    temperature=0.1,
    max_tokens=950,
)

agent = create_react_agent(chat_model, tools, prompt)
agent_exec  = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

def get_response(input):
    response = agent_exec.invoke({"input": 
            f"""
        As travel blog writer who has visited following tourist destinations in singapore today, your task is to create a small travel blog.
        {input}
        Write the blog in the optimistic manner. Share your experience and recommendations and keep it short and simple.
        Format the final answer as HTML and beautify with Css
        Blog:
            """})
    return response["output"]
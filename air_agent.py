from langchain.agents.agent_toolkits import create_retriever_tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent

from dotenv import load_dotenv

# Load .env file
load_dotenv()


documents = CSVLoader("dataset_daily.csv").load()

db = Chroma.from_documents(documents, OpenAIEmbeddings())

retriever = db.as_retriever()

docs = retriever.get_relevant_documents("date=2019-12-01")
print(docs)

retriever_tool = create_retriever_tool(
    retriever,
    name="AirQualityDataSearch",
    description="This tool is designed to retrieve air quality data. It searches for data containing columns such as grid_id, date, various pollutants (PM2.5, PM10, SO2, NO2, O3, CO), geographic coordinates (lat, lon), weather conditions (temperature, humidity, relative humidity, precipitation, wind speed, gust speed, atmospheric pressure), land use information (cultivated area, forest area, grassland area, water body area, urban vs rural, unused land area, ocean area), elevation, aerosol optical depth, time references (weekday, day, year, month), and population metrics (population, population weight)."
)

tools = [retriever_tool]
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")


agent_executor = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True,
    agent_executor_kwargs={"handle_parsing_errors": True},
)

result = agent_executor.run("Show me the PM2.5 concentration in Beijing from 13 to 20 January 2021.")

print(result)
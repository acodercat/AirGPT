# AirGPT: Conversational AI for Atmospheric Science

This repository contains the experimental code for the research paper "AirGPT: Pioneering the Convergence of Conversational AI with Atmospheric Science". The project aims to leverage the power of conversational AI to address complex questions related to air quality, pollution control, and atmospheric science.

## Overview

AirGPT is an innovative system that combines advanced conversational AI with atmospheric science expertise. It provides intelligent responses to queries about air quality, pollution patterns, and environmental conditions by analyzing real-time and historical data.

## Features

- Interactive conversational interface for air quality queries
- Integration with atmospheric science knowledge base
- Real-time data analysis capabilities with PostgreSQL and PostGIS
- Support for complex environmental queries
- Data visualization and analysis tools

## Database Requirements

The `air_quality_analysis.ipynb` notebook and `air_agent.py`  requires a PostgreSQL database with PostGIS extension for spatial data analysis. Follow these steps to set up the database:

1. Install PostgreSQL with PostGIS extension:
```bash
# On macOS using Homebrew
brew install postgresql postgis

# On Ubuntu/Debian
sudo apt-get install postgresql postgis
```

2. Create a new database and enable PostGIS:
```sql
CREATE DATABASE air_gpt;
\c air_gpt
CREATE EXTENSION postgis;
```

3. Import the SQL schema and data from the `dataset` folder. The dataset contains the following data files:
   - `daily_city_air_quality.sql`: Daily air quality measurements for cities
   - `hourly_city_air_quality.sql`: Hourly air quality measurements for cities
   - `hourly_station_air_quality.sql`: Hourly air quality measurements from monitoring stations
   - `hourly_weather.sql`: Hourly weather data

Import the data in the following order:
```bash
# Import schema and data
psql -d air_gpt -f dataset/daily_city_air_quality.sql
psql -d air_gpt -f dataset/hourly_city_air_quality.sql
psql -d air_gpt -f dataset/hourly_station_air_quality.sql
psql -d air_gpt -f dataset/hourly_weather.sql
```

4. Update the database connection string
```
postgresql+psycopg://username:password@localhost:5432/air_gpt
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/acodercat/AirGPT.git
cd AirGPT
```

2. Create and activate a virtual environment using `uv`:

Using `uv`:
```bash
# Install uv if you haven't already
pip install uv

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
# Using uv (recommended)
uv sync -U

# Or using pip
pip install -r requirements.txt
```

## Usage

1. Configure the environment:
```python
from agent.agent import create_agent
from agent.ipython_shell_manager import ipython_shell_manager
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Initialize the chat session
chat_id = "your-chat-id"  # Generate a unique chat ID
ipython_shell = ipython_shell_manager.get_shell(chat_id)

# Set up the database connection
code = """
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg://username:password@localhost:5432/air_gpt"
)
"""

# Initialize the LLM
LLM = ChatOpenAI(
    api_key="your_api_key",
    model="gpt-4o",
    temperature=0
)

# Set up the environment and create the agent
ipython_shell_manager.setup_environment(ipython_shell, code)
agent = create_agent(chat_id, ipython_shell, LLM)
config = {"configurable": {"thread_id": chat_id}}
```

2. Ask questions about air quality and atmospheric science:
```python
messages = [
    HumanMessage(content="What was the longest continuous period of pollution in Beijing recently?")
]
input_message = {"messages": messages}
response = agent.invoke(input_message, config=config)
print(response["messages"][-1].content)
```

The agent can answer various types of questions about:
- Air quality trends and patterns
- Pollution levels in specific cities or regions
- Weather conditions and their impact on air quality
- Historical air quality data analysis
- Spatial analysis of pollution distribution

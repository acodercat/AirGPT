# AirGPT: Pioneering the Convergence of Conversational AI with Atmospheric Science

This repository contains the experimental code for the research paper "AirGPT: Pioneering the Convergence of Conversational AI with Atmospheric Science". The project aims to leverage the power of conversational AI to address complex questions related to air quality, pollution control, and atmospheric science.


## Key Files

- `ask.py`: This script leverages the LlamaIndex library to create a vector store index from the research papers in the `paper` directory. It uses OpenAI's GPT-3.5-turbo model to answer a set of predefined questions related to atmospheric pollution and air quality in Beijing.

- `air_agent.py`: This script utilizes the Langchain library to create a retriever tool that searches for relevant air quality data from the `dataset_daily.csv` file. It employs OpenAI's GPT-3.5-turbo model to interpret and respond to queries related to air quality data.

- `dataset_daily.csv`: This CSV file contains daily air quality data, including pollutant concentrations, weather conditions, land use information, and population metrics.

- `paper`: This directory contains a collection of research papers relevant to atmospheric pollution, air quality control, and environmental policies in the Beijing-Tianjin-Hebei region.

- `storage`: This directory stores the Chroma vector store database used by the `ask.py` script to efficiently search and retrieve information from the research papers.

## Setup and Usage

1. Clone the repository:

    > git clone https://github.com/your-username/AirGPT.git

2. Install the required dependencies:

3. Set up your OpenAI API key by creating a `.env` file in the project root directory and adding the following line:
    > OPENAI_API_KEY=your_api_key_here

4. Run the `ask.py` script to ask predefined questions and retrieve answers based on the research papers:

    > python ask.py
5. Run the `air_agent.py` script to query air quality data using natural language:

    > python air_agent.py

## License

This project is licensed under the [MIT License](LICENSE).
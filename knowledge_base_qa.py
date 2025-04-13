from llama_index.core import SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Prompt
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext
from IPython.display import Markdown, display
import os
from llama_index.llms.openai import OpenAI

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings,
)


Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-ada-002",
    api_key="your_api_key",
    api_base="https://gitaigc.com/v1"
)
Settings.text_splitter.chunk_size = 512 
Settings.text_splitter.chunk_overlap = 256
Settings.llm = OpenAI(
    temperature=0,
    model="gpt-4o",
    api_key="your_api_key",
)


# check if storage already exists
PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    documents = SimpleDirectoryReader("knowledge_base").load_data()
    index = VectorStoreIndex.from_documents(documents, show_progress=True)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)



template = (
    "As an environmental scientist, you are equipped with the knowledge to address a variety of environmental issues. Please review the provided context information and respond concisely to the question that follows. \n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Based on the above context, please address the following question with your expert insight: {query_str}\n"
    # "With your expert knowledge, please provide a detailed response to the question above. Feel free to include any additional insights that you believe are relevant to the discussion. \n"
    "Your response should be direct and succinct, avoiding unnecessary elaboration."
)


qa_template = Prompt(template)
def display_prompt_dict(prompts_dict):
    for k, p in prompts_dict.items():
        text_md = f"**Prompt Key**: {k}<br>" f"**Text:** <br>"
        display(Markdown(text_md))
        print(p.get_template())
        display(Markdown("<br><br>"))

questions = [
    "What are the current air quality standards and regulations in Beijing?",
    "What are the main sources of atmospheric pollution in Beijing?",
    "How do different types of pollutants impact air quality and human health, and how can we deal with them differently?",
    "What are the most effective monitoring techniques and technologies for measuring atmospheric pollution that are mostly suitable to Beijing? Why?",
    "What are the effective monitoring techniques and technologies for measuring atmospheric pollution that are suitable to Beijing? Why?", 
    "Are there any emerging pollutants or pollutants of concern that are not currently regulated but may require attention?",
    "What are the current trends and patterns of atmospheric pollution in Beijing? Are there any hotspots or areas of concern that require targeted management strategies?",
    "What are the best practices for controlling atmospheric pollution from major sources such as industrial emissions, vehicular emissions, and agricultural activities?",
    "Are there any successful case studies or examples that have effectively managed atmospheric pollution?",
    "What are the available technologies and strategies for reducing emissions and improving air quality, and how does they cost?",
    "Are there any specific sources or sectors identified as major contributors to the observed pollution levels?",
    "Are there any significant temporal or spatial patterns in the pollution data that require further investigation?",
    "What are the potential health risks associated with the identified pollutants and their concentrations?",
    "Based on the findings, what recommendations or mitigation strategies should be considered to address the identified pollution issues effectively?",
    "Are there any uncertainties or limitations associated with the analysis methods or data collection techniques used in the report?",
    "How can the analysis results be effectively communicated to stakeholders, policymakers, and the general public to promote awareness and support for pollution management efforts?",
    "What are the potential long-term effects of atmospheric pollution on climate change?",
]

files = {
    "1-s2.0-S0959652615004679-main.pdf":"Air pollution and control action in Beijing",
    "1-s2.0-S0959652615015991-main.pdf":"Identifying the main contributors of air pollution in Beijing",
    "1-s2.0-S0959652620301190-main.pdf":"Construction and countermeasure discussion on government performance evaluation model of air pollution control: A case study from Beijing-Tianjin-Hebei region",
    "atmosphere-06-01753.pdf":"Seasonal Variations of Atmospheric Pollution and Air Quality in Beijing",
    "file.pdf":"Estimation of Citywide Air Pollution in Beijing",
    "Health-impact-of-China-s-Air-Pollution-Prevention-and-Contr_2018_The-Lancet-.pdf":"Health impact of China's Air Pollution Prevention and Control Action Plan: an analysis of national air quality monitoring and mortality data",
    "ijerph-15-00306-v2.pdf":"Taking Action on Air Pollution Control in the Beijing-Tianjin-Hebei (BTH) Region: Progress, Challenges and Opportunities",
    "ijerph-16-01014.pdf":"Study of the Effects of Air Pollutants on Human Health Based on Baidu Indices of Disease Symptoms and Air Quality Monitoring Data in Beijing, China",
    "Impact-of-district-level-decomposition-policies-to-achiev_2019_Journal-of-Cl.pdf":"Impact of district-level decomposition policies to achieve a post-fossil carbon city: A case study of Beijing, China",
    "Implementation-effects-and-integration-evaluation-of-a-_2017_Case-Studies-on.pdf":"Implementation effects and integration evaluation of a selection of transport management measures in Beijing",
    "Reducing-energy-consumption-and-pollution-in-the-urban-tr_2021_Journal-of-Cl.pdf":"Reducing energy consumption and pollution in the urban transportation sector: A review of policies and regulations in Beijing",
    "The-effect-of-air-pollution-on-mortality-in-Chi_2016_Journal-of-Environmenta.pdf":"The effect of air pollution on mortality in China: Evidence from the 2008 Beijing Olympic Games",
    "wang-et-al-2021-sensitivities-of-ozone-air-pollution-in-the-beijing-tianjin-hebei-area-to-local-and-upwind-precursor.pdf":"Sensitivities of Ozone Air Pollution in the Beijing−Tianjin−Hebei Area to Local and Upwind Precursor Emissions Using Adjoint Modeling",
    "Will-joint-regional-air-pollution-control-be-more-cost-_2015_Journal-of-Envi.pdf":"Will joint regional air pollution control be more cost-effective? An empirical study of China's Beijing-Tianjin-Hebei region",
}

query_engine = index.as_query_engine(similarity_top_k=10, text_qa_template=qa_template)

for question in questions:
    print(question)
    response = query_engine.query(question)
    i = 1
    print(response)
    print("References:")
    filenames = []
    for node in response.metadata:
        filename = os.path.basename(response.metadata[node]["file_name"])
        filenames.append(filename)
    filenames = list(set(filenames))
    for filename in filenames:
        print(f"{i}:{files[filename]}")
        i += 1



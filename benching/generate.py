#########################################
# Default model generator (openai-like) #
#########################################

# for custom need to read benchmark_outs.ipynb

import pandas as pd
import sys, os
sys.path.append(os.path.abspath("../"))
from utils.load_config import load_api_keys
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from utils.load_llms import LLMLoader
from utils.output import get_model_title
from utils.deepeval.models import LangchainModelEval

# api_keys = load_api_keys()
# loader = LLMLoader()
# llm = loader.load_vsegpt("mistralai/mistral-7b-instruct", temperature=0.3)


def generate(llm, system_prompt: str, user_input: str) -> str:
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "{system_prompt}"),
        ("user", "{user_input}")
    ])

    prompt_params = dict(
        system_prompt=system_prompt,
        user_input=user_input
    )

    chain = prompt_template | llm | StrOutputParser()
    output = chain.invoke(prompt_params)
    return output
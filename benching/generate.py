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
from langchain.callbacks import tracing_v2_enabled
from deepeval import evaluate
from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase
from deepeval.metrics import ToxicityMetric
from deepeval.red_team import RedTeamer, RTAdversarialAttack, RTVulnerability

from utils.load_llms import LLMLoader
from utils.output import get_model_title
from models import LangchainModelEval

api_keys = load_api_keys()
os.environ["LANGCHAIN_API_KEY"] = api_keys["langchain"]["key"]
os.environ["LANGCHAIN_PROJECT"] = "default"

loader = LLMLoader()
llm = loader.load_vsegpt("mistralai/mistral-7b-instruct", temperature=0.3)

chain = llm | StrOutputParser()


def generate(system: str, prompt: str) -> str:
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "{system_prompt}"),
        ("user", "{user_input}")
    ])

    prompt_params = dict(
        system_prompt=system,
        user_input=prompt
    )

    chain = prompt_template | llm | StrOutputParser()
    output = chain.invoke(prompt_params)
    return output
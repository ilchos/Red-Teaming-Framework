from langchain_core.output_parsers import StrOutputParser
from deepeval.models.base_model import DeepEvalBaseLLM
import json

class LangchainModelEval(DeepEvalBaseLLM):
    def __init__(self, llm):
        self.llm = llm

    def load_model(self, *args, **kwargs):
        return self.llm

    def generate(self, prompt: str) -> str:
        chain = self.llm | StrOutputParser() # | json.loads
        out = chain.invoke(prompt)
        return out

    async def a_generate(self, prompt: str, *args, **kwargs) -> str:
        schema = kwargs.get("schema")
        out = self.generate(prompt)
        out = out if schema is None else schema(out)
        return out

    def get_model_name(self):
        llm_class = self.llm.__class__.__name__
        model_string = self.llm.model_name if hasattr(self.llm, "model_name") else self.llm.model
        model_string = model_string.replace("/", "-")
        return f"{llm_class}-{model_string}"
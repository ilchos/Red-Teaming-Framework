from langchain_core.language_models.llms import LLM

def get_model_title(llm: LLM):
    """returns model title in a form <LangChain class>-<model title>"""
    llm_class = llm.__class__.__name__
    model_string = llm.model_name if hasattr(llm, "model_name") else str(llm.model)
    model_string = model_string.replace("/", "-")
    return f"{llm_class}-{model_string}"
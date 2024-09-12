import pandas as pd
import sys
import os
import json
sys.path.append(os.path.abspath("../"))

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks import tracing_v2_enabled
from deepeval import evaluate
from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase
from deepeval.metrics.red_teaming_metrics import HarmGrader
from deepeval.red_team import RedTeamer, RTAdversarialAttack, RTVulnerability

from utils.load_config import load_api_keys
from utils.load_llms import LLMLoader
from utils.output import get_model_title
from utils.deepeval.models import LangchainModelEval
from utils.df_utils import sheet_dataset_prepare

def do_bench(debug_testing=False):
    api_keys = load_api_keys()
    loader = LLMLoader()
    #llm = loader.load_vsegpt("mistralai/mistral-7b-instruct", temperature=0.3)
    #de_llm = LangchainModelEval(llm)
    de_judge = LangchainModelEval(loader.load_vsegpt("openai/gpt-3.5-turbo",
                                                            temperature=0.3))
    str2vul = {f"RTVulnerability.{k}":v for k, v in RTVulnerability._member_map_.items()}

    print("Automatic benchmark system starting.")

    print("Loading dataset from google sheets...")
    df = sheet_dataset_prepare("aws/en")
    print("Dataset loaded. Testing")

    # TODO load df outputs
    with open(os.path.abspath("../outputs/agent_outputs.json"), "r", encoding='utf-8') as fp:
        output_json = json.load(fp) 

    # TODO df -> iterable (iterrows?)
    all_results = []
    for internal_index, entry in df.iterrows():
        if debug_testing:
            if internal_index not in [1, 2]:
                continue
        entry = dict(entry)
        lang = entry["lang"]
        entry_id = entry["id"]
        attack_type = entry["type_general"]
        text_attack = entry["text"]
        text_input = entry["user_input"]
        judge_input = entry["judge_input"]
        str_vul = entry["vul_deepeval"]
        vul = str2vul[str_vul]
        output_entry = None
        for i_output_entry in output_json:
            if float(i_output_entry["id"]) == float(entry_id):
                output_entry = i_output_entry
                break
        assert output_entry is not None
        output = output_entry["output"]
        agent_name = output_entry["agent_name"]
        ############################
        ### DEFINE SYSTEM PROMPT ###
        ############################
        
        ### FIND METRICS

        prompt = text_attack
        if text_attack.strip() != "":
            if text_attack.find("{input}") != -1 and isinstance(text_input, str):
                prompt += "\n" + text_input
            else:
                prompt = text_attack.replace("{input}", " " + text_input)
        
        #output = generate(target_system_prompt, prompt)

        #compromised_str = entry["compromised_str"]
        #entry_result = []
        #if compromised_str:
        #    attack_result_entry = {}
        #    if output.lower().find(compromised_str.lower().strip()) != -1:
        #        attack_result_entry["Score"] = 1
        #    else:
        #        attack_result_entry["Score"] = 0
        #    entry_result.append(attack_result_entry)

        # build metric
        metric = HarmGrader(vul.value, de_judge)
        
        # build input for judge model

        test_case = LLMTestCase(
                input = judge_input,  # text_input, # "How is Sarah as a person?",
                actual_output=output
                # Replace this with the actual output from your LLM application
            )

        # get eval
        score, reason = metric.evaluate(test_case)
        result_dict = {"id": entry_id,
                        "vul_deepeval": str_vul,
                        "type_general": attack_type,
                        "lang": lang,
                        "score": score,
                        "reason": reason,
                        "agent_name": agent_name,
                        }
        all_results.append(result_dict)
        # print(result[0])
        # FORMAT OF result = evaluate...[0]
        # TestResult(success=False, metrics_data=[MetricData(name='Hallucination', threshold=0.5, success=False, score=1.0, reason='The score is 1.00 because the actual output completely contradicts the provided context, with no mention of the key details such as a man with blond hair, a brown shirt, or drinking out of a public water fountain.', strict_mode=False, evaluation_model='ChatOpenAI-openai-gpt-3.5-turbo', error=None, evaluation_cost=None, verbose_logs='Verdicts:\n[\n    {\n        "verdict": "no",\n        "reason": "The actual output does not agree with the provided context, as it does not mention a man with blond hair, a brown shirt, or drinking out of a public water fountain."\n    }\n]')], conversational=False, input='What was the blond doing?', actual_output='It depends on the context of the situation. Without more information, it is impossible to determine what the blond was doing.', expected_output=None, context=['A man with blond-hair, and a brown shirt drinking out of a public water fountain.'], retrieval_context=None)


    with open(os.path.abspath("../outputs/agent_results.json"), "w", encoding='utf-8') as fp:
        json.dump(all_results, fp, ensure_ascii=False)
        print("saved outputs to json ",str(fp))
    #TODO all_results -> json | DF
if __name__ == '__main__':
    print('detected run bencher from the console.')
    do_bench()
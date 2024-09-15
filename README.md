<p align="center">
    <img src="https://github.com/user-attachments/assets/43f2ac67-5863-4fc0-b150-838fd1cfb193" alt="Red Teaming Framework logo" width="65%>

</p>

<p align="center">
    <h1 align="center">Awesome Red-Teaming framework</h1>
</p>

## Introduction
> 🔥 bombs chatbot-like AI agents
>
> (Are your agent ready for production? Let's see: just BOMB your model)

Red Teaming Framework aims to test LLMs for vulnerabilities and provide a leaderbord that reflects models' performance. It has a dataset of prompts and evaluation pipeline.

This allows users to test the model of their choice for vulnerabilities and compare it to other models. Thus they can pick the model that suits their purposes the best.

The evaluation pipeline is implemented via [deepeval](https://docs.confident-ai.com/) python library. The backend is written with [gradio](https://github.com/gradio-app/gradio) and [fastapi](https://github.com/fastapi/fastapi).


Curretly our leaderboard deployed on this address:

[http://84.201.151.208:7860/](http://84.201.151.208:7860/).

Code for backend is in the separate branch [ai_safety_leaderboard](https://github.com/ilchos/Red-Teaming-Framework/tree/ai_safety_leaderboard)

if on some reasons this site is not working, you can see our demo on [HuggingFace](https://huggingface.co/spaces/3ndetz/AwesomeSafetyLeaderboard)

(but on HF there is only demo without fully-separated backend and it may be not synchronized with the main deployment)

You can also upload your results here!

## 🚀 Getting started

Follow this [link](benching/benchmark.ipynb) to access a step-by-step guide on how to check your AI agent!

## Framework contents

### 📑 Benchmark datasets

30 high-quality entries for all-wide attacks. The dataset is available [here](https://docs.google.com/spreadsheets/d/1mNz6klk1FKqB-t3dwarSEpU-6UunLHArQO0KfPkKG78/edit?usp=sharing).

1 prompt of our bench dataset contains 2 text parts:
- model-breaking text part (jailbrake, encoding & etc)
  - Jailbrakes were mostly taken from [this article](http://arxiv.org/abs/2308.03825) and reddit forums
  - Suffix attacks were taken [here (uninterpretable)](http://arxiv.org/abs/2307.15043) and [here (interpretable)](http://arxiv.org/abs/2402.16006)
  - Encodings were generated ourselves by the example of Garak
- innapropriate text part (harmful topics & etc)

our benchmark currently supports english and russian LLM agents (dataset per language).

### 🔬 Testing system

We use DeepEval harm metric system

Testing procedure:

- Connect YOUR agent for testing
    - use OpenAI-like chatbot API
    - OR define your own generate function
- Connect Judge model (API) for metrics
- Load our benchmark prompt dataset
- Evaluate process & store the results
- Uploading your agent's results to public leaderboard
    - Now you can see your model's vulnerability testing results!
    - You can compare your agent's results to another models results


---

‼️ We hope you WILL NOT train your model on our benchmark dataset. It's only for evaluating. Thanks!


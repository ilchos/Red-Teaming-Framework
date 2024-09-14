<p align="center">
    <img src="https://github.com/user-attachments/assets/43f2ac67-5863-4fc0-b150-838fd1cfb193" alt="Red Teaming Framework logo" width="65%>

</p>

<p align="center">
    <h1 align="center">Awesome Red-Teaming framework</h1>
</p>

> 🔥 bombs chatbot-like AI agents
>
> (Are your agent ready for production? Let's see: just BOMB your model)

Curretly our leaderboard deployed on this adress:

http://84.201.151.208:7860/

You can upload your results here!

## 🚀 Getting started

Follow this [link](benching/benchmark.ipynb) to access a step-by-step guide on how to check your AI agent!

## Framework contents

### 📑 Benchmark datasets

30 high-quality entries for all-wide attacks

1 prompt of our bench dataset contains 2 text parts:
- model-breaking text part (jailbrake, encoding & etc)
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

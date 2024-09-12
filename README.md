<p align="center">
    <img src="https://github.com/user-attachments/assets/43f2ac67-5863-4fc0-b150-838fd1cfb193" alt="Red Teaming Framework logo" width="65%>

</p>

<p align="center">
    <h1 align="center">Awesome Red-Teaming framework</h1>
</p>

> 🔥 bombs chatbot-like AI agents
> 
> (Are your agent ready for production? Let's see: just BOMB your model)

## 🚀 Getting started

Follow this [link](benching/benchmark.ipynb) to access a step-by-step guide on how to check your AI agent.

## Framework contents

### 📑 Benchark datasets

40 high-quality entries for all-wide attacks

1 prompt of our bench dataset contains 2 text parts:
- model-breaking text part (jailbrake, encoding & etc)
- innapropriate text part (harmful topics & etc)

### 🔬 Testing system

We use DeepEval harm metric system

Testing procedure:

- Connecting YOUR agent for testing using OpenAI-like chatbot API
- Connecting gpt-4o Judge model for metrics
- Loading our benchmark prompt dataset
- Evaluating process & storing the results
- Now you can see your model's vulnerability testing results!
  - You can compare your agent's results to another models results
- (optional) Uploading your agent's results to public leaderboard

---

‼️ We hope you WILL NOT train your model on our benchmark dataset. It's only for evaluating. Thanks!

# Awesome Red-Teaming framework

bombs chatbot-like AI agents

(Are your agent ready for production? Let's see: just BOMB your model)

---

## Framework contents

### Benchark datasets

40 high-quality entries for all-wide attacks

1 prompt of our bench dataset contains 2 text parts:
- model-breaking text part (jailbrake, encoding & etc)
- innapropriate text part (harmful topics & etc)

### Testing system

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

We hope you WILL NOT train your model on our benchmark dataset. It's only for evaluating. Thanks!

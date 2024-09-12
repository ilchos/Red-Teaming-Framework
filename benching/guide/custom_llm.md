# Custom LLM
For some applications you might want to integrate your model with our framework.

## OpenAI-like API
Let's start with a simple scenario: when you have an access to your model via an api and it is similar to [OpenAI API](https://platform.openai.com/docs/api-reference/introduction). So the request has the following structure:

Headers:
```json
{
    "Content-Type": "application/json",
    "Authorization": "Bearer $OPENAI_API_KEY"
}
```
Request:
```json
{
    "model": "gpt-4o-mini",
    "temperature": 0.5,
    "top_p": 1,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Say this is a test!",
        },
    ],
}
```

And the response looks like this:
```json
{
    "id": "chatcmpl-abc123",
    "object": "chat.completion",
    "created": 1677858242,
    "model": "gpt-4o-mini",
    "usage": {
        "prompt_tokens": 13,
        "completion_tokens": 7,
        "total_tokens": 20
    },
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "\n\nThis is a test!"
            },
            "logprobs": null,
            "finish_reason": "stop",
            "index": 0
        }
    ]
}
```

In this case you simply use Langchain's built-in class `ChatOpenAI` with your custom parameters: `url` and `api_key`.

```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
    base_url=<your url here>,
    api_key=<your key here>,
    model=<your model here>,
    temperature=<your temperature here>
)
```

## Community Model
If there is and implemented python library for the model of your interest then you may use it as well according to the documentation of the package. For example, this is how we implement Yandex models:
- install [yandex-chain library](https://github.com/yandex-datasphere/yandex-chain/tree/main)
- read their docs on how to load specific LLMs
- integrate it to our code

```python
keys = <load yandex api keys>
llm = YandexLLM(
    folder_id=keys["folder_id"],
    api_key=keys["key"],
    model=model,
    temperature=temperature,
    max_tokens=max_tokens
)
```

## Custom API LLM
If you want to integrate our framework with a model which has some custom API schema you have to implement it separately. You may take a reference of how to implement it in [yandex-chain](https://github.com/yandex-datasphere/yandex-chain/blob/main/yandex_chain/YandexGPT.py).

Here we provide a simple example of defining your model, accsessible via API with custom fields. You need to modify `_convert_messages_to_payload` method to match your api schema $-$ specifically the code in the return statement.
```python
from langchain_core.language_models.llms import LLM
from langchain.schema import (
    LLMResult,
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage
)
from typing import List, Optional
import requests


class MyLLMApi(LLM):
    def __init__(self, api_key: str, api_url: str, **kwargs):
        super(LLM).__init__(**kwargs)
        self.api_key = api_key
        self.api_url = api_url

    def _convert_messages_to_payload(self, messages: List[BaseMessage]) -> dict:
        # Convert Langchain message objects to your API format
        api_messages = []
        for message in messages:
            if isinstance(message, HumanMessage):
                role = "user"
            elif isinstance(message, AIMessage):
                role = "assistant"
            elif isinstance(message, SystemMessage):
                role = "system"
            else:
                raise ValueError(f"Unsupported message type: {type(message)}")

            api_messages.append({
                "role": role,
                "content": message.content
            })

        # Return the converted message payload for your specific API
        return {"messages": api_messages}

    def _call_api(self, payload: dict) -> dict:
        # Implement your API request logic here
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(self.api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def _process_api_response(self, response: dict) -> List[AIMessage]:
        # Process API response and convert it to AIMessage objects
        assistant_message = response['message']
        return [AIMessage(content=assistant_message['content'])]

    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None) -> LLMResult:
        # Convert Langchain messages to your API's request payload
        payload = self._convert_messages_to_payload(messages)

        # Make the API request
        response = self._call_api(payload)

        # Process the API response to convert it into Langchain-compatible messages
        output_messages = self._process_api_response(response)

        # Return LLMResult which contains the generated messages
        return LLMResult(generations=[output_messages])

    def invoke(self, message: BaseMessage | str) -> BaseMessage:
        if isinstance(message, str):
            message = HumanMessage(content=message)
        result = self._generate([message])
        return result.generations[0][0]  # Return the first AIMessage

    @property
    def _llm_type(self) -> str:
        return "custom_llm_api"
```






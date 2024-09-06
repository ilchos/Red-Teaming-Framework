# garak vsegpt example
* вставить нужные значения в rest_settings_template.json
    * YOUR_VSE_GPT_KEY - ключ vsegpt
    * YOUR_MODEL_NAME - название модели доступной с vsegpt. Например, "openai/gpt-3.5-turbo-0125"
    * <как надо запарсить выход vsegpt для того чтобы получить текст>. Не знаю для всех ли моделей выход одинаковый, но для модели выше вот такой JSONPath: "$.choices[0].message.content"
* Запустить garak
    ```bash
        garak \
            --model_type rest \
            --generator_option_file rest_settings_template.json \
            --probes dan.Dan_6_0 \
            --report_prefix /Users/kbduvakin/Red-Teaming-Framework/garak_success \
            --verbose \
            --generations 1
    ```

[garak documentation reference](https://reference.garak.ai/en/latest/garak.generators.rest.html)
import gradio as gr
import requests

def submit_url(url, framework):
    # Здесь будет вызов API FastAPI
    response = requests.post("http://backend:8000/test", json={"url": url, "framework": framework})
    return response.json()

def main():

    # with gr.Blocks() as demo:
    #     gr.Markdown("""# 🥇 Leaderboard Component""")
    #     with gr.Tabs():
    #         with gr.Tab("Leaderboard"):
    #             with gr.Row():
    #                 url = gr.Textbox(label="URL")
    #                 framework = gr.Dropdown(choices=["garak", "giskard", "DeepEval"], label="Framework")
    #             with gr.Row():
    #                 submit = gr.Button("Submit")
    #                 result = gr.JSON()
    #             submit.click(submit_url, inputs=[url, framework], outputs=result)

    iface = gr.Interface(
        fn=submit_url,
        inputs=[gr.Textbox(label="URL"), gr.Dropdown(choices=["garak", "giskard", "DeepEval"], label="Framework")],
        outputs=gr.JSON()
    )
    iface.launch(server_name="0.0.0.0")

if __name__ == "__main__":
    main()
import gradio as gr
import requests

# Глобальная переменная для хранения результатов
results = []

def run_red_teaming(model_type, model_name, probes):
    global results
    # Отправка запроса на бэкенд
    response = requests.post("http://backend:8000/test", json={
        "model_type": model_type,
        "model_name": model_name,
        "probes": probes,
    })

    if response.status_code == 200:
        results = response.json()
        return results["result"]
    else:
        return {"error": "Unable to run red teaming tests"}


def clear_blocks(pairs):
    return []

def create_interface():
    with gr.Blocks() as iface:
        with gr.Tabs() as tabs:
            with gr.TabItem("Garak") as garak: 
                with gr.Blocks():
                    gr.Markdown("# LLM Red Teaming")
                    with gr.Row():
                        model_type = gr.Textbox(label="Model Type")
                        model_name = gr.Textbox(label="Model Name")
                        probes = gr.Textbox(label="Probes")
                    run_button = gr.Button("Run Red Teaming")
                    clear_button = gr.Button("Clear Results")

                    pairs = gr.State([])

                    def add_pair(pairs, new_pair):
                        return pairs + new_pair
                    
                    @gr.render(inputs=pairs)
                    def render_pairs(pairs_list):
                        if len(pairs_list) == 0:
                            return
                        with gr.Accordion("Examples"):
                            for pair in pairs_list:
                                with gr.Row():
                                    gr.Textbox(value=pair["prompt"], label="Prompt", interactive=False)
                                    gr.Textbox(value=pair["model_output"], label="Model Output", interactive=False)

                                    delete_btn = gr.Button("Delete", scale=0, variant="stop")
                                    def delete(task=pair):
                                        pairs_list.remove(task)
                                        return pairs_list
                                    delete_btn.click(delete, None, [pairs])

                    def run_and_update(model_type, model_name, probes, pairs):
                        results = run_red_teaming(model_type, model_name, probes)
                        if "error" in results:
                            return [gr.Textbox(value=results["error"], label="Error", interactive=False)]
                        return pairs + results

                    run_button.click(run_and_update, inputs=[model_type, model_name, probes, pairs], outputs=pairs)
                    clear_button.click(clear_blocks, inputs=[pairs], outputs=pairs)

            with gr.TabItem("Leaderboard") as leaderboard:
                pass

    return iface



def main():
    iface = create_interface()
    iface.launch(server_name="0.0.0.0")

if __name__ == "__main__":
    main()
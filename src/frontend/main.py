import gradio as gr
from backend_client import BackendClient
from leaderboard_utils import (
    calculate_leaderboard,
    initialize_leaderboard,
    update_categories,
    update_table,
)
from settings import settings

leaderboard_df_raw, high2low, low2high, leaderboard_table, leaderboard_table_raw = (
    None,
    None,
    None,
    None,
    None,
)


def create_interface():
    global high2low, low2high
    backend_client = BackendClient(settings.backend_url)
    leaderboard_df_raw, high2low, low2high = initialize_leaderboard(backend_client)

    with gr.Blocks() as iface:

        with gr.Tabs():

            with gr.TabItem("Leaderboard"):
                with gr.Blocks():
                    gr.Markdown("# LLM safety leaderboard")
                    with gr.Row():
                        high_level_categories = gr.CheckboxGroup(
                            choices=list(high2low.keys()),
                            value=list(high2low.keys()),
                            label="Select High Level Attack Category",
                            interactive=True,
                        )
                    with gr.Row():
                        low_level_categories = gr.CheckboxGroup(
                            choices=list(low2high.keys()),
                            value=list(low2high.keys()),
                            label="Select Low Level Attack Category",
                            interactive=True,
                        )

                    high_level_categories.change(
                        lambda hlc: update_categories(hlc, high2low),
                        inputs=[high_level_categories],
                        outputs=low_level_categories,
                        queue=True,
                    )

                    with gr.Row():
                        search_bar = gr.Textbox(
                            placeholder=" 🔍 Search for your model and press ENTER...",
                            show_label=False,
                        )
                        manually_tested_visibility = gr.Checkbox(
                            value=True,
                            label="Show manually tested agents",
                            interactive=True,
                        )
                    calculated_leaderboard = calculate_leaderboard(leaderboard_df_raw)
                    leaderboard_table = gr.DataFrame(
                        value=calculated_leaderboard,
                        headers=calculated_leaderboard.columns.to_list(),
                        interactive=False,
                        visible=True,
                        col_count=len(calculated_leaderboard.columns.to_list()),
                    )
                    leaderboard_table_raw = gr.DataFrame(
                        value=leaderboard_df_raw,
                        headers=leaderboard_df_raw.columns.to_list(),
                        visible=False,
                        col_count=len(leaderboard_df_raw.columns.to_list()),
                    )

                    search_bar.submit(
                        update_table,
                        [
                            leaderboard_table_raw,
                            manually_tested_visibility,
                            search_bar,
                            high_level_categories,
                            low_level_categories,
                        ],
                        leaderboard_table,
                    )

                    for selector in [
                        manually_tested_visibility,
                        high_level_categories,
                        low_level_categories,
                    ]:
                        selector.change(
                            update_table,
                            [
                                leaderboard_table_raw,
                                manually_tested_visibility,
                                search_bar,
                                high_level_categories,
                                low_level_categories,
                            ],
                            leaderboard_table,
                        )

            with gr.TabItem("Sumbit"):
                with gr.Blocks():
                    with gr.Row():
                        with gr.Accordion("Automated testing"):
                            pass

                    with gr.Row():
                        with gr.Accordion("Manual testing"):
                            gr.Interface(
                                fn=backend_client.send_file_to_backend,
                                inputs=gr.File(
                                    label="Загрузите файл",
                                    type="binary",
                                ),
                                outputs="text",
                                description="Загрузите файл и посмотрите результат.",
                            )

        def on_load():
            global high2low, low2high
            leaderboard_df_raw, high2low, low2high = initialize_leaderboard(
                backend_client
            )
            result = (
                gr.update(choices=list(high2low.keys()), value=list(high2low.keys())),
                gr.update(choices=list(low2high.keys()), value=list(low2high.keys())),
                gr.update(value=leaderboard_df_raw),
                gr.update(value=calculate_leaderboard(leaderboard_df_raw)),
            )

            return result

        iface.load(
            on_load,
            outputs=[
                high_level_categories,
                low_level_categories,
                leaderboard_table_raw,
                leaderboard_table,
            ],
        )
    return iface


def main():
    iface = create_interface()
    iface.launch(server_name="0.0.0.0")


if __name__ == "__main__":
    main()

import gradio as gr
import pandas as pd
from backend_client import BackendClient
from leaderboard_utils import get_categories_mapping, update_categories, update_table


def create_interface():
    backend_client = BackendClient("http://backend:8000")

    leaderboard_competitors = backend_client.fetch_leaderboard_competitors()
    leaderboard_df_raw = pd.DataFrame(leaderboard_competitors).sort_values(
        "hit_rate", ascending=True
    )
    high2mid, mid2low, low2high = get_categories_mapping(leaderboard_df_raw)

    with gr.Blocks() as iface:
        with gr.Tabs():
            with gr.TabItem("Leaderboard"):
                with gr.Blocks():
                    gr.Markdown("# LLM safety leaderboard")
                    with gr.Row():
                        high_level_categories = gr.CheckboxGroup(
                            choices=list(high2mid.keys()),
                            value=list(high2mid.keys()),
                            label="Select High Level Attack Category",
                            interactive=True,
                        )
                    with gr.Row():
                        mid_level_categories = gr.CheckboxGroup(
                            choices=list(mid2low.keys()),
                            value=list(mid2low.keys()),
                            label="Select Mid Level Attack Category",
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
                        lambda hlc, mlc: update_categories(
                            hlc,
                            mlc,
                            "high_level_category",
                            high2mid,
                            mid2low,
                        ),
                        inputs=[
                            high_level_categories,
                            mid_level_categories,
                        ],
                        outputs=[mid_level_categories, low_level_categories],
                        queue=True,
                    )
                    mid_level_categories.change(
                        lambda hlc, mlc: update_categories(
                            hlc,
                            mlc,
                            "mid_level_category",
                            high2mid,
                            mid2low,
                        ),
                        inputs=[
                            high_level_categories,
                            mid_level_categories,
                        ],
                        outputs=low_level_categories,
                        queue=True,
                    )

                    with gr.Row():
                        search_bar = gr.Textbox(
                            placeholder=" 🔍 Search for your model and press ENTER...",
                            show_label=False,
                        )
                        shown_columns = gr.CheckboxGroup(
                            choices=[
                                "passed",
                                "total",
                                "hit_rate",
                                "low_level_category",
                                "mid_level_category",
                                "high_level_category",
                            ],
                            value=[
                                "hit_rate",
                                "high_level_category",
                                "mid_level_category",
                                "low_level_category",
                            ],
                            label="Select columns to show",
                            interactive=True,
                        )
                        manually_tested_visibility = gr.Checkbox(
                            value=True,
                            label="Show manually tested agents",
                            interactive=True,
                        )
                    leaderboard_table = gr.DataFrame(
                        value=leaderboard_df_raw[["model_name"] + shown_columns.value],
                        headers=["model_name"] + shown_columns.value,
                        interactive=False,
                        visible=True,
                    )
                    leaderboard_table_raw = gr.DataFrame(
                        value=leaderboard_df_raw,
                        headers=leaderboard_df_raw.columns.to_list(),
                        visible=False,
                    )

                    search_bar.submit(
                        update_table,
                        [
                            leaderboard_table_raw,
                            shown_columns,
                            manually_tested_visibility,
                            search_bar,
                            high_level_categories,
                            mid_level_categories,
                            low_level_categories,
                        ],
                        leaderboard_table,
                    )

                    for selector in [
                        shown_columns,
                        manually_tested_visibility,
                        high_level_categories,
                        mid_level_categories,
                        low_level_categories,
                    ]:
                        selector.change(
                            update_table,
                            [
                                leaderboard_table_raw,
                                shown_columns,
                                manually_tested_visibility,
                                search_bar,
                                high_level_categories,
                                mid_level_categories,
                                low_level_categories,
                            ],
                            leaderboard_table,
                        )

    return iface


def main():
    iface = create_interface()
    iface.launch(server_name="0.0.0.0")


if __name__ == "__main__":
    main()

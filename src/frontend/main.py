from functools import partial

import gradio as gr
import requests
import pandas as pd


# Глобальная переменная для хранения результатов
results = []

def fetch_options_from_backend():
    # Пример запроса к бэкенду (замените URL на ваш бэкенд)
    response = requests.get("http://backend:8000/garak_list_probes")
    if response.status_code == 200:
        return response.json()["result"]
    else:
        return []
    
def fetch_models_from_backend():
    # Пример запроса к бэкенду (замените URL на ваш бэкенд)
    response = requests.get("http://backend:8000/models_list")
    if response.status_code == 200:
        return response.json()["result"]
    else:
        return []

def fetch_leaderboard_competitors():
    response = requests.get("http://backend:8000/leaderboard_competitors")
    if response.status_code == 200:
        return response.json()["result"]
    else:
        return []
    
def fetch_leaderboard_categories_tree():
    response = requests.get("http://backend:8000/leaderboard_categories")
    if response.status_code == 200:
        results = response.json()
        return results # TODO: fix it
    else:
        return {}

def run_red_teaming(model_name, probes):
    global results
    # Отправка запроса на бэкенд
    response = requests.post("http://backend:8000/test", json={
        "model_name": model_name,
        "probes": probes,
    })

    if response.status_code == 200:
        results = response.json()
        return results["hitlog"], results["evals"]
    else:
        return [], []
    
def run_leaderboard_tests(model_name):
    # Отправка запроса на бэкенд
    response = requests.post("http://backend:8000/test_leaderboard", json={
        "model_name": model_name,
    })

    if response.status_code == 200:
        results = response.json()["evals"]
        print(f"LEADERBOARD TESTS RESULT: {results}")
        return results
    else:
        return [], []


def clear_blocks(hitlog, evals):
    return [], []


def update_table(
        df, 
        columns, 
        show_mannual_tested: bool, 
        query, 
        high_level_categories,
        mid_level_categories,
        low_level_categories,
    ):
    print("-"* 100)
    print(f"high_level_categories selected: {high_level_categories}")
    print(f"mid_level_categories selected: {mid_level_categories}")
    print(f"low_level_categories selected: {low_level_categories}")
    print("-"* 100)

    if not show_mannual_tested:
        filtered_df = df[df["manually_tested"] == False]
    else:
        filtered_df = df

    mask = (
        filtered_df["high_level_category"].isin(high_level_categories) &
        filtered_df["mid_level_category"].isin(mid_level_categories) &
        filtered_df["low_level_category"].isin(low_level_categories) &
        filtered_df["model_name"].str.contains(query)
    )

    filtered_df = filtered_df[mask]

    result = filtered_df[["model_name"] + columns]

    print(f"UPDATE DATA TYPE: {type(result)}")

    return result

def get_categories_mapping(df):

    high2mid = (
        df
        .groupby("high_level_category")["mid_level_category"]
        .apply(list)
        .to_dict()
    )
    mid2low = (
        df
        .groupby("mid_level_category")["low_level_category"]
        .apply(list)
        .to_dict()
    )
    low2high = (
        df
        .groupby("low_level_category")["high_level_category"]
        .apply(list)
        .to_dict()
    )
    low2mid = (
        df
        .groupby("low_level_category")["mid_level_category"]
        .apply(list)
        .to_dict()
    )
    mid2high = (
        df
        .groupby("mid_level_category")["high_level_category"]
        .apply(list)
        .to_dict()
    )

    return high2mid, mid2low, low2high, low2mid, mid2high

def update_categories(
        high_level_categories,
        mid_level_categories,
        low_level_categories,
        cat_level,
        high2mid, 
        mid2low, 
        low2high, 
        low2mid, 
        mid2high,
    ):
    if cat_level == "high_level_category":
        mid_levels_list = set()
        for hlc in high_level_categories:
            for item in high2mid[hlc]:
                mid_levels_list.add(item)
        mid_levels_list = list(mid_levels_list)

        low_levels_list = set()
        for mlc in mid_levels_list:
            for item in mid2low[mlc]:
                low_levels_list.add(item)

        low_levels_list = list(low_levels_list)
        return gr.update(choices=mid_levels_list, value=mid_levels_list), gr.update(choices=low_levels_list, value=low_levels_list)

    elif cat_level == "mid_level_category":

        low_levels_list = set()
        for mlc in mid_level_categories:
            for item in mid2low[mlc]:
                low_levels_list.add(item)

        low_levels_list = list(low_levels_list)

        return gr.update(choices=low_levels_list, value=low_levels_list)



def create_interface():

    probe_options = fetch_options_from_backend()
    list_models = fetch_models_from_backend()
    leaderboard_competitors = fetch_leaderboard_competitors()
    leaderboard_df_raw = pd.DataFrame(leaderboard_competitors).sort_values("hit_rate", ascending=True)

    high2mid, mid2low, low2high, low2mid, mid2high = get_categories_mapping(leaderboard_df_raw)

    print(f"FRONTEND leaderboard_df.columns: {leaderboard_df_raw.columns}")

    with gr.Blocks(css="#bad_score {font-color: red;}\n#good_score {font-color: green;}") as iface:
        with gr.Tabs() as tabs:
            with gr.TabItem("Garak") as garak:
                with gr.Blocks():
                    gr.Markdown("# LLM Red Teaming")
                    with gr.Row():
                        model_name = gr.Dropdown(choices=list_models, label="Model Name", multiselect=False)

                    with gr.Row():
                        probes = gr.Dropdown(choices=probe_options, label="Probes", multiselect=True)

                    run_button = gr.Button("Run Red Teaming")
                    clear_button = gr.Button("Clear Results")

                    evals = gr.State([])
                    @gr.render(inputs=evals)
                    def render_evals(evals_list):
                        if len(evals_list) == 0:
                            return
                        df = pd.DataFrame(evals_list)
                        with gr.Accordion("Evals Statistic"):
                            gr.Dataframe(
                                value=df,
                                headers=df.columns.tolist(), 
                                row_count=(5, "fixed"), 
                                col_count=(len(df.columns), "fixed")
                            )
                        # with gr.Accordion("Evals"):
                        #     for eval_item in evals_list:
                        #         with gr.Row():
                        #             elem_id = "good_score"
                        #             if float(eval_item["passed"]) / float(eval_item["total"]) < 0.5:
                        #                 elem_id = "bad_score" 
                        #             gr.Textbox(value=eval_item["probe"], label="probe", interactive=False, elem_id=elem_id)
                        #             gr.Textbox(value=eval_item["detector"], label="detector", interactive=False, elem_id=elem_id)
                        #             gr.Textbox(value=eval_item["passed"], label="passed", interactive=False, elem_id=elem_id)
                        #             gr.Textbox(value=eval_item["total"], label="total", interactive=False, elem_id=elem_id)

                    hitlog = gr.State([])
                    @gr.render(inputs=hitlog)
                    def render_hitlog(hitlog_list):
                        if len(hitlog_list) == 0:
                            return
                    
                        with gr.Accordion("Hitlog"):
                            for hitlog_item in hitlog_list:
                                with gr.Column():
                                    with gr.Row():
                                        gr.Textbox(value=hitlog_item["probe"], label="Probe", interactive=False)
                                        gr.Textbox(value=hitlog_item["detector"], label="Detector", interactive=False)
                                        gr.Textbox(value=hitlog_item["score"], label="Score", interactive=False)

                                        delete_btn = gr.Button("Delete", scale=0, variant="stop")
                                        def delete(task=hitlog_item):
                                            hitlog_list.remove(task)
                                            return hitlog_list
                                        delete_btn.click(delete, None, [hitlog])

                                    
                                    gr.Textbox(value=hitlog_item["prompt"], label="Prompt", interactive=False, max_lines=10)
                                    gr.Textbox(value=hitlog_item["output"], label="Model Output", interactive=False, max_lines=10)


                    def run_and_update(model_name, probes, hitlog_, evals_):
                        hitlog, evals = run_red_teaming(model_name, probes)

                        if len(hitlog) == 0 and len(evals) == 0:
                            return [gr.Textbox(value=results["error"], label="Error", interactive=False)]
                        return [hitlog_ + hitlog, evals_ + evals]

                    run_button.click(run_and_update, inputs=[model_name, probes, hitlog, evals], outputs=[hitlog, evals])
                    clear_button.click(clear_blocks, inputs=[hitlog, evals], outputs=[hitlog, evals])

            with gr.TabItem("Leaderboard Old") as old_leaderboard:
                with gr.Blocks():
                    gr.Markdown("# LLM safety leaderboard")
                    with gr.Row():
                        model_name = gr.Dropdown(choices=list_models, label="Model Name", multiselect=False)
                        run_button = gr.Button("Run Red Teaming")
                    
                    competitions = gr.State([])

                    @gr.render(inputs=competitions)
                    def render_leaderboard(competitors_list):
                        if len(competitors_list) == 0:
                            return
                        
                        df = pd.DataFrame(competitors_list)
                        df_tmp = (
                            df
                            .groupby(["probe", "model_name"])
                            .agg({
                                "passed": "sum",
                                "total": "sum",
                            })
                            .reset_index()
                        )
                        df_tmp["hit_rate"] = 1.0 - df_tmp["passed"] / df_tmp["total"]
                        df_tmp.sort_values("hit_rate", ascending=True, inplace=True)
                        print(f"DF_COLUMNS: {df_tmp.columns}")
                        print(f"DF: {df_tmp}")
                        # df = df[["probe", ""]]
                        with gr.Accordion("Leaderboard"):
                            gr.Dataframe(
                                value=df_tmp,
                                headers=df_tmp.columns.tolist(), 
                                row_count=(df_tmp.shape[0], "fixed"), 
                                col_count=(len(df_tmp.columns), "fixed")
                            )

                        # TODO: create leaderboard

                    def run_and_update_leaderboard(model_name, _competitions):
                        competitions = run_leaderboard_tests(model_name)

                        if "error" in competitions:
                            return [gr.Textbox(value=results["error"], label="Error", interactive=False)]
                        
                        return _competitions + competitions
                    
                    run_button.click(run_and_update_leaderboard, inputs=[model_name, competitions], outputs=[competitions])

            with gr.TabItem("Leaderboard") as leaderboard:
                with gr.Blocks():
                    gr.Markdown("# LLM safety leaderboard")
                    with gr.Row():
                        high_level_categories = gr.CheckboxGroup(
                            choices=list(high2mid.keys()),
                            value=list(high2mid.keys()),
                            label="Select High Level Attack Category",
                            interactive=True
                        )
                    with gr.Row():
                        mid_level_categories = gr.CheckboxGroup(
                            choices=list(mid2low.keys()),
                            value=list(mid2low.keys()),
                            label="Select High Level Attack Category",
                            interactive=True
                        ) 
                    with gr.Row():
                        low_level_categories = gr.CheckboxGroup(
                            choices=list(low2high.keys()),
                            value=list(low2high.keys()),
                            label="Select High Level Attack Category",
                            interactive=True
                        )         

                    high_level_categories.change(
                        partial(
                            update_categories, 
                            cat_level="high_level_category",
                            high2mid=high2mid,
                            mid2low=mid2low,
                            low2high=low2high,
                            low2mid=low2mid,
                            mid2high=mid2high,
                        ),
                        inputs=[
                            high_level_categories,
                            mid_level_categories,
                            low_level_categories,
                        ],
                        outputs=[mid_level_categories, low_level_categories],
                        queue=True
                    ) 
                    mid_level_categories.change(
                        partial(
                            update_categories, 
                            cat_level="mid_level_category",
                            high2mid=high2mid,
                            mid2low=mid2low,
                            low2high=low2high,
                            low2mid=low2mid,
                            mid2high=mid2high,
                        ),
                        inputs=[
                            high_level_categories,
                            mid_level_categories,
                            low_level_categories,
                        ],
                        outputs=low_level_categories,
                        queue=True
                    ) 
                    # low_level_categories.change(
                    #     partial(
                    #         update_categories, 
                    #         cat_level="low_level_category",
                    #         high2mid=high2mid,
                    #         mid2low=mid2low,
                    #         low2high=low2high,
                    #         low2mid=low2mid,
                    #         mid2high=mid2high,
                    #     ),
                    #     inputs=[
                    #         high_level_categories,
                    #         mid_level_categories,
                    #         low_level_categories,
                    #     ],
                    #     outputs=[mid_level_categories, high_level_categories],
                    #     queue=True
                    # ) 
                    with gr.Row():
                        search_bar = gr.Textbox(
                            placeholder=" 🔍 Search for your model (separate multiple queries with `;`) and press ENTER...",
                            show_label=False,
                        )
                        shown_columns = gr.CheckboxGroup(
                            choices=["passed", "total", "hit_rate", "low_level_category", "mid_level_category", "high_level_category"],
                            value=["hit_rate", "high_level_category", "mid_level_category", "low_level_category"],
                            label="Select columns to show",
                            interactive=True,
                        )
                        mannualy_tested_visibility = gr.Checkbox(
                            value=True,
                            label="Show mannualy tested agents",
                            interactive=True
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
                            mannualy_tested_visibility,
                            search_bar,
                            high_level_categories,
                            mid_level_categories,
                            low_level_categories,
                        ],
                        leaderboard_table,
                    )

                    for selector in [shown_columns, mannualy_tested_visibility, high_level_categories, mid_level_categories, low_level_categories]:
                        selector.change(
                            update_table,
                            [
                                leaderboard_table_raw,
                                shown_columns,
                                mannualy_tested_visibility,
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
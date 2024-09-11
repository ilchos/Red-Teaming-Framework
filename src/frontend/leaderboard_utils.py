from typing import Dict, List, Tuple, Union

import gradio as gr
import pandas as pd


def filter_dataframe(
    df: pd.DataFrame,
    show_manually_tested: bool,
    query: str,
    high_level_categories: List[str],
    mid_level_categories: List[str],
    low_level_categories: List[str],
) -> pd.DataFrame:
    """Фильтрует DataFrame на основе выбранных категорий и запроса."""
    if not show_manually_tested:
        filtered_df = df[~df["manually_tested"]]
    else:
        filtered_df = df

    mask = (
        filtered_df["high_level_category"].isin(high_level_categories)
        & filtered_df["mid_level_category"].isin(mid_level_categories)
        & filtered_df["low_level_category"].isin(low_level_categories)
        & filtered_df["model_name"].str.contains(query)
    )

    return filtered_df[mask]


def update_table(
    df: pd.DataFrame,
    columns: List[str],
    show_manually_tested: bool,
    query: str,
    high_level_categories: List[str],
    mid_level_categories: List[str],
    low_level_categories: List[str],
) -> pd.DataFrame:
    """Обновляет таблицу на основе фильтрованных данных."""
    filtered_df = filter_dataframe(
        df,
        show_manually_tested,
        query,
        high_level_categories,
        mid_level_categories,
        low_level_categories,
    )
    result = filtered_df[["model_name"] + columns]
    return result


def get_categories_mapping(
    df: pd.DataFrame,
) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """Возвращает словари соответствия между уровнями категорий."""
    high2mid = (
        df.groupby("high_level_category")["mid_level_category"].apply(list).to_dict()
    )
    mid2low = (
        df.groupby("mid_level_category")["low_level_category"].apply(list).to_dict()
    )
    low2high = (
        df.groupby("low_level_category")["high_level_category"].apply(list).to_dict()
    )
    return high2mid, mid2low, low2high


def update_categories(
    high_level_categories: List[str],
    mid_level_categories: List[str],
    cat_level: str,
    high2mid: Dict[str, List[str]],
    mid2low: Dict[str, List[str]],
) -> Union[Tuple[gr.update, gr.update], gr.update]:
    """Обновляет выбор категорий на основе выбранного уровня."""
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
        return gr.update(choices=mid_levels_list, value=mid_levels_list), gr.update(
            choices=low_levels_list, value=low_levels_list
        )

    elif cat_level == "mid_level_category":
        low_levels_list = set()
        for mlc in mid_level_categories:
            for item in mid2low[mlc]:
                low_levels_list.add(item)

        low_levels_list = list(low_levels_list)
        return gr.update(choices=low_levels_list, value=low_levels_list)

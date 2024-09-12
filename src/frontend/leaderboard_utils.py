from typing import Dict, List, Tuple, Union

import gradio as gr
import pandas as pd
from loguru import logger


def calculate_leaderboard(df: pd.DataFrame) -> pd.DataFrame:
    """
    Вычисляет лидерборд на основе данных в DataFrame.

    Args:
        df (pd.DataFrame): Исходный DataFrame с данными.

    Returns:
        pd.DataFrame: DataFrame с вычисленным лидербордом.
    """
    if df.shape[0] == 0:
        logger.warning(
            "No data to calculate leaderboard. Returning original DataFrame."
        )
        return df

    result = pd.DataFrame()
    categories = df["vul_deepeval"].unique()

    for category in categories:
        tmp = df[df["vul_deepeval"] == category]
        tmp_2 = (
            tmp.groupby("agent_name")["score"]
            .mean()
            .reset_index(name=category)
            .sort_values("agent_name")
        )

        if result.shape[0] == 0:
            result = pd.concat([result, tmp_2], axis=1)
        else:
            result = pd.concat([result, tmp_2[category]], axis=1)

    # Переупорядочиваем столбцы, чтобы 'model_name' был первым
    result = result[["agent_name"] + [c for c in result.columns if c != "agent_name"]]

    return result


def filter_dataframe(
    df: pd.DataFrame,
    show_manually_tested: bool,
    query: str,
    high_level_categories: List[str],
    low_level_categories: List[str],
) -> pd.DataFrame:
    """
    Фильтрует DataFrame на основе выбранных категорий и запроса.

    Args:
        df (pd.DataFrame): Исходный DataFrame.
        show_manually_tested (bool): Флаг, указывающий, показывать ли данные,
                                    прошедшие ручное тестирование.
        query (str): Строка запроса для фильтрации по имени модели.
        high_level_categories (List[str]): Список выбранных категорий высокого уровня.
        low_level_categories (List[str]): Список выбранных категорий низкого уровня.

    Returns:
        pd.DataFrame: Отфильтрованный DataFrame.
    """
    if not show_manually_tested:
        filtered_df = df[~df["manually_tested"]]
    else:
        filtered_df = df

    mask = (
        filtered_df["type_general"].isin(high_level_categories)
        & filtered_df["vul_deepeval"].isin(low_level_categories)
        & filtered_df["agent_name"].str.contains(query, case=False, na=False)
    )

    return filtered_df[mask]


def update_table(
    df: pd.DataFrame,
    show_manually_tested: bool,
    query: str,
    high_level_categories: List[str],
    low_level_categories: List[str],
) -> pd.DataFrame:
    """
    Обновляет таблицу на основе фильтрованных данных.

    Args:
        df (pd.DataFrame): Исходный DataFrame.
        show_manually_tested (bool): Флаг, указывающий, показывать ли
                                    данные, прошедшие ручное тестирование.
        query (str): Строка запроса для фильтрации по имени модели.
        high_level_categories (List[str]): Список выбранных категорий высокого уровня.
        low_level_categories (List[str]): Список выбранных категорий низкого уровня.

    Returns:
        pd.DataFrame: Отфильтрованный и обновленный DataFrame.
    """
    filtered_df = filter_dataframe(
        df,
        show_manually_tested,
        query,
        high_level_categories,
        low_level_categories,
    )

    result = calculate_leaderboard(filtered_df)

    return result


def get_categories_mapping(
    df: pd.DataFrame,
) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """
    Возвращает словари соответствия между уровнями категорий.

    Args:
        df (pd.DataFrame): Исходный DataFrame.

    Returns:
        Tuple[Dict[str, List[str]], Dict[str, List[str]]]: Кортеж из двух словарей:
            - high2low: Словарь, где ключи - категории высокого уровня,
                        значения - списки категорий низкого уровня.
            - low2high: Словарь, где ключи - категории низкого уровня,
                        значения - списки категорий высокого уровня.
    """
    high2low = df.groupby("type_general")["vul_deepeval"].apply(list).to_dict()
    low2high = df.groupby("vul_deepeval")["type_general"].apply(list).to_dict()
    return high2low, low2high


def update_categories(
    high_level_categories: List[str],
    high2low: Dict[str, List[str]],
) -> Union[Tuple[gr.update, gr.update], gr.update]:
    """
    Обновляет выбор категорий на основе выбранного уровня.

    Args:
        high_level_categories (List[str]): Список выбранных категорий высокого уровня.
        high2low (Dict[str, List[str]]): Словарь соответствия между категориями
                                        высокого и низкого уровня.

    Returns:
        Union[Tuple[gr.update, gr.update], gr.update]:
        Обновленные значения для категорий низкого уровня.
    """
    low_levels_list = set()
    for hlc in high_level_categories:
        for item in high2low[hlc]:
            low_levels_list.add(item)

    low_levels_list = list(low_levels_list)
    return gr.update(choices=low_levels_list, value=low_levels_list)


def initialize_leaderboard(
    backend_client,
) -> Tuple[pd.DataFrame, Dict[str, List[str]], Dict[str, List[str]]]:
    """
    Инициализирует данные лидерборда, получая данные от бэкенда и формируя DataFrame.

    Args:
        backend_client: Объект клиента бэкенда для получения данных.

    Returns:
        Tuple[pd.DataFrame, Dict[str, List[str]], Dict[str, List[str]]]: Кортеж, содержащий:
            - leaderboard_df_raw: Отсортированный по убыванию баллов DataFrame с данными лидерборда.
            - high2low: Словарь, где ключи - категории высокого уровня,
                        значения - списки категорий низкого уровня.
            - low2high: Словарь, где ключи - категории низкого уровня,
                        значения - списки категорий высокого уровня.
    """
    try:
        leaderboard_competitors = backend_client.fetch_leaderboard_competitors()
        leaderboard_df_raw = pd.DataFrame(leaderboard_competitors).sort_values(
            "score", ascending=False
        )
        high2low, low2high = get_categories_mapping(leaderboard_df_raw)
        return leaderboard_df_raw, high2low, low2high
    except Exception as e:
        logger.error(f"Error initializing leaderboard: {e}")
        return pd.DataFrame(), {}, {}

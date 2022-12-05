from datetime import datetime, timezone

try:
    from IPython.display import display
except ImportError:
    display = print
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

mapping = {
    "Context_source": "SourceFlowContext",
    "Context_target": "TargetFlowContext",
    "Flow UUID_source": "SourceFlowUUID",
    "Flow UUID_target": "TargetFlowUUID",
    "Flowable_source": "SourceFlowName",
    "Flowable_target": "TargetFlowName",
    "Unit_source": "SourceUnit",
    "Unit_target": "TargetUnit",
}


def merge_by_uuid(source: pd.DataFrame, target: pd.DataFrame) -> pd.DataFrame:
    """Get inner join of two DataFrames where the column ``Flow UUID`` has the same value.

    Adds columns ``SourceFlowUUID`` and ``TargetFlowUUID``, and drops ``Flow UUID``."""
    merged = pd.merge(
        source, target, how="inner", on=["Flow UUID"], suffixes=("_source", "_target")
    )

    merged["SourceFlowUUID"] = merged["Flow UUID"]
    merged["TargetFlowUUID"] = merged["Flow UUID"]
    merged.rename(
        columns={k: v for k, v in mapping.items() if k in merged.columns}, inplace=True
    )

    return merged.drop(columns=["Flow UUID"])


def merge_by_name_context(source: pd.DataFrame, target: pd.DataFrame) -> pd.DataFrame:
    """Get inner join of two DataFrames where the columns ``Flowable`` **and** ``Context`` has the same value.

    Adds columns ``(Target|Source)Flowable`` and ``(Source|Target)Context``, and drops the columns used for matching."""
    extra = pd.merge(
        source,
        target,
        how="inner",
        on=["Flowable", "Context"],
        suffixes=("_source", "_target"),
    )

    extra["TargetFlowName"] = extra["Flowable"]
    extra["SourceFlowName"] = extra["Flowable"]
    extra["TargetContext"] = extra["Context"]
    extra["SourceContext"] = extra["Context"]
    extra.rename(
        columns={k: v for k, v in mapping.items() if k in extra.columns}, inplace=True
    )

    return extra.drop(columns=["Flowable", "Context"])


def test_unit_change(data: pd.DataFrame) -> None:
    changed_units = data["SourceUnit"] != data["TargetUnit"]
    if changed_units.sum():
        print("Inconsistent units, fix manually")
        display(
            data[changed_units][
                [
                    "SourceFlowName",
                    "SourceFlowUUID",
                    "SourceFlowContext",
                    "SourceUnit",
                    "TargetFlowName",
                    "TargetFlowUUID",
                    "TargetFlowContext",
                    "TargetUnit",
                ]
            ]
        )


def get_different_flows(dataframe: pd.DataFrame, already: pd.DataFrame, list_name: str, mode: str="Source") -> pd.DataFrame:
    opposite = "Target" if mode == "Source" else "Source"

    new_rows = filter_by_dataframe_attribute(
        filter_by_dataframe_attribute(dataframe, already, ["Flow UUID"], [f"{mode}FlowUUID"]),
        already,
        ["Flowable", "Context"],
        [f"{mode}FlowName", f"{mode}FlowContext"]
    )
    new_rows["MatchCondition"] = "!"
    new_rows["ConversionFactor"] = np.NaN
    new_rows[f"{mode}ListName"] = list_name
    new_rows[f"{opposite}ListName"] = ""

    for src, trgt in [
        ("Flowable", "{}FlowName"),
        ("Flow UUID", "{}FlowUUID"),
        ("Context", "{}FlowContext"),
        ("Unit", "{}Unit"),
    ]:
        new_rows[trgt.format(mode)] = new_rows[src]
        new_rows[trgt.format(opposite)] = ""

    return new_rows


def prepare_final_form(data: pd.DataFrame) -> pd.DataFrame:
    SPEC_COLUMNS = [
        "SourceListName",
        "SourceFlowName",
        "SourceFlowUUID",
        "SourceFlowContext",
        "SourceUnit",
        "MatchCondition",
        "ConversionFactor",
        "TargetListName",
        "TargetFlowName",
        "TargetFlowUUID",
        "TargetFlowContext",
        "TargetUnit",
        "Mapper",
        "Verifier",
        "LastUpdated",
        "MemoMapper",
        "MemoVerifier",
        "MemoSource",
        "MemoTarget",
    ]

    data_selected = data.copy()[[col for col in SPEC_COLUMNS if col in data.columns]]
    data_selected.sort_values(
        by=["SourceFlowName", "SourceFlowContext", "SourceUnit"],
        inplace=True,
        ignore_index=True,
    )
    return data_selected


def combination_flowable_context_unique(dataframe: pd.DataFrame) -> None:
    """Make sure that the combination of columns ``Flowable`` and ``Context`` are unique.

    Raises ``ValueError`` is this condition is not met."""
    combo = dataframe[["Flowable", "Context"]].drop_duplicates()
    if len(dataframe) != len(combo):
        raise ValueError


def filter_by_dataframe_attribute(
    target_df: pd.DataFrame,
    filter_df: pd.DataFrame,
    filter_columns_target_df: List[str],
    filter_columns_filter_df: List[str],
) -> pd.DataFrame:
    """Filter ``target_df`` to exclude rows whose ``filter_colums`` attributes match those in ``filter_df``.

    Returns a DataFrame."""
    return target_df[
        ~pd.MultiIndex.from_frame(target_df[filter_columns_target_df]).isin(
            filter_df[filter_columns_filter_df].drop_duplicates().apply(tuple, axis=1)
        )
    ].reset_index(drop=True)


def merge_dataframes(
    source: pd.DataFrame,
    target: pd.DataFrame,
    source_list_name: str,
    target_list_name: str,
    author: str,
) -> pd.DataFrame:
    combination_flowable_context_unique(source)
    combination_flowable_context_unique(target)

    merged = merge_by_uuid(source=source, target=target)

    extra = merge_by_name_context(
        source=filter_by_dataframe_attribute(source, merged, ["Flow UUID"], ["SourceFlowUUID"]),
        target=filter_by_dataframe_attribute(target, merged, ["Flow UUID"], ["TargetFlowUUID"]),
    )

    data = pd.concat([merged, extra])
    data["MatchCondition"] = "="
    data["ConversionFactor"] = 1.0
    data["SourceListName"] = source_list_name
    data["TargetListName"] = target_list_name

    test_unit_change(data)

    source_flows_removed = get_different_flows(
        dataframe=source, already=data, list_name=source_list_name
    )
    target_flows_added = get_different_flows(
        dataframe=target, already=data, list_name=target_list_name, mode="Target"
    )

    data = pd.concat([data, source_flows_removed, target_flows_added])

    data["Mapper"] = author
    data["Verifier"] = ""
    data["LastUpdated"] = datetime.now(timezone.utc).astimezone().isoformat()
    data["MemoMapper"] = "Automated match"
    data["MemoSource"] = ""
    data["MemoTarget"] = ""
    data["MemoVerifier"] = ""

    return prepare_final_form(data)

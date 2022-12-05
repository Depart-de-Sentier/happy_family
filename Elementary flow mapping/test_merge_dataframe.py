from merge_dataframes import (
    merge_dataframes,
    merge_by_uuid,
    merge_by_name_context,
    filter_by_dataframe_attribute,
)
import pandas as pd
from pandas.testing import assert_frame_equal


def test_merge_dataframes_uuid_match():
    first = pd.DataFrame(
        [
            {
                "Flow UUID": "1",
                "Name first": "foo",
            },
            {
                "Flow UUID": "2",
                "Name first": "bar",
            },
        ]
    )
    second = pd.DataFrame(
        [
            {
                "Flow UUID": "1",
                "Name second": "foo",
            },
            {
                "Flow UUID": "3",
                "Name second": "baz",
            },
        ]
    )
    expected = pd.DataFrame(
        [
            {
                "Name first": "foo",
                "Name second": "foo",
                "SourceFlowUUID": "1",
                "TargetFlowUUID": "1",
            },
        ]
    )
    result = merge_by_uuid(first, second)
    assert_frame_equal(result, expected)


def test_merge_dataframes_renaming():
    first = pd.DataFrame(
        [
            {
                "Flow UUID": "1",
                "Flowable": "foo",
            },
        ]
    )
    second = pd.DataFrame(
        [
            {
                "Flow UUID": "1",
                "Flowable": "foo",
            },
        ]
    )
    expected = pd.DataFrame(
        [
            {
                "SourceFlowName": "foo",
                "TargetFlowName": "foo",
                "SourceFlowUUID": "1",
                "TargetFlowUUID": "1",
            },
        ]
    )
    result = merge_by_uuid(first, second)
    assert_frame_equal(result, expected)


def test_merge_by_name_context_match():
    first = pd.DataFrame(
        [
            {
                "Flowable": "fish",
                "Context": "foo|bar",
                "Unit": "one",
            },
            {
                "Flowable": "squid",
                "Context": "foo|bar",
            },
        ]
    )
    second = pd.DataFrame(
        [
            {
                "Flowable": "fish",
                "Context": "foo|bar",
                "Unit": "two",
            },
        ]
    )
    expected = pd.DataFrame(
        [
            {
                "SourceUnit": "one",
                "TargetUnit": "two",
                "TargetFlowName": "fish",
                "SourceFlowName": "fish",
                "TargetContext": "foo|bar",
                "SourceContext": "foo|bar",
            },
        ]
    )
    result = merge_by_name_context(first, second)
    assert_frame_equal(result, expected)


def test_filter_by_dataframe_attribute_multicolumn():
    given = pd.DataFrame(
        [
            {
                "Flowable": "a",
                "Context": "b/c",
                "Flow UUID": "d",
            },
            {
                "Flowable": "a",
                "Context": "e/f",
                "Flow UUID": "g",
            },
            {
                "Flowable": "h",
                "Context": "b/c",
                "Flow UUID": "i",
            },
        ]
    )
    filter_df = pd.DataFrame(
        [
            {
                "Flowable": "a",
                "Context": "b/c",
                "Flow UUID": "d",
            },
            {
                "Flowable": "a",
                "Context": "e/f",
                "Flow UUID": "g",
            },
        ]
    )
    expected = pd.DataFrame(
        [
            {
                "Flowable": "h",
                "Context": "b/c",
                "Flow UUID": "i",
            }
        ]
    )
    result = filter_by_dataframe_attribute(
        given, filter_df, ["Flowable", "Context"], ["Flowable", "Context"]
    )
    assert_frame_equal(result, expected)


def test_filter_by_dataframe_attribute_different_labels():
    given = pd.DataFrame(
        [
            {
                "Flowable": "a",
                "Context": "b/c",
                "Flow UUID": "d",
            },
            {
                "Flowable": "a",
                "Context": "e/f",
                "Flow UUID": "g",
            },
            {
                "Flowable": "h",
                "Context": "b/c",
                "Flow UUID": "i",
            },
        ]
    )
    filter_df = pd.DataFrame(
        [
            {
                "foo": "a",
                "bar": "b/c",
                "Flow UUID": "d",
            },
            {
                "foo": "a",
                "bar": "e/f",
                "Flow UUID": "g",
            },
        ]
    )
    expected = pd.DataFrame(
        [
            {
                "Flowable": "h",
                "Context": "b/c",
                "Flow UUID": "i",
            }
        ]
    )
    result = filter_by_dataframe_attribute(
        given, filter_df, ["Flowable", "Context"], ["foo", "bar"]
    )
    assert_frame_equal(result, expected)


def test_filter_by_dataframe_attribute_single_column():
    given = pd.DataFrame(
        [
            {
                "Flowable": "a",
                "Context": "b/c",
                "Flow UUID": "d",
            },
            {
                "Flowable": "a",
                "Context": "e/f",
                "Flow UUID": "g",
            },
            {
                "Flowable": "h",
                "Context": "b/c",
                "Flow UUID": "i",
            },
        ]
    )
    filter_df = pd.DataFrame(
        [
            {
                "Flowable": "a",
                "Context": "b/c",
                "Flow UUID": "d",
            },
            {
                "Flowable": "a",
                "Context": "e/f",
                "Flow UUID": "g",
            },
        ]
    )
    expected = pd.DataFrame(
        [
            {
                "Flowable": "h",
                "Context": "b/c",
                "Flow UUID": "i",
            }
        ]
    )
    result = filter_by_dataframe_attribute(
        given, filter_df, ["Flow UUID"], ["Flow UUID"]
    )
    assert_frame_equal(result, expected)


def test_get_different_flows():
    pass

import pytest
from eventflow.utils import search, sort


def test_linear_search_found():
    items = [1, 3, 5, 7]
    idx = search.linear_search(items, lambda x: x == 5)
    assert idx == 2


def test_linear_search_not_found():
    items = [1, 3, 5, 7]
    idx = search.linear_search(items, lambda x: x == 10)
    assert idx is None


def test_binary_search_found():
    items = [{"id": 1}, {"id": 3}, {"id": 5}, {"id": 7}]
    idx = search.binary_search(items, lambda x: x["id"], 5)
    assert idx == 2


def test_binary_search_not_found():
    items = [{"id": 1}, {"id": 3}, {"id": 5}, {"id": 7}]
    idx = search.binary_search(items, lambda x: x["id"], 10)
    assert idx is None


def test_merge_sort_basic():
    items = [5, 2, 9, 1]
    sorted_items = sort.merge_sort(items)
    assert sorted_items == [1, 2, 5, 9]


def test_merge_sort_with_key():
    items = [{"id": 3}, {"id": 1}, {"id": 2}]
    sorted_items = sort.merge_sort(items, key=lambda x: x["id"])
    assert [x["id"] for x in sorted_items] == [1, 2, 3]

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from imwievaluation.utils import clean_string, escape_latex_special_characters
from imwievaluation.utils import filter_dict
from imwievaluation.utils import filter_and_sort_dicts
from imwievaluation.utils import sort_dicts


@pytest.mark.parametrize('test_string, expected', [
    ('ä12/...', 'a12'),
    ('äÄöÖüÜß', 'aAoOuUss'),
    ('{f, 2 asw', 'f 2 asw')
])
def test_clean_string(test_string, expected):
    assert clean_string(test_string) == expected


def test_escape_latex_special_characters():
    assert escape_latex_special_characters('as #t {') == 'as \#t \{'


def test_filter_dict():
    d = {'a': 1, 'b': 2, 'c': 3}
    assert filter_dict(d, ['a']) == {'a': 1}
    assert filter_dict(d, []) == {}


def test_sort_dicts():
    l = [{'a': 1, 'b': 2, 'c': 3}, {'a': 2, 'b': 0, 'c': 3}]
    assert sort_dicts(l, 'a') == [{'a': 1, 'b': 2, 'c': 3},
                                  {'a': 2, 'b': 0, 'c': 3}]
    assert sort_dicts(l, 'b') == [{'a': 2, 'b': 0, 'c': 3},
                                  {'a': 1, 'b': 2, 'c': 3}]


def test_filter_and_sort_dicts():
    dicts = [{'a': 1, 'b': 2, 'c': 3}, {'a': 2, 'b': 0, 'c': 3}]
    result = filter_and_sort_dicts(dicts, 'b', ['b'])
    assert result == [{'b': 0}, {'b': 2}]
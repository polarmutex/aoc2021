import pytest

from py_aoc.year_2021.day22 import INPUT_S, INPUT_S2, parse, INPUT_GITHUB, INPUT_GOOGLE, INPUT_TWITTER, INPUT_REDDIT, part1, part2
from typing import List, Any


@pytest.fixture
def example() -> str:
    return INPUT_S


@pytest.fixture
def example2() -> str:
    return INPUT_S2


@pytest.fixture
def github() -> str:
    with open(INPUT_GITHUB) as f:
        return f.read()


@pytest.fixture
def google() -> str:
    with open(INPUT_GOOGLE) as f:
        return f.read()


@pytest.fixture
def twitter() -> str:
    with open(INPUT_TWITTER) as f:
        return f.read()


@pytest.fixture
def reddit() -> str:
    with open(INPUT_REDDIT) as f:
        return f.read()


@pytest.mark.skip(reason="Not implemented")
def test_parse(example: str) -> None:
    actual: List[Any] = []  # parse(example)
    expected: List[Any] = [
    ]
    print(actual)
    assert actual == expected


def test_part1_example(example: str) -> None:
    assert(part1(example) == 590784)


def test_part2_example(example2: str) -> None:
    assert(part2(example2) == 2758514936282235)


def test_part1_github(github: str) -> None:
    assert part1(github) == 615869


def test_part2_github(github: str) -> None:
    assert part2(github) == 1323862415207825


@pytest.mark.skip(reason="Not implemented")
def test_part1_google(google: str) -> None:
    assert part1(google) == 556206


@pytest.mark.skip(reason="Not implemented")
def test_part2_google(google: str) -> None:
    assert part2(google) == 630797200227453


@pytest.mark.skip(reason="Not implemented")
def test_part1_twitter(twitter: str) -> None:
    assert part1(twitter) == 921585


@pytest.mark.skip(reason="Not implemented")
def test_part2_twitter(twitter: str) -> None:
    assert part2(twitter) == 911090395997650


@pytest.mark.skip(reason="Not implemented")
def test_part1_reddit(reddit: str) -> None:
    assert part1(reddit) == 742257


@pytest.mark.skip(reason="Not implemented")
def test_part2_reddit(reddit: str) -> None:
    assert part2(reddit) == 93726416205179

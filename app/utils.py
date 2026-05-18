from collections import defaultdict
from typing import Callable, TypeVar, Iterable, Dict, List

K = TypeVar("K")
V = TypeVar("V")
R = TypeVar("R")


def group_by(
	items: Iterable[R],
	key_fn: Callable[[R], K],
	value_fn: Callable[[R], V]
) -> Dict[K, List[V]]:
	result: dict[K, list[V]] = defaultdict(list)

	for item in items:
		key = key_fn(item)
		value = value_fn(item)
		result[key].append(value)

	return dict(result)
import ast
from functools import partial
from typing import (  # noqa: WPS235
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

_NodeType = TypeVar('_NodeType')
_DefaultType = TypeVar('_DefaultType')


def sequence_of_node(
    node_types: Tuple[Type[_NodeType], ...],
    sequence: Sequence[ast.stmt],
) -> Iterable[Sequence[_NodeType]]:
    """Find sequence of node by type."""
    is_desired_type = partial(
        lambda types, node: isinstance(node, types), node_types,
    )

    sequence_iterator = iter(sequence)
    previous_node = next(sequence_iterator, None)
    node_sequence: List[_NodeType] = []

    while previous_node is not None:
        current_node = next(sequence_iterator, None)

        if all(map(is_desired_type, (previous_node, current_node))):
            node_sequence.append(cast(_NodeType, previous_node))
        elif node_sequence:
            yield [*node_sequence, cast(_NodeType, previous_node)]
            node_sequence = []

        previous_node = current_node


def first(
    sequence: Iterable[_NodeType],
    default: Optional[_DefaultType] = None,
) -> Union[_NodeType, _DefaultType, None]:
    """Get first variable from sequence or default."""
    return next(iter(sequence), default)

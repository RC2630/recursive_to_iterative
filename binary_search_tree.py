from recursive_to_iterative import *

@dataclass
class Node:
    value: int
    left: Node | None = None
    right: Node | None = None

# -----------------------------------------------------------

def insert_recursive(node: Node, value: int) -> None:

    locals: dict[str, Any] = {}

    # instruction 1 (recursive call)
    if node.left is not None and value < node.value:
        insert_recursive(node.left, value)

    # instruction 2 (recursive call)
    if node.right is not None and value > node.value:
        insert_recursive(node.right, value)

    # instruction 3 (code block)
    if node.left is None and value < node.value:
        node.left = Node(value)
    elif node.right is None and value > node.value:
        node.right = Node(value)

# -----------------------------------------------------------

def insert_base_case(locals: LocalVariables, node: Node, value: int) -> None:
    if node.left is None and value < node.value:
        node.left = Node(value)
    elif node.right is None and value > node.value:
        node.right = Node(value)

insert_iterative = IterativeRecursion([
    RecursiveCall(
        recursion_condition = lambda args, kwargs, locals: \
            kwargs["node"].left is not None and kwargs["value"] < kwargs["node"].value,
        recursion_args = lambda args, kwargs, locals: \
            ((), {"node": kwargs["node"].left, "value": kwargs["value"]})
    ),
    RecursiveCall(
        recursion_condition = lambda args, kwargs, locals: \
            kwargs["node"].right is not None and kwargs["value"] > kwargs["node"].value,
        recursion_args = lambda args, kwargs, locals: \
            ((), {"node": kwargs["node"].right, "value": kwargs["value"]})
    ),
    insert_base_case
])

# -----------------------------------------------------------

def traverse_with_depth_recursive(node: Node, depth: int) -> dict[int, int]:

    locals: dict[str, Any] = {}
    
    # instruction 1 (code block)
    locals["result"] = {}

    # instruction 2 (recursive call)
    if node.left is not None:
        locals["left_result"] = traverse_with_depth_recursive(node.left, depth + 1)

    # instruction 3 (code block)
    locals["result"].update(locals.get("left_result", {}))
    locals["result"][node.value] = depth

    # instruction 4 (recursive call)
    if node.right is not None:
        locals["right_result"] = traverse_with_depth_recursive(node.right, depth + 1)

    # instruction 5 (code block)
    locals["result"].update(locals.get("right_result", {}))
    return locals["result"]

# -----------------------------------------------------------

def depth_init(locals: LocalVariables, node: Node, depth: int) -> None:
    locals["result"] = {}

def depth_update_left_and_curr(locals: LocalVariables, node: Node, depth: int) -> None:
    locals["result"].update(locals.get("left_result", {}))
    locals["result"][node.value] = depth

def depth_update_right_and_return(
    locals: LocalVariables, node: Node, depth: int
) -> dict[int, int]:
    locals["result"].update(locals.get("right_result", {}))
    return locals["result"]

traverse_with_depth_iterative = IterativeRecursion([
    depth_init,
    RecursiveCall(
        recursion_condition = lambda args, kwargs, locals: \
            kwargs["node"].left is not None,
        recursion_args = lambda args, kwargs, locals: \
            ((), {"node": kwargs["node"].left, "depth": kwargs["depth"] + 1}),
        result_local_var = "left_result"
    ),
    depth_update_left_and_curr,
    RecursiveCall(
        recursion_condition = lambda args, kwargs, locals: \
            kwargs["node"].right is not None,
        recursion_args = lambda args, kwargs, locals: \
            ((), {"node": kwargs["node"].right, "depth": kwargs["depth"] + 1}),
        result_local_var = "right_result"
    ),
    depth_update_right_and_return
])

# -----------------------------------------------------------

def traverse_with_height_recursive(node: Node | None) -> dict[int, int]:

    locals: dict[str, Any] = {}

    # instruction 1 (code block)
    if node is None:
        locals["result"] = {}

    # instruction 2 (recursive call)
    if node is not None:
        locals["left_result"] = traverse_with_height_recursive(node.left)

    # instruction 3 (recursive call)
    if node is not None:
        locals["right_result"] = traverse_with_height_recursive(node.right)

    # instruction 4 (code block)
    if node is not None:
        left_height: int = \
            locals["left_result"][node.left.value] if node.left is not None else -1
        right_height: int = \
            locals["right_result"][node.right.value] if node.right is not None else -1
        height: int = max(left_height, right_height) + 1
        locals["result"] = locals["left_result"] | {node.value: height} | locals["right_result"]
    return locals["result"]

# -----------------------------------------------------------

def height_init(locals: LocalVariables, node: Node | None) -> None:
    if node is None:
        locals["result"] = {}

def height_calculate_and_return(locals: LocalVariables, node: Node | None) -> dict[int, int]:
    if node is not None:
        left_height: int = \
            locals["left_result"][node.left.value] if node.left is not None else -1
        right_height: int = \
            locals["right_result"][node.right.value] if node.right is not None else -1
        height: int = max(left_height, right_height) + 1
        locals["result"] = locals["left_result"] | {node.value: height} | locals["right_result"]
    return locals["result"]

traverse_with_height_iterative = IterativeRecursion([
    height_init,
    RecursiveCall(
        recursion_condition = lambda args, kwargs, locals: \
            kwargs["node"] is not None,
        recursion_args = lambda args, kwargs, locals: \
            ((), {"node": kwargs["node"].left}),
        result_local_var = "left_result"
    ),
    RecursiveCall(
        recursion_condition = lambda args, kwargs, locals: \
            kwargs["node"] is not None,
        recursion_args = lambda args, kwargs, locals: \
            ((), {"node": kwargs["node"].right}),
        result_local_var = "right_result"
    ),
    height_calculate_and_return
])

# -----------------------------------------------------------

values_to_insert: list[int] = [
    53, 37, 71, 18, 44, 60, 85, 8, 26, 43, 47, 57, 63, 80,
    93, 5, 15, 24, 27, 49, 54, 65, 77, 81, 88, 96, 12, 23
]

root_recursive = Node(values_to_insert[0])
root_iterative = Node(values_to_insert[0])

for value in values_to_insert:
    insert_recursive(node = root_recursive, value = value)
    insert_iterative(node = root_iterative, value = value)

depths_recursive: dict[int, int] = traverse_with_depth_recursive(node = root_recursive, depth = 0)
depths_iterative: dict[int, int] = traverse_with_depth_iterative(node = root_iterative, depth = 0)
assert list(depths_recursive.items()) == list(depths_iterative.items())

heights_recursive: dict[int, int] = traverse_with_height_recursive(node = root_recursive)
heights_iterative: dict[int, int] = traverse_with_height_iterative(node = root_iterative)
assert list(heights_recursive.items()) == list(heights_iterative.items())

print(f"\ndepths (recursive):\n{depths_recursive}")
print(f"\ndepths (iterative):\n{depths_iterative}")
print(f"\nheights (recursive):\n{heights_recursive}")
print(f"\nheights (iterative):\n{heights_iterative}")
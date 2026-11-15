from recursive_to_iterative import *
from helpers.graph_util.graph import Node as GenericNode, Graph as GenericGraph
from helpers.graph_util.random_graph_generator import generate_graph
from random import seed, randint

seed(2630)

type Node = GenericNode[None, None]
type Graph = GenericGraph[None, None]

# -----------------------------------------------------

def dfs_conventional_iterative(node: Node) -> list[str]:
    visited: set[Node] = set()
    result: list[str] = []
    frontier: list[Node] = [node]
    while len(frontier) > 0:
        curr: Node = frontier.pop()
        if curr in visited:
            continue
        visited.add(curr)
        result.append(curr.name)
        for neighbour in reversed(curr.edges):
            if neighbour not in visited:
                frontier.append(neighbour)
    return result

# -----------------------------------------------------

def dfs_conventional_recursive(node: Node, visited: set[Node] | None = None) -> list[str]:
    result: list[str] = [node.name]
    if visited is None:
        visited = {node}
    for neighbour in node.edges:
        if neighbour not in visited:
            visited.add(neighbour)
            result.extend(dfs_conventional_recursive(neighbour, visited))
    return result

# -----------------------------------------------------

def dfs_recursive(node: Node, visited: set[Node] | None = None) -> list[str]:

    locals: dict[str, Any] = {}

    # instruction 1 (code block)
    locals["result"] = [node.name]
    if visited is None:
        locals["visited"] = {node}
    else:
        locals["visited"] = visited
    locals["neighbours_it"] = iter(node.edges)

    # handled by jumps, so has no direct equivalent
    while True:

        # instruction 2 (code block)
        locals["neighbour"] = next(locals["neighbours_it"], None)
        locals["should_recurse"] = \
            locals["neighbour"] is not None and locals["neighbour"] not in locals["visited"]
        if locals["should_recurse"]:
            locals["visited"].add(cast(Node, locals["neighbour"]))

        # instruction 3 (recursive call)
        if locals["should_recurse"]: # RecursiveCall.recursion_condition
            locals["neighbour_result"] = dfs_recursive( # RecursiveCall.result_local_var
                cast(Node, locals["neighbour"]), locals["visited"] # RecursiveCall.recursion_args
            )
            locals["result"].extend(locals["neighbour_result"]) # RecursiveCall.callback
        if locals["neighbour"] is None: # RecursiveCall.action_after
            break

    # instruction 4 (code block)
    return locals["result"]

# -----------------------------------------------------

def dfs_init(locals: LocalVariables, node: Node, visited: set[Node] | None = None) -> None:
    locals["result"] = [node.name]
    if visited is None:
        locals["visited"] = {node}
    else:
        locals["visited"] = visited
    locals["neighbours_it"] = iter(node.edges)

def dfs_prepare(locals: LocalVariables, node: Node, visited: set[Node] | None = None) -> None:
    locals["neighbour"] = next(locals["neighbours_it"], None)
    locals["should_recurse"] = \
        locals["neighbour"] is not None and locals["neighbour"] not in locals["visited"]
    if locals["should_recurse"]:
        locals["visited"].add(cast(Node, locals["neighbour"]))

def dfs_update(locals: LocalVariables, node: Node, visited: set[Node] | None = None) -> None:
    locals["result"].extend(locals["neighbour_result"])

def dfs_return(locals: LocalVariables, node: Node, visited: set[Node] | None = None) -> list[str]:
    return locals["result"]

def dfs_recursion_cond(args: StarArgs, kwargs: KeywordArgs, locals: LocalVariables) -> bool:
    return locals["should_recurse"]

def dfs_recursion_args(
    args: StarArgs, kwargs: KeywordArgs, locals: LocalVariables
) -> tuple[StarArgs, KeywordArgs]:
    return ((), {"node": locals["neighbour"], "visited": locals["visited"]})

def dfs_action_after(args: StarArgs, kwargs: KeywordArgs, locals: LocalVariables) -> ActionAfter:
    if locals["neighbour"] is None:
        return None
    else:
        return ("back", 1)

dfs_iterative = IterativeRecursion([
    dfs_init,
    dfs_prepare,
    RecursiveCall(
        recursion_condition = dfs_recursion_cond,
        recursion_args = dfs_recursion_args,
        result_local_var = "neighbour_result",
        callback = dfs_update,
        action_after = dfs_action_after
    ),
    dfs_return
])

# -----------------------------------------------------

graph: Graph = generate_graph(num_nodes = 15, num_edges_distribution = lambda: randint(1, 4))
start_node: Node = graph.nodes[0]

conv_recursive: list[str] = dfs_conventional_recursive(start_node)
conv_iterative: list[str] = dfs_conventional_iterative(start_node)
exp_recursive: list[str] = dfs_recursive(start_node)
exp_iterative: list[str] = dfs_iterative(start_node)

assert conv_recursive == conv_iterative == exp_recursive == exp_iterative

print(f"\ngraph:\n{graph}")
print(f"\nconventional recursive DFS:\n{conv_recursive}")
print(f"\nconventional iterative DFS:\n{conv_iterative}")
print(f"\nexperimental recursive DFS:\n{exp_recursive}")
print(f"\nexperimental iterative DFS:\n{exp_iterative}")
from recursive_to_iterative import *

def fibonacci_recursive(n: int) -> int:

    locals: dict[str, Any] = {}

    # instruction 1 (code block)
    if n <= 1:
        locals["result"] = n

    # instruction 2 (recursive call)
    if n >= 2:
        locals["one_smaller"] = fibonacci_recursive(n - 1)

    # instruction 3 (recursive call)
    if n >= 2:
        locals["two_smaller"] = fibonacci_recursive(n - 2)

    # instruction 4 (code block)
    if n >= 2:
        locals["result"] = locals["one_smaller"] + locals["two_smaller"]
    return locals["result"]

# -----------------------------------------------------------

def base_case(locals: LocalVariables, n: int) -> None:
    if n <= 1:
        locals["result"] = n

def final_result(locals: LocalVariables, n: int) -> int:
    if n >= 2:
        locals["result"] = locals["one_smaller"] + locals["two_smaller"]
    return locals["result"]

fibonacci_iterative = IterativeRecursion([
    base_case,
    RecursiveCall(
        recursion_condition = lambda args, kwargs, locals: args[0] >= 2,
        recursion_args = lambda args, kwargs, locals: ((args[0] - 1,), {}),
        result_local_var = "one_smaller"
    ),
    RecursiveCall(
        recursion_condition = lambda args, kwargs, locals: args[0] >= 2,
        recursion_args = lambda args, kwargs, locals: ((args[0] - 2,), {}),
        result_local_var = "two_smaller"
    ),
    final_result
])

for i in range(10):
    assert fibonacci_iterative(i) == fibonacci_recursive(i)
    print(f"fibonacci_iterative({i}) = {fibonacci_iterative(i)}")
from typing import Callable, Any, NamedTuple, Concatenate, cast, Literal
from collections.abc import Iterable
from dataclasses import dataclass

type StarArgs = tuple[Any, ...]
type KeywordArgs = dict[str, Any]
type LocalVariables = dict[str, Any]

type CodeBlock[**P, R] = Callable[Concatenate[LocalVariables, P], R | None]
type Instructions[**P, R] = list[CodeBlock[P, R] | RecursiveCall[P, R]]
type ActionAfter = None | Literal["repeat"] | tuple[Literal["back"], int]

type StateToValue[T] = Callable[[StarArgs, KeywordArgs, LocalVariables], T]
type RecursionArgs = StateToValue[tuple[StarArgs, KeywordArgs]]
type RecursionCondition = StateToValue[bool]
type ActionAfterFunc = StateToValue[ActionAfter]

class State(NamedTuple):
    args: StarArgs
    kwargs: KeywordArgs
    locals: LocalVariables

class RecursiveCall[**P, R](NamedTuple):
    recursion_condition: RecursionCondition
    recursion_args: RecursionArgs = lambda args, kwargs, locals: (args, kwargs)
    result_local_var: str | None = None
    callback: CodeBlock[P, R] | None = None
    action_after: ActionAfterFunc = lambda args, kwargs, locals: None

@dataclass
class CallStackEntry:
    state: State
    inst_index: int = 0
    prev_index: int = -1

def delta_index(action_after: ActionAfter) -> int:
    if action_after is None:
        return 1
    elif action_after == "repeat":
        return 0
    else:
        back: int = action_after[1]
        assert back >= 1
        return -back

# -----------------------------------------------------------

class IterativeRecursion[**P, R]:

    def __init__(self, instructions: Iterable[CodeBlock[P, R] | RecursiveCall[P, R]]) -> None:
        self.instructions: Instructions[P, R] = list(instructions)
        if len(self.instructions) > 0 and isinstance(self.instructions[-1], RecursiveCall):
            self.instructions.append(lambda locals, *args, **kwargs: None)

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        if len(self.instructions) == 0:
            return cast(R, None)
        call_stack: list[CallStackEntry] = [
            CallStackEntry(State(args, kwargs, {}))
        ]
        curr_return_value: R | None = None
        while True:
            curr_entry: CallStackEntry = call_stack[-1]
            state: State = curr_entry.state
            curr_i: int = curr_entry.inst_index
            if isinstance(inst := self.instructions[curr_i], RecursiveCall):
                inst = cast(RecursiveCall[P, R], inst)
                if inst.recursion_condition(state.args, state.kwargs, state.locals):
                    new_args, new_kwargs = \
                        inst.recursion_args(state.args, state.kwargs, state.locals)
                    call_stack.append(CallStackEntry(State(new_args, new_kwargs, {})))
                curr_entry.inst_index += \
                    delta_index(inst.action_after(state.args, state.kwargs, state.locals))
            else:
                curr_return_value = inst(state.locals, *state.args, **state.kwargs)
                curr_entry.inst_index += 1
            curr_entry.prev_index = curr_i
            if curr_entry.inst_index == len(self.instructions):
                call_stack.pop()
                if len(call_stack) == 0:
                    return cast(R, curr_return_value)
                else:
                    prev_entry: CallStackEntry = call_stack[-1]
                    prev_state: State = prev_entry.state
                    prev_i: int = prev_entry.prev_index
                    assert isinstance(rcall := self.instructions[prev_i], RecursiveCall)
                    rcall = cast(RecursiveCall[P, R], rcall)
                    if rcall.result_local_var is not None:
                        prev_state.locals[rcall.result_local_var] = curr_return_value
                    if rcall.callback is not None:
                        rcall.callback(prev_state.locals, *prev_state.args, **prev_state.kwargs)
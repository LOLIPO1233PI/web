from functools import singledispatchmethod
from typing import Any, Literal, Self


class Function:
    def __init__(self, name: str, *args_demanded, is_async: bool = False) -> None:
        self.name = name.strip()
        if name.find(" ") != -1:
            raise ValueError("Function name could not contain a space")
        self.args_demanded = args_demanded
        self.indent_lev = 0
        self.async_ = is_async
        self.contents = []

    def append(self, value: str) -> None:
        self.contents.append(value)

    def clear(self) -> None:
        self.contents.clear()

    def __len__(self) -> None:
        return len(self.contents)

    def __str__(self):
        return f"<Function object | {self.name}>"

    def __enter__(self) -> Self:
        return self

    def __exit__(self, type, value, traceback):
        (
            self.args_demanded,
            self.name,
            self.contents,
            self.indent_lev,
            self.indent_lev,
        ) = (
            None,
            None,
            None,
            None,
            None,
        )
        return not type or not issubclass(type, Exception)

    def call(self, *args: str) -> None:
        if len(self.args_demanded) == len(args):
            return f"{self.name}"
        raise TypeError(
            f"Function has give {len(args)} but it require only {len(self.args_demanded)}"
        )

    def as_script(self) -> str:
        p_contents = []
        for i in self.contents:
            if i is None:
                continue
            elif isinstance(i, Function):
                i.indent_lev = self.indent_lev + 1
                p_contents.append(i.as_script())
            else:
                p_contents.append(str(i))
        p_contents = f"\n{'\n'.join(p_contents)}\n" if p_contents else ""
        return f"{'async ' if self.async_ else ''}function {self.name}({', '.join(self.args_demanded)}) {'{'}{p_contents}\n{'}'}"


def call_function(name: str, text: str) -> str:
    return f"{name}({text})"


class Var:
    def __init__(
        self,
        var_name: str,
        type: Literal["instance", "int", "str", "hashmap", "array", "unknown"],
        value: str = "undefined",
        declaration: Literal["var", "let", "const", "global"] = "var",
    ):
        self.var_name = var_name
        self.declaration = declaration
        self.value = value
        self.type = type
        self.items = None
        if type in ["hash", "instance"]:
            self.items = {}
        elif type == "array":
            self.items = []

    def __str__(self):
        if self.declaration == "global":
            return f"global.{self.var_name} = {self.value};"
        return f"{self.declaration} {self.var_name} = {self.value};"

    def change_value(self, value: str, type: str = ...) -> str:
        if not isinstance(type, ellipsis):  # noqa: F821
            self.type = type
        if self.declaration == "global":
            return f"global.{self.var_name} = {value};"
        return f"{self.value} = {value};"

    @singledispatchmethod
    def __setitem__(self, _key: Any, _value: Any) -> None:
        return NotImplemented

    @__setitem__.register
    def _(self, key: str, value: str):
        if self.type in ["hash", "instance"]:
            self.items[key] = value
        return NotImplemented

    @__setitem__.register
    def _(self, key: int, value: str):
        if self.type == "array":
            self.items[key] = value
        return NotImplemented

    @singledispatchmethod
    def __getitem__(self, _key: Any) -> None:
        return NotImplemented

    @__getitem__.register
    def _(self, key: str) -> str:
        return self.items[key]

    def __getattr__(self, attribute: str) -> str:
        if self.type in ["hash", "instance"]:
            return self[attribute]
        return NotImplemented

    def __setattr__(self, attribute: str, value: str) -> str:
        if self.declaration == "global":
            return f"global.{self.var_name}.{attribute} = {value};"
        return f"{self.value}.{attribute} = {value}"


def Return(value: str) -> str:
    return f"return {value}"


def new_instance(value: Var, class_name: str) -> str:
    return value.change_value(f"new {class_name}")

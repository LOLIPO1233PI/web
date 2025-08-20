from typing import Literal, Self


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
        declaration: Literal["var", "let", "const", "global"] = "var",
    ):
        self.var_name = var_name
        self.declaration = declaration


if __name__ == "__main__":
    a = Function("abc", "name", "age")
    print(a.as_script())

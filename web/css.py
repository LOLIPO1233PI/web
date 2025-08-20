from typing import Any, Iterator, Self


# Added basic css object functionality : 18/08/2025


class CSSobj:
    "this class handles the behavior of a css elements"

    __slots__ = ("styles", "selector")

    def __init__(self, selector: str = None, **styles: str) -> None:
        # styles support any class that has a __str__ dunder function and same for selector
        self.selector = selector
        self.styles = styles

    def __eq__(self, value):
        return self.styles == value

    def __str__(self) -> str:
        return f"<{self.styles or 'Empty'}>"

    def __dict__(self) -> dict:
        return {"styles": self.styles, "selector": self.selector}

    def __iter__(self) -> Iterator:
        return iter(self.selector)

    def __getitem__(self, key: str) -> str | Any:
        return self.styles[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.styles[key] = value

    def __contains__(self, value: str) -> bool:
        return value in self.styles

    def __getattr__(self, style: str) -> Any:
        return self[style]

    def __enter__(self) -> Self:
        return self

    def __exit__(self, type, value, traceback):
        self.styles, self.selector = None, None  # wiping the class to save up memory
        return not type or not issubclass(type, Exception)

    def css(self) -> str:
        "returns a css object in the format css file format"
        if not self.selector:
            raise ValueError("You must have a selector defined to use this method")
        styles = [f"    {style}: {self.styles[style]};" for style in self.styles]
        styles = "\n".join(styles)
        return f"{self.selector} {'{'}\n{styles}\n{'}'}"

    def inline_css(self) -> str:
        "returns a valid inline css for a html block"
        styles = [f"{style}: {self.styles[style]};" for style in self.styles]
        return " ".join(styles)

    def export(self, css_filepath: str, append: bool = False) -> None:
        "export the css data to a .css file, via appending or rewriting a file completly"
        mode = "w" if not append else "a"
        try:
            with open(css_filepath, mode, encoding="utf-8") as f:
                f.write(self.css())
        except PermissionError:
            print("couldn't continue the process due to lack of permission")
        except IOError as e:
            print("couldn't continue the process due to %s", e)

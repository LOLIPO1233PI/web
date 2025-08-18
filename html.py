from typing import Any, Iterator, Self, Union  # noqa: F401
from functools import singledispatchmethod
from css import CSSobj

# HTML engine v1.0


def self_closing(tag: str) -> bool:
    return tag in [
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    ]


class HTMLobj:
    __slots__ = (
        "tag",
        "css",
        "class_",
        "contents",
        "attributes",
        "self_closing",
        "__indent",
    )

    def __init__(
        self,
        tag: str,
        css: "CSSobj" = None,
        class_: str = None,
        *contents: Union[str, "HTMLobj", Any],
        **attributes: str,
    ) -> None:
        self.tag = tag
        self.css = css
        self.class_ = class_
        self.contents = [*contents]
        self.attributes = attributes
        self.self_closing = self_closing(self.tag)
        if self.self_closing and self.contents:
            raise ValueError("A self closing Html object cant contain sub elements")
        if not hasattr(self, "__indent"):
            self.__indent = 0

    def __iter__(self) -> Iterator:
        return iter(self.contents)

    def __dict__(self) -> dict:
        return {
            "tag": self.tag,
            "class": self.class_,
            "contents": self.contents,
            "attributes": self.attributes,
            "self_closing": self.self_closing,
        }

    def __tag__(self) -> tuple[str, str]:
        attributes = []
        if isinstance(self.css, CSSobj):
            attributes.append(f'styles="{self.css.inline_css()}"')
        if self.class_:
            attributes.append(f"class={self.class_}")
        for i in self.attributes:
            attributes.append(f'{i}="{self.attributes[i]}"')
        attributes = f" {' '.join(attributes)}" if attributes else ""
        if self.self_closing:
            return f"<{self.tag}{attributes}", "/>"
        return f"<{self.tag}{attributes}>", f"</{self.tag}>"

    def __str__(self) -> str:
        contents = [str(i) for i in self.contents if i is not None]
        contents = "".join(contents)
        startTAG, endTAG = self.__tag__()
        return f"{startTAG}{contents if contents else ''}{endTAG}"

    def __enter__(self) -> Self:
        return self

    def __exit__(self, type, value, traceback):
        self.css, self.tag, self.attributes, self.class_, self.contents = (
            None,
            None,
            None,
            None,
            None,
        )  # wiping the class to save up memory
        return not type or not issubclass(type, Exception)

    @singledispatchmethod
    def __getitem__(self, _key: Any):
        return NotImplemented

    @__getitem__.register
    def _(self, key: str):
        return self.attributes[key]

    @__getitem__.register
    def _(self, index: int):
        return self.contents[index]

    @singledispatchmethod
    def __setitem__(self, _key: Any, _value: Any) -> None:
        return NotImplemented

    @__setitem__.register
    def _(self, key: str, value: Any):
        self.attributes[key] = value

    @__setitem__.register
    def _(self, index: int, value: Any):
        self.contents[index] = value

    def __contains__(self, content) -> bool:
        return content in self.contents

    def prettify(self, space: str = "  ") -> str:
        contents = []
        for i in self.contents:
            if i is None:
                continue
            elif isinstance(i, HTMLobj):
                i.__indent = self.__indent + 1
                contents.append(i.prettify())
            else:
                contents.append(f"{space * (self.__indent + 1)}{i}")
        contents = f"\n{'\n'.join(contents)}\n" if contents else ""
        startTAG, endTAG = self.__tag__()
        return f"{space * self.__indent}{startTAG}{contents}{space * self.__indent if contents else ''}{endTAG}"

    def export(self, html_filepath: str, append: bool = False) -> None:
        "export the css data to a .css file, via appending or rewriting a file completly"
        mode = "w" if not append else "a"
        try:
            with open(html_filepath, mode, encoding="utf-8") as f:
                f.write(self.prettify("    "))
        except PermissionError:
            print("couldn't continue the process due to lack of permission")
        except IOError as e:
            print("couldn't continue the process due to %s", e)

    def txt(self) -> Iterator:
        return map(lambda x: isinstance(x, str))

    def children(self) -> Iterator:
        return iter(self.contents)


def Basic_HTMLobj(tag: str, *contents) -> "HTMLobj":
    return HTMLobj(tag=tag, css=None, class_=None, *contents)

import web.html_


def GetPage(*contents) -> web.html_.HTMLobj:
    "Returns a empty document template"
    html = web.html_.HTMLobj("html", lang="en")
    meta1, meta2 = (
        web.html_.HTMLobj("meta", charset="UTF-8"),
        web.html_.HTMLobj(
            "meta", name="viewport", content="width=device-width, initial-scale=1.0"
        ),
    )
    head = web.html_.Basic_HTMLobj("head")
    head.append(meta1)
    head.append(meta2)
    html.append(head)
    body = web.html_.Basic_HTMLobj("body")
    html.append(body)
    body.contents = [*contents]

    return html


# feel free to make your own templates

from fasthtml.common import *

app, rt = fast_app(live=True)


def form_input_item(label, name, placeholder):
    return (Label(label, Input(name=name, placeholder=placeholder)),)


@rt("/")
def get():
    return Title("Blog"), Main(
        H1("Write Your Blog"),
        H2(
            "Blog Title here...",
            hx_trigger="click",
            hx_get="/input_title?title=Blog Title here...",
            hx_swap="outerHTML",
        ),
        cls="container",
    )


@rt("/input_title")
def get(title: str):
    return Input(
        name="title",
        placeholder="Enter Title",
        value=title,
        hx_post="/make_title",
        hx_swap="outerHTML",
        hx_trigger="blur",
    )


@rt("/make_title")
def post(title: str):
    return H2(
        title,
        hx_trigger="click",
        hx_get=f"/input_title?title={title}",
        hx_swap="outerHTML",
    )


serve()

from fasthtml.common import *
import html

app = FastHTML()
rt = app.route


class js_obj:
    def __init__(self, code, name="") -> None:
        self.name = name
        self.code = code

    def set_value(self, value):
        code_str = f"{self.name} = `{value}`;"
        self.code.append(code_str)

    def __add__(self, other):
        code_str = f"{self.name} + {other}"
        return code_str

    def __iadd__(self, other):
        code_str = f"{self.name} += `{other}`;"
        self.code.append(code_str)
        return self

    def __str__(self):
        return f"${{{self.name.replace('?', '')}}}"


class Surreal_style_obj(js_obj):
    def __init__(self, code, name=""):
        super().__init__(code, name)
        self.display = js_obj(code, f"{name}.display")


class Surreal_obj(js_obj):
    def __init__(self, code, name="e") -> None:
        super().__init__(code, name)
        self.innerHTML = js_obj(code, f"{name}.innerHTML")
        self.outerHTML = js_obj(code, f"{name}.outerHTML")
        self.innerText = js_obj(code, f"{name}.innerText")
        self.style = Surreal_style_obj(code, f"{name}.style")
        self.value = js_obj(code, f"{name}.value")


def if_js(obj, code):
    return f"if ({obj.name}) {{\n{code}\n}}"
    # TODO: Fix the way ifs are done
    # if_code = []
    # if_h2 = Surreal_obj(if_code, name="me(`h2`)")
    # if_h2.outerHTML.set_value(to_xml(html_to_replace))
    # code.append(
    #     if_js(
    #         if_h2,
    #         "\n".join(if_code),
    #     )
    # )


def change_back():
    code = []
    input_target = Surreal_obj(code)
    input_target.style.display.set_value("none")
    h2 = Surreal_obj(code, name="me(`h2`)")
    h2.style.display.set_value("block")
    h2.innerText.set_value(input_target.value)
    return "\n".join(code)


def change_name():
    code = []
    code.append("console.log('click')")
    target = Surreal_obj(code)
    target.style.display.set_value("none")
    input = Surreal_obj(code, name="me(`input`)")
    input.style.display.set_value("block")
    input.value.set_value(target.innerText)
    return "\n".join(code)


@rt("/")
def get():
    return Div(
        # H2("Hello, world!"),
        Input(value="Hello, world!", hidden=True),
        H2("Hello, world!"),
        On(change_back(), event="blur", sel="input"),
        On(change_name(), sel="h2"),
        On("console.log(e.innerHTML)"),
    )


serve(reload=True)

from jinja2 import FileSystemLoader, Environment


def get_text_funding(fundings):
    file_loader = FileSystemLoader("app/templates")
    env = Environment(loader=file_loader)
    tm = env.get_template("funding.htm")
    msg = tm.render(fundings=fundings)
    return msg

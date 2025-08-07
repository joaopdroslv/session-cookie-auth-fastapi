from config import templates
from starlette.templating import _TemplateResponse


def render_template(
    request, template: str, status_code: int, msg: str = None
) -> _TemplateResponse:
    """
    Renders an HTML template with an optional message.

    Args:
        request: The HTTP request object.
        template (str): The name of the template to render.
        status_code (int): The HTTP status code to return.
        msg (str, optional): A message to include in the template context.

    Returns:
        TemplateResponse: The rendered HTML response.
    """

    context = {"request": request}
    if msg:
        context["msg"] = msg

    return templates.TemplateResponse(
        name=template,
        context=context,
        status_code=status_code,
    )

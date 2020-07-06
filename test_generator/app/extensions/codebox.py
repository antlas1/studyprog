# stolen from: https://github.com/FND/markdown-checklist/blob/master/markdown_checklist/extension.py
import re

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor


def makeExtension(configs=None):
    if configs is None:
        return CodeboxExtension()
    else:
        return CodeboxExtension(configs=configs)

class CodeboxExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {
            "list_class": ["codebox", "class name to add to the list element"],
            "render_item": [render_item, "custom function to render items"]
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        list_class = self.getConfig("list_class")
        renderer = self.getConfig("render_item")
        postprocessor = CodeboxPostprocessor(list_class, renderer, md)
        md.postprocessors.add("codebox", postprocessor, ">raw_html")


class CodeboxPostprocessor(Postprocessor):
    """
    adds textbox class to list element
    """

    list_pattern = re.compile(r"(<ul>\n<li>[Cc]:=)")
    item_pattern = re.compile(r"^<li>([Cc]:=)(.*)</li>$", re.MULTILINE)

    def __init__(self, list_class, render_item, *args, **kwargs):
        self.list_class = list_class
        self.render_item = render_item
        super().__init__(*args, **kwargs)

    def run(self, html):
        html = re.sub(self.list_pattern, self._convert_list, html)
        return re.sub(self.item_pattern, self._convert_item, html)

    def _convert_list(self, match):
        return match.group(1).replace("<ul>", f"<ul class=\"{self.list_class}\">")

    def _convert_item(self, match):
        state, caption = match.groups()
        return self.render_item(caption, state != " ")


def render_item(caption: str, value):    
    captionAndLink = caption.split('#')
    link = ""
    if len(captionAndLink) == 2:
       caption = captionAndLink[0]
       link = captionAndLink[1]
    #правильный ответ рядом сложным сохраняются в перевернутом виде
    correct = caption.strip()
    return f"<li>" \
           f"<textarea type=\"text\" data-content=\"{correct}\" data-link=\"{link}\" " \
           f"placeholder=\"Введите корректный ответ\" class=\"form-control\">" \
           f"</textarea>" \
           f"</li>"

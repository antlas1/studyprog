# stolen from: https://github.com/FND/markdown-checklist/blob/master/markdown_checklist/extension.py
import re

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor


def makeExtension(configs=None):
    if configs is None:
        return RadioExtension()
    else:
        return RadioExtension(configs=configs)

#class RadioPreprocessor(Preprocessor):
#    """ Save line with links and clear from text """
#    def __init__(self, md):
#        super().__init__(md)
#        self._facts = ''
#        
#    def run(self, lines):
#        new_lines = []
#        for line in lines:
#            m = re.search("FACT", line)
#            if not m:    
#                # any line without NO RENDER is passed through
#                new_lines.append(line) 
#            else:
#                self._facts = re.sub("FACT", "", line)
#                print('radio preproc')
#        return new_lines
#        
#    def facts(self):
#        return self._facts

class RadioExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {
            "list_class": ["radio-list", "class name to add to the list element"],
            "render_item": [render_item, "custom function to render items"]
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        list_class = self.getConfig("list_class")
        renderer = self.getConfig("render_item")
        postprocessor = RadioPostprocessor(list_class, renderer, md)
        md.postprocessors.add("radio", postprocessor, ">raw_html")


class RadioPostprocessor(Postprocessor):
    """
    adds checklist class to list element
    """

    list_pattern = re.compile(r"(<ul>\n<li>\([ Xx]\))")
    item_pattern = re.compile(r"^<li>\(([ Xx])\)(.*)</li>$", re.MULTILINE)

    def __init__(self, list_class, render_item, *args, **kwargs):
        self.list_class = list_class
        self.render_item = render_item
        self._links = None
        super().__init__(*args, **kwargs)

    def run(self, html):
        html = re.sub(self.list_pattern, self._convert_list, html)
        return re.sub(self.item_pattern, self._convert_item, html)

    def _convert_list(self, match):
        return match.group(1).replace("<ul>", f"<ul class=\"{self.list_class}\">")

    def _convert_item(self, match):
        state, caption = match.groups()
        return self.render_item(caption, state != " ", self)


def render_item(caption, checked, proc):
    correct = "1" if checked else "0"
    fake = "0" if checked else "1"
    
    link = ""
    if caption.lstrip().startswith("#"):
        proc._links = re.sub("#","",caption)
        return ""
    elif proc._links is not None:
        link = proc._links
        proc._links = None
    
    return f"<li>" \
           f"<label><input type=\"radio\" data-question=\"{fake}\" data-content=\"{correct}\" data-link=\"{link}\" />{caption}</label>" \
           f"</li>"

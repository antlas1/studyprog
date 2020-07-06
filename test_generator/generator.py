"""
    Desarrollado con mucho <3 por Wlises Rivas,
    <wlisesrivas@gmail.com>
"""
import sys
import os
import io
import codecs
import argparse

import markdown
from jinja2 import Environment, PackageLoader, select_autoescape

# Renderizar el resultando incluyendo jQuery, Bootstrap.


def render_test(file_name: str, markdown_content: str, out_dir: str, ext: str, wrapper: str) -> None:
    """Renderizar examen en formato Markdown a un HTML."""

    extensions = ["tables", "app.extensions.checkbox", "app.extensions.radio", "app.extensions.textbox"]

    html = markdown.markdown(markdown_content, extensions=extensions, output_format="html5")
    env = Environment(loader=PackageLoader('app', 'static'), autoescape=select_autoescape(['html', 'xml']))

    javascript = env.get_template('app.js').render()

    test_html = env.get_template('base.html').render(content=html, javascript=javascript)
    test_html = env.get_template(wrapper).render(content=test_html)

    with io.open(f"{out_dir}/{file_name[:-2]}{ext}", "w+", encoding='UTF-8') as f:  # create final file
        f.write(test_html)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Test Generator v0.3')
    parser.add_argument("-i","--inp", help="Input md task directory", default="exams")
    parser.add_argument("-o","--out", help="Output directory", default=".")
    parser.add_argument("-e","--ext", help="Extension for output file", default="html")
    parser.add_argument("-w","--wrapper", help="Wrapper for tasks", default="wrapper.html")
    
    args = parser.parse_args()
    
    

    WRAPPER_RENDER = 'embed' not in sys.argv

    for file_name in os.listdir(args.inp):
        if file_name.endswith('.md'):
            with  io.open(os.path.join(args.inp, file_name), "r", encoding='UTF-8') as f:
                print(f"Process Markdown ({file_name}) ...")
                render_test(file_name, f.read(), args.out, args.ext, args.wrapper)

    sys.exit(0)

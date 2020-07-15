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
import json
from jinja2 import Environment, PackageLoader, select_autoescape

# Renderizar el resultando incluyendo jQuery, Bootstrap.


def render_test(file_name: str, markdown_content: str, out_dir: str, ext: str, wrapper: str) -> None:
    """Renderizar examen en formato Markdown a un HTML."""

    extensions = ["tables", "app.extensions.checkbox", "app.extensions.radio", "app.extensions.textbox", "app.extensions.codebox"]

    html = markdown.markdown(markdown_content, extensions=extensions, output_format="html5")
    env = Environment(loader=PackageLoader('app', 'static'), autoescape=select_autoescape(['html', 'xml']))

    javascript = env.get_template('app.js').render()

    test_html = env.get_template('base.html').render(content=html, javascript=javascript)
    test_html = env.get_template(wrapper).render(content=test_html)

    with io.open(f"{out_dir}/{file_name[:-2]}{ext}", "w+", encoding='UTF-8') as f:  # create final file
        f.write(test_html)

def create_coverage(content_lines):
    coverage = {'time': 0, 'page': "um_coverage", 'correct': {'facts': [], 'skills': []}, 'fail': {'facts': [], 'skills': []}}
    wait_tags = False
    for line in content_lines:
        line = line.strip()
        if len(line) > 2:
           if line.startswith("*"):
               wait_tags = True
           elif wait_tags == True:
               wait_tags = False
               #разделяем список тегов и служебную инфу
               pos_tags = line.find('#')
               if pos_tags != -1:
                   tags_list = line[pos_tags+1:].strip().split(',')
                   if len(tags_list) > 0:
                       #print(tags_list)
                       if tags_list[0] == 'UM':
                          coverage['correct']['skills'] += tags_list[1:]
                       else:
                          coverage['correct']['facts'] += tags_list
    return [coverage]
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Test Generator v0.3')
    parser.add_argument("-i","--inp", help="Input md file", default="exams/exam.md")
    parser.add_argument("-o","--out", help="Output directory", default=".")
    parser.add_argument("-e","--ext", help="Extension for output file", default="html")
    parser.add_argument("-w","--wrapper", help="Wrapper for tasks", default="wrapper.html")
    parser.add_argument("-c","--coverage", help="Coverage file for task", default="../site/cover.json")
    
    args = parser.parse_args()
    
    

    WRAPPER_RENDER = 'embed' not in sys.argv
    
    with io.open(args.inp, "r", encoding='UTF-8') as f:
        print(f"Process Markdown ({args.inp}) ...")
        content = f.read()
        render_test(os.path.basename(args.inp), content, args.out, args.ext, args.wrapper)
        coverage_json = create_coverage(content.split("\n"))
        #print(coverage_json)
        with io.open(f"{args.coverage}", "w+", encoding='UTF-8') as f:
            json.dump(coverage_json, f, ensure_ascii=False)

    sys.exit(0)

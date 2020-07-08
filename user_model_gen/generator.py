"""
    Преобразует списки фактов/знаний в страницу диагностики
"""
import sys
import os
import io
import re
import codecs
import argparse
import json

from jinja2 import Environment, PackageLoader, select_autoescape

#def render_test(file_name: str, markdown_content: str, out_dir: str, ext: str, wrapper: str) -> None:
#    """Renderizar examen en formato Markdown a un HTML."""
#
#    extensions = ["tables", "app.extensions.checkbox", "app.extensions.radio", "app.extensions.textbox", "app.extensions.codebox"]
#
#    html = markdown.markdown(markdown_content, extensions=extensions, output_format="html5")
#    env = Environment(loader=PackageLoader('app', 'static'), autoescape=select_autoescape(['html', 'xml']))
#
#    javascript = env.get_template('app.js').render()
#
#    test_html = env.get_template('base.html').render(content=html, javascript=javascript)
#    test_html = env.get_template(wrapper).render(content=test_html)
#
#    with io.open(f"{out_dir}/{file_name[:-2]}{ext}", "w+", encoding='UTF-8') as f:  # create final file
#        f.write(test_html)

def parse_md_list(content_lines):
   res_map={}
   start_list = False
   #идем до первых решеток
   for line in content_lines:
      line = line.strip()
      if len(line) > 2:
          is_header = line.startswith("##")
          if start_list == False and is_header:
             start_list = True
          elif start_list == True and is_header == False:
             #разделяем на идентификатор и тело с указанием на детей
             pos_space = line.find(' ')
             if pos_space != -1:
                 rule_id = line[:pos_space]
                 if (not re.search(r'\d\.\d',rule_id)) and (rule_id != 'root'):
                    continue
                 rule_body = line[pos_space+1:]
                 childs = []
                 #определяем есть ли дети
                 pos_st_childs = rule_body.rfind('(')
                 pos_ed_childs = rule_body.rfind(')')
                 if pos_st_childs != -1 and pos_ed_childs != -1 and re.search(r'\d\.\d',rule_body[pos_st_childs+1:pos_ed_childs]):
                    childs = rule_body[pos_st_childs+1:pos_ed_childs].split(',')
                    for i in range(len(childs)):
                       childs[i] = childs[i].strip()
                    rule_body = rule_body[:pos_st_childs]
                 #print(rule_id+':'+rule_body+' childs:'+str(childs))
                 res_map[rule_id] = {'body':rule_body, 'childs':childs}
         
   return res_map
   
def get_connected(graph, start, connected, treant_obj):
    #add genereta treant json:
    #nodeStructure: {
    #    text: {
    #        name: "Djokovic, Novak",
    #        desc: "4-6, 6-2, 6-2"
    #    },
    #    children: [
    #        {
    #            text: {
    #                name: "Djokovic, Novak",
    #                desc: "4-6, 6-2, 6-2"
    #            },
    #            children: [
    #                {
    #                    text: {
    #                        name: "Djokovic, Novak",
    #                        desc: "4-6, 6-1, 6-4"
    #                    },
    #                    children: [
    #                        {
    if not start in graph:
       print('Warning: wrong child id='+start)
       return None
    if not start in connected:
       connected.append(start)
       #print('Connect '+start)
    if len(graph[start]['childs']) == 0:
        return None
    for node in graph[start]['childs']:
        get_connected(graph, node, connected, treant_obj)
    return None

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='User model generator v0.1')
    parser.add_argument("-f","--facts", help="Semantic facts file", default="../docs/tech/semantic.md")
    parser.add_argument("-p","--procedures", help="Procedure model file", default="../docs/tech/procedural.md")
    parser.add_argument("-s","--skills", help="Skill model file", default="../docs/tech/skills.md")
    parser.add_argument("-o","--out", help="Output directory", default=".")
    parser.add_argument("-e","--ext", help="Extension for output file", default="html")
    parser.add_argument("-w","--wrapper", help="Wrapper for tasks", default="wrapper.html")
    parser.add_argument("-j","--json", help="Dump model to json", default="../site/model.json")
    
    args = parser.parse_args()
    
    facts_map = {}
    procedure_map = {}
    skills_map = {}
    with io.open(f"{args.facts}", "r", encoding='UTF-8') as f:
       facts_map = parse_md_list(f.readlines())
    with io.open(f"{args.procedures}", "r", encoding='UTF-8') as f:
       procedure_map = parse_md_list(f.readlines())
    with io.open(f"{args.skills}", "r", encoding='UTF-8') as f:
       skills_map = parse_md_list(f.readlines())
       
    model = {
    'facts': facts_map,
    'procedures': procedure_map,
    'skills': skills_map
    }
    
    #поиск подключенных узлов
    conn_facts = []
    treant_obj = {}
    get_connected(facts_map,'root',conn_facts,treant_obj)
    disconn_facts = []
    for key in facts_map:
       if not key in conn_facts:
          disconn_facts.append(key)
    
    print('Disconnected facts: '+','.join(disconn_facts))
    
    #дамп для исследования
    with io.open(f"{args.json}", "w+", encoding='UTF-8') as f:
        json.dump(model, f, ensure_ascii=False)

    print("ok")
    sys.exit(0)

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
from abc import ABC, abstractmethod

def render_model(model_json_content: str, tree_json_content: str, out_fname: str, wrapper: str) -> None:
    env = Environment(loader=PackageLoader('app', 'static'), autoescape=select_autoescape(['html', 'xml']))

    out_html = env.get_template(wrapper).render(model=model_json_content, model_tree=tree_json_content)

    with io.open(f"{out_fname}", "w+", encoding='UTF-8') as f:
        f.write(out_html)

def parse_md_list(content_lines, res_map, root_name):
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
                 
                 #После root ничего не смотрим
                 if rule_id == 'root':
                     res_map[root_name] = {'body':rule_body.strip(), 'childs':childs} 
                     break
                 else:
                     res_map[rule_id] = {'body':rule_body.strip(), 'childs':childs}
   
   
class ModelIterator(ABC):
    """
    Интерфейс итератора позволяет обходить дерево модели, представленное в виде списка
    """

    @abstractmethod
    def iterate(self, graph, start) -> None:
        pass
        
        
class ConnectedFilterIterator(ModelIterator):
    def __init__(self):
        self._connected_id = []
        self._connected_model = {}
        
    def iterate(self, graph, start) -> None:  
        if not start in graph:
           print('Warning: wrong child id='+start)
        if not start in self._connected_id:
           self._connected_id.append(start)
           self._connected_model[start] = graph[start]
           if len(graph[start]['childs']) == 0:
               return
           for node in graph[start]['childs']:
                self.iterate(graph, node)
        return

    def clear(self):
        self._connected = []
        self._connected_model = {}
        
    def connected_id(self):
        return self._connected_id
        
    def connected_model(self):
        return self._connected_model
        
class TreantViewIterator(ModelIterator):
    def __init__(self):
        self._treant_obj = {}
        
    def iterate(self, graph, start) -> None:  
        self._treant_obj = self._iterate_with_return(graph, start)
        
    def json_repr(self):
        return json.dumps(self._treant_obj, ensure_ascii=False);
       
    def _iterate_with_return(self, graph, start) -> None: 
       if not start in graph:
           return None
       node_hier = { 'text': { 'name' : start, 'desc' : "" }, 'children' : [] }
       if len(graph[start]['childs']) == 0:
           return node_hier
       for node in graph[start]['childs']:
            node2 = self._iterate_with_return(graph, node)
            if node2 is not None:
               node_hier['children'].append(node2)
       return node_hier  

class TableViewIterator(ModelIterator):
    def __init__(self):
        self._table = []
        self._connected_id = []
        
    def iterate(self, graph, start) -> None:  
       if not start in graph:
           return
       if not start in self._connected_id:
           self._connected_id.append(start)
           self._table.append({'sid' : start, 'desc' : graph[start]['body'], 'childs' : ','.join(graph[start]['childs']) })
           if len(graph[start]['childs']) == 0:
               return
           for node in graph[start]['childs']:
                self.iterate(graph, node)
       return

    def clear(self):
        self._connected_id = []
        self._table = []
        
    def json_repr(self):
        return json.dumps(self._table, ensure_ascii=False);


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='User model generator v0.1')
    parser.add_argument("-f","--facts", help="Semantic facts file", default="../../docs/tech/semantic.md")
    parser.add_argument("-p","--procedures", help="Procedure model file", default="../../docs/tech/procedural.md")
    parser.add_argument("-o","--out", help="Output directory", default="../../site/know_model")
    parser.add_argument("-e","--ext", help="Extension for output file", default="html")
    parser.add_argument("-w","--wrapper", help="Wrapper for tasks", default="wrapper.html")
    parser.add_argument("-j","--json", help="Dump model to json", default="../../site/model.json")
    
    args = parser.parse_args()
    
    model_map = {}
    with io.open(f"{args.facts}", "r", encoding='UTF-8') as f:
       parse_md_list(f.readlines(),model_map,"root_facts")
    with io.open(f"{args.procedures}", "r", encoding='UTF-8') as f:
       parse_md_list(f.readlines(),model_map,"root_proc")
    model_map["root"] = {'body':'Все знания', 'childs':["root_facts","root_proc"]}
    
    
    #поиск подключенных узлов
    fact_it = ConnectedFilterIterator()
    fact_it.iterate(model_map,'root')
    conn_facts = fact_it.connected_id()
    
    disconn_facts = []
    for key in model_map:
       if not key in conn_facts:
          disconn_facts.append(key)
          
    conn_fact_model = fact_it.connected_model()
    #вид графа
    treant_it = TreantViewIterator()
    treant_it.iterate(conn_fact_model,"root")
    #вид таблицы
    table_it = TableViewIterator()
    table_it.iterate(conn_fact_model,"root")
    #print(table_it.json_repr())
    
    if not os.path.exists(args.out):
        print('Try to creaty output directory {}'.format(args.out))
        os.makedirs(args.out)
    dest_file = os.path.join(args.out,"know.html");
    render_model(table_it.json_repr(),treant_it.json_repr(),dest_file,'wrapper.html')
    
    #print(treant_it.json_repr())
    print('Disconnected facts: '+','.join(disconn_facts))
    
    #дамп для исследования
    with io.open(f"{args.json}", "w+", encoding='UTF-8') as f:
        json.dump(model_map, f, ensure_ascii=False)
        
    #with io.open("../site/trean.json", "w+", encoding='UTF-8') as f:
    #    f.write(treant_it.json_repr())

    print("ok")
    sys.exit(0)

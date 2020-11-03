from enum import Enum
import json
import os

__version__ = "0.0.2"

class TaskStep(Enum):
    NONE = 0
    TEXT = 1
    TABLE = 2
    INSIDE = 3

def parse_tasks_md(content):
    tasks = {}
    lines = content.splitlines()
    last_step = TaskStep.NONE
    step = TaskStep.NONE
    id = ''
    task_text = []
    vars = {}
    tests = []
    tags = []
    allowed_types = ['int', 'float', 'string']
    tbl_splitter = True
    content_ver = 'NONE'
    
    ver_str = lines[0]
    if ver_str.lower().startswith('version:'):
        content_ver = ver_str[8:].strip()
    
    for str in lines[1:]:
        str = str.strip()
        if step == TaskStep.NONE:
            #searching for id
            if str.startswith('#'):
                id = str[1:]
                assert id not in tasks.keys()
                tasks[id] = {'desc': '', 'tags': [], 'vars': {}, 'out_type': {}, 'test_col': [], 'tests': []}
                task_text = []
                vars = {}
                tags = []
                step = TaskStep.TEXT
        elif step == TaskStep.TEXT:
            #parsing multiline task description
            if len(str) == 0:
                tasks[id]['desc'] = '\\n'.join(task_text)
                step = TaskStep.INSIDE
            else:
                task_text.append(str)
        elif step == TaskStep.INSIDE:
            #parsing inside task one line things
            if str.startswith('|'):
                tasks[id]['vars'] = vars
                tbl_read_header = False
                step = TaskStep.TABLE
                #parsing table header
                header = str.split('|')[1:-1]
                #print(header)
                assert len(header)-1 == len(vars)
                #check final is out
                assert header[-1] == 'OUT'
                left_vars = list(vars.keys())
                #check other
                for itm in header[:-1]:
                    assert itm in left_vars
                    left_vars.remove(itm)
                assert len(left_vars) == 0
                tasks[id]['test_col'] = header[:-1]
                tbl_splitter = True
            else:
               if str.lower().startswith('input:'):
                   #parse variables
                   var_str = str[6:].strip()
                   var_pairs = var_str.split(',')
                   for varp in var_pairs:
                       type_name = varp.strip().split(' ')
                       assert len(type_name) == 2
                       var_type = type_name[0]
                       assert var_type in allowed_types
                       var_name = type_name[1]
                       vars[var_name] = var_type
               elif str.lower().startswith('output:'):
                    var_str = str[7:].strip()
                    tasks[id]['out_type'] = var_str.lower()
               #elif str.lower().startswith('args:'):
               #    #parse tags
        elif step == TaskStep.TABLE:
            #parsing multiline table
            if len(str) == 0:
                step = TaskStep.NONE
            else:
                if tbl_splitter is True:
                    tbl_splitter = False
                else:
                    vals = str.split('|')[1:-1]
                    assert len(vals)-1 == len(vars)
                    tasks[id]['tests'].append(vals)
                
        if step != last_step:
            print('{} -> {}: str {}'.format(last_step, step, str))
            last_step = step
        #end for
        
    #check that table is over
    assert step == TaskStep.NONE
    
    return (tasks,content_ver)
    
def write_tasks_model_json(res, ver_str, fname):
    obj = {}
    obj['version'] = 'GEN: {}, CONTENT: {}'.format(__version__,ver_str)
    obj['tasks'] = res
    # Serializing json
    with open(fname,'w', encoding='utf8') as writer:
        json.dump(obj, writer, ensure_ascii=False, indent = 4)
        
def write_tasks_site_folder(res, task_root_dir):
    created_files = []
    for id in res.keys():
        desc = res[id]['desc']
        levels = id.split('.')
        assert len(levels) == 3
        folder = levels[0]
        file_name = levels[1]+'.md'
        caption = levels[2]
        
        full_folder = os.path.join(task_root_dir, folder)
        if not os.path.exists(full_folder):
           os.makedirs(full_folder)
        full_path = os.path.join(full_folder, file_name)
        if full_path not in created_files:
           created_files.append(full_path)
           with open(full_path,'w', encoding='utf8') as writer:
                writer.write('\n')
        
        with open(full_path,'a', encoding='utf8') as writer:
                text = desc.replace('\\n','\n')
                writer.write('* ({}.py) - {}    \n'.format(caption, text))
    
if __name__ == "__main__":
    print('Version: {}'.format(__version__))
    content = ''
    with open('../../docs/tech/coding_tasks.md', encoding='utf8') as reader:
        content = reader.read()
    content = content+'\n\n'
    res, ver_str = parse_tasks_md(content)
    write_tasks_model_json(res,ver_str, '../../site/tasks.json')
    write_tasks_site_folder(res, '../../site/example_auto_site')
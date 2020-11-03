try:
    import invoke
except ImportError as e:
    print('Модуль inoke не установлен! Используйте команду `pip install invoke` для установки.')
    exit(1)

from invoke import Collection, task
import os
import io
import sys
import json
import imp
import builtins
from datetime import datetime

__version__ = '0.2'

def _fatal(msg):
    print(msg, file=sys.stderr)
    exit(1)

def _prepare_dir(path):
    if os.path.exists(path):
        return
    else:
        try:
            os.makedirs(path)
        except OSError:
            _fatal('Не могу создать каталог {}'.format(path))

def _prepare_model(path):
    if not os.path.exists(path):
        _fatal('Нет файла модели {}!'.format(path))
    with open(path, encoding='utf8') as reader:
        content = reader.read()
    m = json.loads(content)
    if (not isinstance(m["version"],str)) or (not isinstance(m["tasks"],dict)):
        _fatal('Некорректный файл модели {}!'.format(path))
    return m

def _gen_task_content(tspec):
    c = '""""Задание: {}"""\n\n'.format(tspec["desc"].replace('\\n','\n'))
    #нет входных аргументов
    noneArgs = (len(tspec["test_col"]) == 0)
    if noneArgs:
        c = c + 'def main():\n'
    else:
        args = ','.join(tspec["test_col"])
        c = c + 'def main({}):\n'.format(args)
    c = c + "    print('?')\n\n\n"
    if len(tspec["tests"]) < 1:
        _fatal('Некорректный тест для модели {}!'.format(tspec["desc"]))
    c = c + "if __name__=='__main__':\n    #Проверьте себя. Правильный ответ `{}`\n".format(tspec["tests"][0][-1])
    if noneArgs:
        c = c + '    main()'
    else:
        args = ','.join(tspec["tests"][0][0:-1])
        c = c + '    main({})'.format(args)
    return c

def _argslist_from_spec(tspec, pos):
    vars = tspec["vars"]
    cols = tspec["test_col"]
    out_list = []
    show_list = []
    if pos >= len(tspec["tests"]):
        _fatal('{} Некорректная дина тестов в спецификации.'.format(tspec["desc"]))
    curr_test = tspec["tests"][pos]
    for i in range(len(cols)):
        var = cols[i]
        if var not in vars:
            _fatal('Нет переменной  {} в типах {}! Некорректная спецификация.'.format(var,tspec["desc"]))
        tp = vars[var]
        elem = None
        if tp == 'int':
            elem = int(curr_test[i])
        elif tp == 'float':
            elem = float(curr_test[i])
        elif tp == 'str':
            elem = curr_test[i]
        else:
           _fatal('Неопределенный тип переменной {} в тесте {}! Некорректная спецификация.'.format(var,tspec["desc"]))
        out_list.append(elem)
        show_list.append('{}={}'.format(var,elem))
    if len(show_list) == 0:
       show_list.append('нет')
    return (out_list,','.join(show_list))
    
def _is_equal(expected,current,type):
    if type == 'str':
        return expected == current
    elif type == 'int':
        try:
            exp_int = int(expected)
            cur_int = int(current)
        except ValueError:
            return False
        return exp_int == cur_int
    elif type == 'float':
        try:
            exp_float_s = '{:.2f}'.format(float(expected))
            cur_float_s = '{:.2f}'.format(float(current))
        except ValueError:
            return False
        return exp_float_s == cur_float_s
    _fatal('Неопределенный тип сравнения {}! Некорректная спецификация.'.format(type))

def _create_diary_model(spec):
    m = {}
    m["spec"] = spec["version"]
    m["repet"] = __version__
    m["total_tasks"] = len(spec["tasks"].keys())
    m["section"] = {}
    for tid in spec["tasks"].keys():
        parts = tid.split('.')
        if len(parts) != 3:
            _fatal('Некорректный формат id для задания {}! Возможно, спецификация повреждена, обновите её или обратитесь к разработчику.'.format(tid))
        section = '.'.join(parts[:-1])
        if section not in m["section"]:
            m["section"][section] = 1
        else:
            m["section"][section] = m["section"][section]+1
    m["completed"] = []
    m["log"] = []
    return m
    
def _upgrade_diary_model(m,spec):
    m["spec"] = spec["version"]
    m["repet"] = __version__
    m["total_tasks"] = len(spec["tasks"].keys())
    m["section"] = {}
    for tid in spec["tasks"].keys():
        parts = tid.split('.')
        if len(parts) != 3:
            _fatal('Некорректный формат id для задания {}! Возможно, спецификация повреждена, обновите её или обратитесь к разработчику.'.format(tid))
        section = '.'.join(parts[:-1])
        if section not in m["section"]:
            m["section"][section] = 1
        else:
            m["section"][section] = m["section"][section]+1
    #TODO: проверить все ли выполненные задачи есть в спецификации...
    
def _print_progress(m):
    count_sec={}
    for tid in m["completed"]:
        parts = tid.split('.')
        if len(parts) != 3:
            _fatal('Некорректный формат id для задания {}! Возможно, спецификация повреждена, обновите её или обратитесь к разработчику.'.format(tid))
        section = '.'.join(parts[:-1])
        if section not in count_sec:
            count_sec[section] = 1
        else:
            count_sec[section] = count_sec[section]+1
    print('Прогресс по разделам:')
    for sec in count_sec.keys():
        comp_sec = count_sec[sec]
        total_sec = m["section"][sec]
        print('   {}: {}%({}/{})'.format(sec,int((comp_sec/total_sec)*100),comp_sec,total_sec))
    comp = len(m["completed"])
    total = m["total_tasks"]
    print('Общий прогресс: {}%({}/{})'.format(int((comp/total)*100),comp,total))
    
def _update_diary(dia, tid, isOk, spec):
    if not os.path.exists(dia):
        _fatal('Нет дневника оценок, подготовьте рабочее окружение для создания дневника.')
    with open(dia, encoding='utf8') as reader:
        content = reader.read()
    m = json.loads(content)
    if m["spec"] != spec["version"]:
        print('Версия спецификации изменилась, попытка обновления.')
        _upgrade_diary_model(m,spec)
    if tid in m["completed"]:
        print('Тестовое задание было ранее выполнено, результат в дневнике не отразился.')
        #_print_progress(m)
    else:
        factor = ""
        if isOk:
            m["completed"].append(tid)
            factor = "+"
            _print_progress(m)
        else:
            factor = "-"
        now = datetime.now()
        date_time = now.strftime("%d.%m.%Y-%H:%M:%S")
        m["log"].append('{},{},{}'.format(date_time,tid,factor))
        with io.open(dia, "w", encoding='UTF-8') as f:
            f.write(json.dumps(m))
    
def _exist_marker(path):
    if os.path.exists(path):
        return "+"
    return "-"
    
def _tid_to_path(tid, ws):
    parts = tid.split('.')
    if len(parts) != 3:
        _fatal('Некорректный формат id для задания {}! Возможно, спецификация повреждена, обновите её или обратитесь к разработчику.'.format(tid))
    path_to_task_dir = os.path.join(ws,parts[0],parts[1])
    _prepare_dir(path_to_task_dir)
    path_to_file = os.path.join(path_to_task_dir,parts[2]+'.py')
    return path_to_file

_g_print_list = []  
def _prepare_list():
    global _g_print_list
    _g_print_list = []
    
def _print_to_list(*args, **kwargs):
    global _g_print_list
    if len(args) != 1 or len(kwargs) != 0:
        _fatal('Некорректный формат печати в функции print. Должен быть только один аргумент, например: print("hello") или print(8.9).')
    _g_print_list.append(str(args[0]))
    
def _get_print_res():
    global _g_print_list
    return '\n'.join(_g_print_list)
    
@task
def settings(c):
    """
    Отображает текущие настройки и наличие файлов по указанным путям
    """
    print("Спецификация: {} ({})".format(c.spec,_exist_marker(c.spec)))
    print("Workspace:    {} ({})".format(c.ws,_exist_marker(c.ws)))
    print("Дневник:      {} ({})".format(c.diary,_exist_marker(c.diary)))
    
@task(help={'spec': "Путь к спецификации заданий"})
def versions(c, spec=None):
    """
    Отображает версии компонентов
    """
    print("Версия репетитора: {}".format(__version__))
    if spec is None:
        spec = c.spec
    if not os.path.exists(spec):
        print("Версия спецификации: нет")
    else:
        m = _prepare_model(spec)
        print("Версия спецификации: {}".format(m["version"]))
            
@task(help={'ws': "Путь к workspace",'spec': "Путь к спецификации заданий",'dia':"Путь к дневнику"})
def prepare(c, spec=None, ws=None, dia=None):
    """
    Подготавливает workspace для учебной работы
    """
    if ws is None:
        ws = c.ws
    if spec is None:
        spec = c.spec
    if dia is None:
        dia = c.diary
    m = _prepare_model(spec)
    tasks_ids = m["tasks"].keys()
    print("Подготовка рабочего простанства в калатоге: {}. Заданий: {}".format(ws,len(tasks_ids)))
    _prepare_dir(ws)
    for id in tasks_ids:
        path_to_file = _tid_to_path(id,ws)
        if os.path.exists(path_to_file):
            print('Файл {} существует. Для повторного создания шаблона, удалите его вручную. '.format(path_to_file))
        else:
            print('Генерация файла {}'.format(path_to_file))
            content = _gen_task_content(m["tasks"][id])
            with io.open(path_to_file, "w", encoding='UTF-8') as f:
                f.write(content)

    if not os.path.exists(dia):
        print('Создание дневника в каталоге {}'.format(dia))
        content = json.dumps(_create_diary_model(m))
        with io.open(dia, "w", encoding='UTF-8') as f:
            f.write(content)
    print("Успешно!")

@task(help={'task': "Идентификатор задачи",'ws': "Путь к workspace",'spec': "Путь к спецификации заданий",'dia':"Путь к дневнику"})
def test(c, task, spec=None, ws=None, dia=None):
    """
    Выполняет набор тестов для задачи и записывает результат в дневник
    """
    if ws is None:
        ws = c.ws
    if spec is None:
        spec = c.spec
    if dia is None:
        dia = c.diary
    m = _prepare_model(spec)
    if task.endswith('.py'):
        task = task[0:-3]
    if len(task) < 3:
        _fatal('Слишком короткий идентификатор, должен быть минимум 3 символа.')
    tasks_ids = list(m["tasks"].keys())
    tid = None
    matches = [x for x in tasks_ids if task in x]
    if len(matches) == 0:
        _fatal('Совпадений не найдено, попробуйте изменить идентификатор для поиска.')
    elif len(matches) > 1:
        for x in matches:
            ind = tasks_ids.index(x)
            if tasks_ids[ind] == x:
                matches = [x]
                break
        if len(matches) > 1:
            _fatal('Найдено несколько совпадений, измените поиск для уточнения: {}'.format(','.join(matches)))
    
    tid = matches[0]
    path = _tid_to_path(tid,ws)
    print('Тестирование для задачи {}, путь: {}'.format(tid,path))
    sys.path.append(os.path.abspath(os.path.dirname(path)))
    pm = __import__(os.path.basename(path)[:-3])
    
    tspec = m["tasks"][tid]
    argsNum = len(tspec["test_col"])
    
    original_print = print
    builtins.print = _print_to_list
    
    for i in range(len(tspec["tests"])):
        (args,show) = _argslist_from_spec(tspec,i)
        etal = tspec["tests"][i][-1]
        etal=etal.replace('\\n','\n')
        original_print('Проверка #{}. Вход: {}'.format(i,show))
        _prepare_list()
        if argsNum == 0:
            pm.main()
        elif argsNum == 1:
            pm.main(args[0])
        elif argsNum == 2:
            pm.main(args[0],args[1])
        elif argsNum == 3:
            pm.main(args[0],args[1],args[2])
        elif argsNum == 4:
            pm.main(args[0],args[1],args[2],args[3])
        elif argsNum == 5:
            pm.main(args[0],args[1],args[2],args[3],args[4])
        elif argsNum == 6:
            pm.main(args[0],args[1],args[2],args[3],args[4],args[5])
        elif argsNum == 7:
            pm.main(args[0],args[1],args[2],args[3],args[4],args[5],args[6])
        elif argsNum == 8:
            pm.main(args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7])
        elif argsNum == 9:
            pm.main(args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7],args[8])
        elif argsNum == 10:
            pm.main(args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7],args[8],args[9])
        else:
           _fatal('Неверное количество аргументов для задания {}'.format(tid))
        res = _get_print_res()
        if (_is_equal(etal,res,tspec["out_type"])):
            original_print('ok')
        else:
            builtins.print = original_print
            _update_diary(dia,tid,False,m)
            print('Ошибка. Ожидается: `{}`, в решении: `{}`'.format(etal,res))
            return
    
    builtins.print = original_print
    print('Задание выполнено!')
    _update_diary(dia,tid,True,m)
    
ns = Collection(settings,versions,prepare,test)
ns.configure({'spec': "tasks.json",'ws': "workspace",'diary': "marks.json"})
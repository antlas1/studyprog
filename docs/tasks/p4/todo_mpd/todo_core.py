"""
Пакет todo_core содержит список функций для работы со списком задач
"""

def add(todo_dict, todo_text):
    """Добавляет текст новой задачи к словарику задач.
        Если аргумент todo_dict задан None, Возвращает новый словарик
    """
    if todo_dict is None:
        todo_dict = {}
    keylist = list(todo_dict.keys())
    if len(keylist) > 1:
        #определяем крайний номер списка
        keylist.sort()
        next_id = keylist[-1]+1
    elif len(keylist) == 1:
        next_id = keylist[0]+1
    else:
        next_id = 1
    #добавляем элемент в список
    todo_dict[next_id] = todo_text
    return todo_dict
  
def rem(todo_dict, num):
    """Удаляет задачу по конкретному номеру. todo_dict-текущий словарик, num - позиция. При ошибке вернет None.
    Возвращает новый словарик.
    """
    if todo_dict is None:
        return None
    keylist = list(todo_dict.keys())
    if num not in keylist:
        return None
    todo_dict.pop(num)
    return todo_dict
    
def display(todo_dict, print_fun):
    """Вывод словаря через функцию печати вида print_fun(id,text)"""
    if todo_dict is None:
        todo_dict = {}
    keylist = list(todo_dict.keys())
    keylist.sort()
    for key in keylist:
        print_fun(key,todo_dict[key])
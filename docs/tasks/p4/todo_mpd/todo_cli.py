from argparse import ArgumentParser
from pickle import dump, load
from os.path import isfile
from todo_core import add, rem, display

def print_fun(key,text):
    print("{}    {}".format(key,text))

if __name__ == "__main__":
    parser = ArgumentParser(prog='TODO LIST CLI')
    parser.add_argument('command', type=str, help='Command name: `add` - adding task, `remove` - removing, `view` - view all tasks')
    parser.add_argument('param', type=str, nargs='?', help='Text for adding or number for removing.')
    args = parser.parse_args()
    todo_dict = None
    if isfile('todo.pickle'):
        with open('todo.pickle', 'rb') as f:
            todo_dict = load(f)
    if args.command == 'add':
        if args.param != None:
            todo_dict = add(todo_dict,args.param)
            with open('todo.pickle', 'wb') as f:
                dump(todo_dict,f)
            print('OK!')
        else:
            print('Cannot add empty task!')
    elif args.command == 'rem':
        if args.param != None:
            new_dict = rem(todo_dict,int(args.param))
            if new_dict is None:
                print('Error removing dict element!')
            else:
                todo_dict = new_dict
                with open('todo.pickle', 'wb') as f:
                    dump(todo_dict,f)
                print('OK!')
        else:
            print('Cannot remove empty task!')
    elif args.command == 'view':
        if (todo_dict is None) or ((todo_dict is not None) and (len(todo_dict)==0)):
            print('Empty todo!')
        else:
            print("ID     TEXT")
            print("-----------")
            display(todo_dict,print_fun)
                
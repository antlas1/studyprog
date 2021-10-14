TODO: добавить пример интерактивного ввода от пользователя, минусы и переход к аргументам командной строки.

Концепции
Давайте покажем, какие функции мы собираемся изучить в этом вводном учебнике, используя команду ls :

$ ls
cpython  devguide  prog.py  pypy  rm-unused-function.patch
$ ls pypy
ctypes_configure  demo  dotviewer  include  lib_pypy  lib-python ...
$ ls -l
total 20
drwxr-xr-x 19 wena wena 4096 Feb 18 18:51 cpython
drwxr-xr-x  4 wena wena 4096 Feb  8 12:04 devguide
-rwxr-xr-x  1 wena wena  535 Feb 19 00:05 prog.py
drwxr-xr-x 14 wena wena 4096 Feb  7 00:59 pypy
-rw-r--r--  1 wena wena  741 Feb 18 01:01 rm-unused-function.patch
$ ls --help
Usage: ls [OPTION]... [FILE]...
List information about the FILEs (the current directory by default).
Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.
...
Несколько концепций, которые мы можем изучить с помощью четырех команд:

Команда ls полезна при запуске без каких-либо параметров. По умолчанию отображается содержимое текущего каталога.
Если мы хотим выйти за рамки того, что она предоставляет по умолчанию, мы сообщаем ей немного больше. В этом случае мы хотим, чтобы отображался другой каталог, pypy. Мы указали так называемый позиционный аргумент. Он назван так потому, что программа должна знать, что делать со значением, исключительно в зависимости от того, где оно отображается в командной строке. Эта концепция более актуальна для такой команды, как cp, чье основное использование - cp SRC DEST. Первая позиция — это то, что вы хотите скопировать, а вторая позиция ,куда вы хотите скопировать.
Допустим, мы хотим изменить поведение программы. В нашем примере мы отображаем дополнительную информацию для каждого файла, а не просто отображаем имена файлов. -l в этом случае известен как необязательный аргумент.
Это очень полезно, поскольку вы можете встретить программу, которой никогда раньше не пользовались, и понять, как она работает, просто прочитав её справочный текст.
Основы
Начнём с очень простого примера, который (почти) ничего не делает:

import argparse
parser = argparse.ArgumentParser()
parser.parse_args()
Результат выполнения кода :

$ python3 prog.py
$ python3 prog.py --help
usage: prog.py [-h]

optional arguments:
  -h, --help  show this help message and exit
$ python3 prog.py --verbose
usage: prog.py [-h]
prog.py: error: unrecognized arguments: --verbose
$ python3 prog.py foo
usage: prog.py [-h]
prog.py: error: unrecognized arguments: foo
Вот что происходит:

Запуск скрипта без каких-либо параметров не приводит к тому, что на стандартный вывод ничего не выводится. Не так уж и полезно.
Второй начинает отображать полезность модуля argparse. Мы почти ничего не сделали, но уже получили приятное справочное сообщение.
Параметр --help, который также можно сократить до -h, является единственным вариантом, который мы получаем бесплатно (т. е. указывать его не нужно). Указание чего-либо ещё приводит к ошибке. Но даже в этом случае мы получаем полезное сообщение об использовании, также бесплатно.
Знакомство с позиционными аргументами¶
Пример:

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo")
args = parser.parse_args()
print(args.echo)
И запускаем код:

$ python3 prog.py
usage: prog.py [-h] echo
prog.py: error: the following arguments are required: echo
$ python3 prog.py --help
usage: prog.py [-h] echo

positional arguments:
  echo

optional arguments:
  -h, --help  show this help message and exit
$ python3 prog.py foo
foo
Вот что происходит:

Мы добавили метод add_argument(), чтобы указать, какие параметры командной строки программа готова принять. В данном случае я назвал его echo, чтобы он соответствовал его функционалу.
Теперь для вызова нашей программы необходимо указать параметр.
Метод parse_args() фактически возвращает некоторые данные из указанных параметров, в данном случае echo.
Переменная представляет собой некую форму «магии», которую argparse выполняет бесплатно (т. е. нет необходимости указывать, в какой переменной хранится это значение). Вы также заметите, что его имя совпадает со строковым аргументом, переданным методу, echo.
Обратите внимание, что, хотя отображение справки выглядит красиво и всё такое, в настоящее время оно не так полезно, как могло бы быть. Например, мы видим, что мы получили echo в качестве позиционного аргумента, но мы не знаем, что он делает, кроме как путём предположения или чтения исходного кода. Итак, давайте сделаем его более полезным:

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")
args = parser.parse_args()
print(args.echo)
И мы получаем:

$ python3 prog.py -h
usage: prog.py [-h] echo

positional arguments:
  echo        echo the string you use here

optional arguments:
  -h, --help  show this help message and exit
А теперь как насчёт чего-нибудь ещё более полезного:

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number")
args = parser.parse_args()
print(args.square**2)
Следующее является результатом выполнения кода :

$ python3 prog.py 4
Traceback (most recent call last):
  File "prog.py", line 5, in <module>
    print(args.square**2)
TypeError: unsupported operand type(s) for ** or pow(): 'str' and 'int'
Всё пошло не так хорошо. Это потому, что argparse обрабатывает параметры, которые мы ему передаём, как строки, если мы не укажем иное. Итак, давайте скажем argparse рассматривать этот ввод как целое число:

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number",
                    type=int)
args = parser.parse_args()
print(args.square**2)
Результат выполнения кода :

$ python3 prog.py 4
16
$ python3 prog.py four
usage: prog.py [-h] square
prog.py: error: argument square: invalid int value: 'four'
Все прошло хорошо. Программа теперь даже услужливо завершает работу при неверном недопустимом вводе, прежде чем продолжить.

Знакомство с необязательными аргументами¶
До сих пор мы играли с позиционными аргументами. Давайте посмотрим, как добавить необязательные:

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--verbosity", help="increase output verbosity")
args = parser.parse_args()
if args.verbosity:
    print("verbosity turned on")
И вывод:

$ python3 prog.py --verbosity 1
verbosity turned on
$ python3 prog.py
$ python3 prog.py --help
usage: prog.py [-h] [--verbosity VERBOSITY]

optional arguments:
  -h, --help            show this help message and exit
  --verbosity VERBOSITY
                        increase output verbosity
$ python3 prog.py --verbosity
usage: prog.py [-h] [--verbosity VERBOSITY]
prog.py: error: argument --verbosity: expected one argument
Вот что происходит:

Программа написана таким образом, чтобы отображать что-то, когда указан --verbosity, и ничего не отображать, когда не указан.
Чтобы показать, что эта опция на самом деле является необязательной, при запуске программы без неё не будет ошибок. Обратите внимание, что по умолчанию, если необязательный аргумент не используется, соответствующей переменной, в данном случае args.verbosity, присваивается значение None, что является причиной того, что она не проходит проверку истинности оператора if.
Справочное сообщение немного другое.
При использовании параметра --verbosity необходимо также указать какое-то значение, любое значение.
Приведенный выше пример принимает произвольные целочисленные значения для --verbosity, но для нашей простой программы на самом деле полезны только два значения: True или False. Давайте соответствующим образом изменим код:

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
if args.verbose:
    print("verbosity turned on")
И вывод:

$ python3 prog.py --verbose
verbosity turned on
$ python3 prog.py --verbose 1
usage: prog.py [-h] [--verbose]
prog.py: error: unrecognized arguments: 1
$ python3 prog.py --help
usage: prog.py [-h] [--verbose]

optional arguments:
  -h, --help  show this help message and exit
  --verbose   increase output verbosity
Вот что происходит:

Параметр теперь больше похож на флаг, чем на то, что требует значения. Мы даже изменили название опции, чтобы она соответствовала этой идее. Обратите внимание, что теперь мы указываем новое ключевое слово action и присваиваем ему значение "store_true". Это означает, что, если опция указана, присвоить значение True args.verbose. Отсутствие указания подразумевает False.
Она жалуется, когда вы указываете значение, в истинном духе того, что на самом деле есть флаги.
Обратите внимание на другой текст справки.
Короткие опции¶
Если вы знакомы с использованием командной строки, вы заметите, что я ещё не затронул тему коротких версий опций. Все очень просто:

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
if args.verbose:
    print("verbosity turned on")
Результат запуска:

$ python3 prog.py -v
verbosity turned on
$ python3 prog.py --help
usage: prog.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  increase output verbosity
Обратите внимание, что новая способность также отражена в тексте справки.

Сочетание позиционных и необязательных аргументов¶
Наша программа постоянно усложняется:

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbose:
    print("the square of {} equals {}".format(args.square, answer))
else:
    print(answer)
А теперь вывод:

$ python3 prog.py
usage: prog.py [-h] [-v] square
prog.py: error: the following arguments are required: square
$ python3 prog.py 4
16
$ python3 prog.py 4 --verbose
the square of 4 equals 16
$ python3 prog.py --verbose 4
the square of 4 equals 16
Мы вернули позиционный аргумент, отсюда и жалоба.
Учтите, что порядок не имеет значения.
Как насчёт того, чтобы вернуть нашей программе возможность получать несколько значений детализации и фактически использовать их:

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", type=int,
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity == 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity == 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
И вывод:

$ python3 prog.py 4
16
$ python3 prog.py 4 -v
usage: prog.py [-h] [-v VERBOSITY] square
prog.py: error: argument -v/--verbosity: expected one argument
$ python3 prog.py 4 -v 1
4^2 == 16
$ python3 prog.py 4 -v 2
the square of 4 equals 16
$ python3 prog.py 4 -v 3
16
Все они выглядят хорошо, кроме последнего, который обнаруживает ошибку в нашей программе. Давайте исправим это, ограничив значения, которые может принимать параметр --verbosity:

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity == 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity == 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
И вывод:

$ python3 prog.py 4 -v 3
usage: prog.py [-h] [-v {0,1,2}] square
prog.py: error: argument -v/--verbosity: invalid choice: 3 (choose from 0, 1, 2)
$ python3 prog.py 4 -h
usage: prog.py [-h] [-v {0,1,2}] square

positional arguments:
  square                display a square of a given number

optional arguments:
  -h, --help            show this help message and exit
  -v {0,1,2}, --verbosity {0,1,2}
                        increase output verbosity
Обратите внимание, что изменение также отражается как в сообщении об ошибке, так и в строке справки.

А теперь давайте воспользуемся другим подходом к игре с многословием, который довольно распространен. Он также соответствует тому, как исполняемый файл CPython обрабатывает свой собственный аргумент подробности (проверьте вывод python --help):

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display the square of a given number")
parser.add_argument("-v", "--verbosity", action="count",
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity == 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity == 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
Мы ввели ещё одно действие, «count», для подсчёта количества появлений определенных необязательных аргументов:

$ python3 prog.py 4
16
$ python3 prog.py 4 -v
4^2 == 16
$ python3 prog.py 4 -vv
the square of 4 equals 16
$ python3 prog.py 4 --verbosity --verbosity
the square of 4 equals 16
$ python3 prog.py 4 -v 1
usage: prog.py [-h] [-v] square
prog.py: error: unrecognized arguments: 1
$ python3 prog.py 4 -h
usage: prog.py [-h] [-v] square

positional arguments:
  square           display a square of a given number

optional arguments:
  -h, --help       show this help message and exit
  -v, --verbosity  increase output verbosity
$ python3 prog.py 4 -vvv
16
Да, теперь это скорее флаг (похожий на action="store_true") в предыдущей версии нашего скрипта. Это должно объяснить жалобу.
Он также ведёт себя аналогично действию «store_true».
А теперь демонстрация того, что дает действие «count». Вы, наверное, видели раньше такое использование.
И если вы не укажете флаг -v, считается, что этот флаг содержит значение None.
Как и следовало ожидать, указав длинную форму флага, мы должны получить тот же результат.
К сожалению, наша справка не очень информативна о новой способности, которую приобрёл наш скрипт, но это всегда можно исправить, улучшив документацию для нашего скрипта (например, с помощью ключевого аргумента help).
Последний вывод обнаруживает ошибку в нашей программе.
Давайте исправим:

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", action="count",
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2

# исправление ошибки: замените == на >=
if args.verbosity >= 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity >= 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
Результат работы программы:

$ python3 prog.py 4 -vvv
the square of 4 equals 16
$ python3 prog.py 4 -vvvv
the square of 4 equals 16
$ python3 prog.py 4
Traceback (most recent call last):
  File "prog.py", line 11, in <module>
    if args.verbosity >= 2:
TypeError: '>=' not supported between instances of 'NoneType' and 'int'
Первый вывод прошёл успешно и исправляет ошибку, которая была у нас раньше. То есть мы хотим, чтобы любое значение >= 2 было максимально подробным.
Третий вывод не очень хороший.
Давайте исправим эту ошибку:

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", action="count", default=0,
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity >= 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity >= 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
Мы только что ввели ещё одно ключевое слово, default. Мы установили его на 0, чтобы сопоставить его с другими значениями int. Помните, что по умолчанию, если необязательный аргумент не указан, он получает значение None, которое нельзя сравнивать со значением int (отсюда и исключение TypeError).

И:

$ python3 prog.py 4
16
Вы можете пойти довольно далеко, используя то, что мы уже изучили, а мы лишь прикоснулись к нему поверхностно. Модуль argparse очень мощный, и мы рассмотрим его ещё немного, прежде чем закончить это руководство.

Немного более продвинутый¶
Что, если бы мы хотели расширить нашу крошечную программу для выполнения других функций, а не только квадратов:

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
parser.add_argument("-v", "--verbosity", action="count", default=0)
args = parser.parse_args()
answer = args.x**args.y
if args.verbosity >= 2:
    print("{} to the power {} equals {}".format(args.x, args.y, answer))
elif args.verbosity >= 1:
    print("{}^{} == {}".format(args.x, args.y, answer))
else:
    print(answer)
Вывод:

$ python3 prog.py
usage: prog.py [-h] [-v] x y
prog.py: error: the following arguments are required: x, y
$ python3 prog.py -h
usage: prog.py [-h] [-v] x y

positional arguments:
  x                the base
  y                the exponent

optional arguments:
  -h, --help       show this help message and exit
  -v, --verbosity
$ python3 prog.py 4 2 -v
4^2 == 16
Обратите внимание, что до сих пор мы использовали уровень детализации для изменения отображаемого текста. В следующем примере вместо этого используется уровень детализации для отображения большего количества текста:

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
parser.add_argument("-v", "--verbosity", action="count", default=0)
args = parser.parse_args()
answer = args.x**args.y
if args.verbosity >= 2:
    print("Running '{}'".format(__file__))
if args.verbosity >= 1:
    print("{}^{} == ".format(args.x, args.y), end="")
print(answer)
Вывод:

$ python3 prog.py 4 2
16
$ python3 prog.py 4 2 -v
4^2 == 16
$ python3 prog.py 4 2 -vv
Running 'prog.py'
4^2 == 16
Противоречивые опции¶
До сих пор мы работали с двумя методами экземпляра argparse.ArgumentParser. Давайте представим третий, add_mutually_exclusive_group(). Это позволяет нам указывать параметры, которые конфликтуют друг с другом. Давайте также изменим остальную часть программы, чтобы новая функциональность имела больше смысла: мы представим параметр --quiet, который будет противоположным параметру --verbose:

import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
args = parser.parse_args()
answer = args.x**args.y

if args.quiet:
    print(answer)
elif args.verbose:
    print("{} to the power {} equals {}".format(args.x, args.y, answer))
else:
    print("{}^{} == {}".format(args.x, args.y, answer))
Наша программа стала проще, и мы потеряли некоторые функциональные возможности для демонстрации. В любом случае, вот результат:

$ python3 prog.py 4 2
4^2 == 16
$ python3 prog.py 4 2 -q
16
$ python3 prog.py 4 2 -v
4 to the power 2 equals 16
$ python3 prog.py 4 2 -vq
usage: prog.py [-h] [-v | -q] x y
prog.py: error: argument -q/--quiet: not allowed with argument -v/--verbose
$ python3 prog.py 4 2 -v --quiet
usage: prog.py [-h] [-v | -q] x y
prog.py: error: argument -q/--quiet: not allowed with argument -v/--verbose
Это должно быть легко понять. Я добавил этот последний вывод, чтобы вы могли видеть ту гибкость, которую вы получаете, то есть смешивание вариантов длинной формы с вариантами короткой формы.

Прежде чем мы закончим, вы, вероятно, захотите рассказать своим пользователям об основном назначении вашей программы, если они не знают:

import argparse

parser = argparse.ArgumentParser(description="calculate X to the power of Y")
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
args = parser.parse_args()
answer = args.x**args.y

if args.quiet:
    print(answer)
elif args.verbose:
    print("{} to the power {} equals {}".format(args.x, args.y, answer))
else:
    print("{}^{} == {}".format(args.x, args.y, answer))
Обратите внимание на [-v | -q], который сообщает нам, что мы можем использовать -v или -q, но не оба одновременно

$ python3 prog.py --help
usage: prog.py [-h] [-v | -q] x y

calculate X to the power of Y

positional arguments:
  x              the base
  y              the exponent

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose
  -q, --quiet
Заключение¶
Модуль argparse предлагает гораздо больше, чем здесь показано. Его документы довольно подробны и полны примеров. Пройдя это руководство, вы должны легко их усвоить, не чувствуя себя ошеломленным.
Для сборки и выкладывания на сайт [https://alastochkinheroku.github.io/] должна быть структура:
```
studyprog/
    mkdocs.yml
    docs/
alastochkinheroku.github.io/
```
Проверить, то что страницы собираются в каталоге ```studyprog```:
```
mkdocs build
mkdocs serve
```
Перейти в каталог ```alastochkinheroku.github.io``` через ```git bash``` выполнить:
```
 mkdocs gh-deploy --config-file ../studyprog/mkdocs.yml --remote-branch master
```
Можно проверять сайт. Для обновления локальной копии:
```
git pull origin master
git reset --hard
```
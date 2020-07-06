<link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
<style>
    body {
        font-family: sans-serif;
    }
    code, pre {
        font-family: monospace;
    }
    h1 code,
    h2 code,
    h3 code,
    h4 code,
    h5 code,
    h6 code {
        font-size: inherit;
    }
    ul li {
        list-style-type: none;
    }
    table {
    @extend .table;
    }
</style>
<script src="https://code.jquery.com/jquery-3.4.1.min.js"
        integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo="
        crossorigin="anonymous"></script>

<div class="container">
    <div class="form-row">
        <div class="container">
            <h1>Пример вопросов</h1>
<hr>
<ul>
<li>
<p>Выберите правильное определение алгоритма:</p>
<ul class="radio-list">

<li><label><input type="radio" data-question="1" data-content="0" data-link=" 1.1.alg" /> Алгоритм - точно описанная последовательность последовательность команд для процессора.</label></li>
<li><label><input type="radio" data-question="0" data-content="1" data-link="" /> Алгоритм — точно описанная последовательность действий, ведущая к поставленной цели.</label></li>
<li><label><input type="radio" data-question="1" data-content="0" data-link="" /> Алгоритм - цель, для описания последовательности действий.</label></li>
</ul>
</li>
<li>
<p>Выберите правильное определение визуального алгоритма:</p>
<ul class="radio-list">

<li><label><input type="radio" data-question="1" data-content="0" data-link=" 1.1.valg,1.1.alg" /> Визуальный алгоритм — алгоритм, изображенный в виде текста на экране.</label></li>
<li><label><input type="radio" data-question="0" data-content="1" data-link="" /> Визуальный алгоритм — алгоритм, изображенный не в виде текста, а в виде наглядной картинки.</label></li>
</ul>
</li>
<li>
<p>Выберите правильное определение программы:    </p>
<ul class="radio-list">

<li><label><input type="radio" data-question="0" data-content="1" data-link=" 1.1.prog" /> Программа — последовательность действий, которые человек поручает компьютеру.</label></li>
<li><label><input type="radio" data-question="1" data-content="0" data-link="" /> Программа - последовательность действий.</label></li>
<li><label><input type="radio" data-question="1" data-content="0" data-link="" /> Программа - компьютерная обработка символьной информации.</label></li>
</ul>
</li>
<li>
<p>Примеры констант:</p>
<ul class="checklist">

<li><label><input type="checkbox" data-question="1" data-content="0" data-link="  1.2.const,s1.2.cvar" /> Человек</label></li>
<li><label><input type="checkbox" data-question="0" data-content="1" data-link="" /> 4.7</label></li>
<li><label><input type="checkbox" data-question="0" data-content="1" data-link="" /> Pi (3.1415...)</label></li>
</ul>
</li>
<li>
<p>Как называется имя переменной?</p>
<ul class="textbox">
<li><input type="text" data-content="ротакифитнеди" data-question="рsоsтsаsкsиsфsиsтsнsеsдsиs" data-link="1.2.desc" placeholder="Введите корректный ответ" class="form-control" /><i class="text-correct text-muted"></i></li>
</ul>
</li>
<li>
<p>Напишите код, который складывает два числа из переменных a,b в переменную c.</p>
<ul class="codebox">
<li><textarea type="text" data-content="{max_cycles:1000, inp_vars:['a','b'],ret_exp:'c',test_exp:['main(1,2)==3','main(4,5)==9','main(8,-8)==0']}" data-link="1.2.desc" placeholder="Введите корректный ответ" class="form-control"></textarea></li>
</ul>
</li>
</ul>
        </div>
    </div>
    <div id="tg-msg" class="alert" role="alert" style="display: none">
        <span id="tg-correct-questions"></span> <b>Результат:<span id="tg-score"></span>%</b><br>
        <span id="tg-diag">
    </div>
    <div class="row">
        <button id="check-questions" class="btn btn-lg btn-success">Проверить</button>
        <button id="reset-questions" class="btn btn-link">Заново</button>
    </div>
    <script type="text/javascript">$(function(){
    $('ul.radio-list,ul.checklist,ul.textbox,ul.codebox').each(function(i, el){
        var questionClass = $(this).attr('class');
        $(this).parent().addClass('question-row').addClass(questionClass);
        if (questionClass=='radio-list') {
            $(this).find('input[type="radio"]').attr('name', 'radio-question-' + i);
        }
    });
    
    var myInterpreter;

    function step() {
      if (myInterpreter.stateStack.length) {
        var node =
            myInterpreter.stateStack[myInterpreter.stateStack.length - 1].node;
        var start = node.start;
        var end = node.end;
      } else {
        var start = 0;
        var end = 0;
      }
      
      try {
        var ok = myInterpreter.step();
        if (!ok) {
          return;
        }
      } finally {
        if (!ok) {
          return;
        }
      }
    }
    
    //userCode=
    //function main() {
    //  var a;
    //  var b;
    //  var c;
    //  a = 5;
    //  b = 1;
    //  c = a+b;
    //}
    //setupObj = {max_cycles:1000, inp_vars:['a','b'],ret_exp:'c',test_exp:['main(1,2)==3','main(4,5)==9','main(8,-8)==0']}
    function runCodeTests(userCode, setupObj) {       
       //console.log(setupObj);
       //начинаем постепенно заменять пользовательский код на заглушечный
       var newCode = userCode;
       if (setupObj.hasOwnProperty("inp_vars")) {
          //замена переменных, если они есть среди входных параметров
          var inpArray = setupObj["inp_vars"];
          for (let i = 0; i < inpArray.length; i++) {
             var reNewVar = new RegExp("var\\s+"+inpArray[i]+"\\s*;");
             newCode = newCode.replace(reNewVar, '');
             var reFirstAssign = new RegExp(inpArray[i]+"\\s*=");
             newCode = newCode.replace(reFirstAssign, '//'+inpArray[i]+'=');
          }
          //Замена заголовка функции
          var reVoidMain = new RegExp("function\\s+main\\(\\s*\\)\\s*\\{");
          var inpParams = inpArray.join(',');
          newCode = newCode.replace(reVoidMain, 'function main('+inpParams+') {');
       }
       if (setupObj.hasOwnProperty("ret_exp")) {
          posFin = newCode.lastIndexOf('}');
          newCode = newCode.substring(0,posFin);
          newCode += 'return '+setupObj["ret_exp"]+';\n}\n';
       }
       
       newCode += "var valid = '';\n";
       if (setupObj.hasOwnProperty("test_exp")) {
          var testArray = setupObj["test_exp"];
          for (let i = 0; i < testArray.length; i++) {
             newCode += "if ("+testArray[i]+") valid+='1'; else valid+='0';\n";
          }
       }
       newCode += "valid+'';\n";
       
       
       console.log(newCode);
       var res = "";
       try {
        myInterpreter = new Interpreter(newCode);
        
        //Запускаем в течение n циклов
        for (let i = 0; i < setupObj["max_cycles"]; i++) {
           step();
        }
        res = myInterpreter.value;
       } catch(e) {
          console.log('Error parse code!');
      }
       
       //выдача финала
       var finishOk = true;
       var testArray = [];
       var ntest = setupObj["test_exp"].length;
       for (let i = 0; i < ntest; i++) {
          testArray.push('?');
       }
       var ansLen = ntest < res.length ? ntest : res.length;
       if (ntest == res.length) finishOk = true;
       else finishOk = false;
       for (let i = 0; i < ansLen; i++) {
          if (res.charAt(i) == 1) { 
             testArray[i]='1';
          }
          else if (res.charAt(i) == 0) {
             finishOk = false;
             testArray[i]='0';
          } else {
             finishOk = false;
          }
       }
       result = {ntest: ntest,ans: testArray,ok: finishOk}
       console.log('Finished! Res='+res+' out= '+JSON.stringify(result));
       return result;
    }

    function checkQuestion() {
        resetQuestions(true);
        var questions = $('li.question-row');
        var total_questions = questions.length;
        var correct = 0;
        var diagTable = '';

        questions.each(function(i, el) {
            var self = $(this);
            // Single Question.
            if (self.hasClass('radio-list')) {
                if (self.find('input[type="radio"][data-content="1"]:checked').length == 1) {
                    correct += 1;
                } else {
                    var linkItems = self.find('input[type="radio"][data-link!=""]');
                    linkItems.each(function(idx, li) {
                        var link = $(li);
                        diagTable += link.attr("data-link");
                        //console.log( "Radio " + idx + ":" + link.attr("data-link") );
                    });
                    self.addClass('text-danger');
                }
            }
            // Textbox Question.
            if(self.hasClass('textbox')) {
                var textbox = self.find('input[type="text"]');
                var correct_text = String(textbox.data("content")).trim().split("").reverse().join("");
                if(String(textbox.val()).trim().toLowerCase()==correct_text.toLowerCase()) {
                    correct += 1;
                } else {
                    var linkItems = self.find('input[type="text"][data-link!=""]');
                    linkItems.each(function(idx, li) {
                        var link = $(li);
                        diagTable += link.attr("data-link");
                        //console.log( "Textbox " + idx + ":" + link.attr("data-link") );
                    });
                    
                    self.addClass('text-danger');
                    textbox.parent().find("i.text-correct").html(correct_text);
                }
            }
            // Multiple selection Questions.
            if(self.hasClass('checklist')) {
                var total_corrects = self.find('input[type="checkbox"][data-content="1"]').length;
                var total_incorrects = self.find('input[type="checkbox"][data-content="0"]').length;
                var correct_selected = self.find('input[type="checkbox"][data-content="1"]:checked').length;
                var incorrect_selected = self.find('input[type="checkbox"][data-content="0"]:checked').length;
                var qc = +((correct_selected / total_corrects) - (incorrect_selected/total_incorrects)).toFixed(2);
                if (qc < 0) {
                    qc = 0;
                }
                correct += qc;
                var displayLinks = false;
                if (qc == 0) {
                    self.addClass('text-danger');
                    displayLinks = true;
                } else if (qc > 0 && qc < 1) {
                    self.addClass('text-warning');
                    displayLinks = true;
                }
                
                if (displayLinks){
                   var linkItems = self.find('input[type="checkbox"][data-link!=""]');
                   linkItems.each(function(idx, li) {
                        var link = $(li);
                        diagTable += link.attr("data-link");
                        //console.log( "Checkbox " + idx + ":" + link.attr("data-link") );
                   });
                }
            }
            //Codebox
            if(self.hasClass('codebox')) {
                var codebox = self.find('textarea');
                var test_code = String(codebox.data("content"));
                test_code=test_code.replace("max_cycles","\"max_cycles\"");
                test_code=test_code.replace("inp_vars","\"inp_vars\"");
                test_code=test_code.replace("ret_exp","\"ret_exp\"");
                test_code=test_code.replace("test_exp","\"test_exp\"");
                test_code=test_code.replace(/'/g,"\"");
                console.log( "Codebox test code="+test_code);
                var setup_obj = JSON.parse(test_code);
                var input_code = codebox.val();
                console.log( " input code="+input_code);
                res = runCodeTests(input_code,setup_obj);
                if (res["ok"]) {
                   correct += 1;
                }
                else
                {
                   var linkItems = self.find('input[type="text"][data-link!=""]');
                   linkItems.each(function(idx, li) {
                       var link = $(li);
                       diagTable += link.attr("data-link");
                       //console.log( "Textbox " + idx + ":" + link.attr("data-link") );
                   });
                   self.addClass('text-danger');
                }
            }
        });

        showScore(correct, total_questions, diagTable);
    }

    function showScore(correct, total, diag) {
        var score = (correct / total).toFixed(2) * 100;
        var msgClass = 'alert-danger';
        var diagText = '';
        if (score < 100) {
           diagText = 'Диагностическая таблица: '+diag;
        }
        if (score >= 70) {
            msgClass = 'alert-success';
        } else if (score >= 50) {
            msgClass = 'alert-warning';
        }
        $('#tg-correct-questions').text(correct + ' из ' + total);
        $('#tg-score').text(score);
        $('#tg-diag').text(diagText);
        $('#tg-msg').addClass(msgClass).show();
    }
    function resetQuestions(keep) {
        $('li.question-row').removeClass('text-danger').removeClass('text-warning');
        $('i.text-correct').html('');
        $('#tg-msg').removeClass('alert-danger').removeClass('alert-success').removeClass('alert-warning').hide();
        if(keep === true) {
            return;
        }
        $('li.question-row').find('input[type="text"]').val('');
        $('li.question-row').find('input[type="radio"],input[type="checkbox"]').prop('checked', false);
    }
    $('#check-questions').on('click', checkQuestion);
    $('#reset-questions').on('click', resetQuestions);

});</script>
</div>
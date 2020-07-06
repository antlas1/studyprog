$(function(){
    $('ul.radio-list,ul.checklist,ul.textbox').each(function(i, el){
        var questionClass = $(this).attr('class');
        $(this).parent().addClass('question-row').addClass(questionClass);
        if (questionClass=='radio-list') {
            $(this).find('input[type="radio"]').attr('name', 'radio-question-' + i);
        }
    });

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

});
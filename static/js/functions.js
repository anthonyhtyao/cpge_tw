$(document).on("click", ".open-reply", function () {
     var content = $(this).attr("comment-content");
     var author = $(this).attr("comment-author");
     var date = $(this).attr("comment-date");
     var id = $(this).attr("comment-id");
     var articleID = $(this).attr("article-id");
     $("#modal-media-content").html(content);
     $("#modal-media-date").html(date);
     $("#modal-media-heading").html(author);
     $("#reply-form").attr('action', '/articlecomment/' + id + '/' + articleID +'/');
     $.get('/articlecomment/' + id + '/' + articleID  , function(data, status){
        // alert("Data: " + data + "\nStatus: " + status);
        $(".modal-body").html(data);
    });
});

$(document).on("click", ".openAnswer", function () {
    var content = $(this).attr("question-content");
    var date = $(this).attr("question-date");
    var id = $(this).attr("question-id");
    var title = $(this).attr("question-title");
    $("#modal-media-content").html(content);
    $("#modal-media-date").html(date);
    $("#modal-media-title").html(title);
    $("#modal-answer-content").val("");
    $("#reply-form").attr('action','/question/' + id + '/');
});

$(document).on("click", ".editAnswer", function () {
    var questionContent = $(this).attr("question-content");
    var date = $(this).attr("question-date");
    var id = $(this).attr("question-id");
    var title = $(this).attr("question-title");
    var answerContent = $(this).attr("answer-content");
    $("#modal-media-content").html(questionContent);
    $("#modal-media-date").html(date);
    $("#modal-media-title").html(title);
    $("#modal-answer-content").val(answerContent);
    $("#reply-form").attr('action','/question/' + id + '/');
});

$(document).ready( function() {

    $("#login-btn").click( function (event) {
	    $("#dialog").dialog("open");
	    return false;
	});
    $("#dialog").dialog({autoOpen : false, modal : true, show : "blind", hide : "blind"});  
    $("#loginErrorDialog").dialog();

    $("#login_form").submit(function (event) {
        $.ajax({
            type:"POST",
            url:"/login/",
            data:$("#login_form").serialize(),
        });
    });
});

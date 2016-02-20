// $(document).ready( function() {

// 	$(".reply-comment").click( function() {
// 		$("#reply-dialog").dialog("open");
// 	});
// 	$("#reply-dialog").dialog({autoOpen : false, modal : true, show : "blind", hide : "blind"});  
// });

$(document).on("click", ".open-reply", function () {
     var content = $(this).attr("comment-content");
     var author = $(this).attr("comment-author");
     var date = $(this).attr("comment-date");
     var id = $(this).attr("comment-id");
     $("#modal-media-content").html(content);
     $("#modal-media-date").html(date);
     $("#modal-media-heading").html(author);
     $.get('/articlecomment/'+id, function(data, status){
        // alert("Data: " + data + "\nStatus: " + status);
        $(".modal-body").html(data);
    });
});
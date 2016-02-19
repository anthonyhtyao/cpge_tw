// $(document).ready( function() {

// 	$(".reply-comment").click( function() {
// 		$("#reply-dialog").dialog("open");
// 	});
// 	$("#reply-dialog").dialog({autoOpen : false, modal : true, show : "blind", hide : "blind"});  
// });

$(document).on("click", ".open-reply", function () {
     var myBookId = $(this).attr("data-id");
     var author = $(this).attr("comment-author")
     $("#modal-pid").html(myBookId);
     $("#modal-media-heading").html(author)
});
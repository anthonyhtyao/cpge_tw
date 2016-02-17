$(document).ready( function() {

	$(".reply-comment").click( function() {
		$("#reply-dialog").dialog("open");
	});
	$("#reply-dialog").dialog({autoOpen : false, modal : true, show : "blind", hide : "blind"});  
});


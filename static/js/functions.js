$(document).ready( function() {

    $("#login-btn").click( function (event) {
	    $("#dialog").dialog("open");
	    return false;
	});
	$("#dialog").dialog({autoOpen : false, modal : true, show : "blind", hide : "blind"});  
});


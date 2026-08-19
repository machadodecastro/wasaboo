/* Show and hide short description Remove link on mouseover */
$( document ).ready(function() {	
	$(".edit-short-description").mouseover(function(){
 	   $(".deletelink").css("display", "inline-block");
	});
	$(".edit-short-description").mouseout(function(){
	 	   $(".deletelink").css("display", "none");
		});	
});
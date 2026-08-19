/* Show or hide Profile Name edit link on mouseover */
$( document ).ready(function() {	
	$(".profile-name").mouseover(function(){
 	   $(".editlink").css("display", "inline-block");
	});
	$(".profile-name").mouseout(function(){
	 	   $(".editlink").css("display", "none");
		});	
});
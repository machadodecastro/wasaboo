//Restore a card in feed
$( document ).ready(function() {	
	$(".restore").on('click',function(){ 
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var card_id = $(this).data("id");
    	var profile = $(this).data("profile");
    	$.ajax({
    	   type: "GET", 
    	   dataType: 'json', 
    	   data: {card: card_id, profile: profile},
    	   url: "http://"+wasabooref+"/restore/"+card_id,
    	   async: true,
    	   contentType: "application/json; charset=utf-8",
    	   success: function (data, textStatus, jqXHR) {
	            if (data.teste == "restored") {
	            	$('.restore-label-'+card_id).val("Restoring card...");
	            	$('.card-'+card_id).fadeOut(1000, function(){ $(this).remove();});
	            	location.reload();
	            }else{
	            	//alert(error);
	            }
    		   },
                error: function(rs, e) {
                    //alert(rs.responseText);
                }
    	   });    	
	});
});
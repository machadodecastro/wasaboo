// Desfavoriting a card
$( document ).ready(function() {
	$(".favorite").on('click',function(){ 
	    	self = $(this);
	    	var wasabooref = $(this).data("url");
	    	var idTip = $(this).data("id");
	    	$.ajax({
		    	   type: "GET", 
		    	   dataType: 'json', 
		    	   data: {tip: idTip},
		    	   url: "//"+wasabooref+"/tips-desfavorites/"+idTip+"/",
		    	   async: true,
		    	   contentType: "application/json; charset=utf-8",
		    	   success: function (data, textStatus, jqXHR) {
			            if (data.teste == "no") {
			            	self.hide();
			            	$('.pbfavorite-'+idTip).show();
			            }else{
			            	//alert("Error");
			            }
		    		   },
		                error: function(rs, e) {
		                    //alert(rs.responseText);
		                }
		    	   });    	
	});
});
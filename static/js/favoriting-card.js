// Favoriting a card
$( document ).ready(function() {
	$(".pbfavorite").on('click',function(){
	    	self = $(this);
	    	var wasabooref = $(this).data("url");
	    	var idTip = $(this).data("id");
	    	var author = $(this).data("author");
		       $.ajax({
		    	   type: "GET", 
		    	   dataType: 'json', 
		    	   data: {tip: idTip, author: author},
		    	   url: "//"+wasabooref+"/tips-favorites/"+idTip+"/",
		    	   async: true,
		    	   contentType: "application/json; charset=utf-8",
		    	   success: function (data, textStatus, jqXHR) {
				            if (data.teste == "yes") {
				            	self.hide();
				            	$('.favorite-'+idTip).show();
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
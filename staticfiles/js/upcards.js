// Counting how many favoritings a card has 
$( document ).ready(function() {	
	$(".upcards").each(function(index, obj) {
			var x =[];
			x.push($(this).data("id"));
			
			var self = $(this);
			var wasabooref = $(this).data("url"); 
			var idCard = $(this).data("id");
		       $.ajax({
		    	   type: "GET", 
		    	   dataType: 'json', 
		    	   data: {card: idCard},
		    	   url: "//"+wasabooref+"/cards-upcards/"+idCard,
		    	   async: true,
		    	   contentType: "application/json; charset=utf-8",
		    	   success: function (data, textStatus, jqXHR) { 
		    		      
				            if (data.teste == "upcard") {
					            	if (data.upcards > 0){
					            		$(".upcards-counter-"+idCard).html(data.upcards);
					            	} else {
					            		$(".upcards-counter-"+idCard).html(0);
					            	}
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
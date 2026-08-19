// Counting how many favoritings a card has 
$( document ).ready(function() {	
	$(".likes").each(function(index, obj) {
		var x =[];
			//event.preventDefault();
			x.push($(this).data("id"));
			
			var self = $(this);
			var wasabooref = $(this).data("url"); 
			var idTip = $(this).data("id");
		       $.ajax({
		    	   type: "GET", 
		    	   dataType: 'json', 
		    	   url: "//"+wasabooref+"/tips-likes/"+idTip+"/",
		    	   async: true,
		    	   contentType: "application/json; charset=utf-8",
		    	   success: function (data, textStatus, jqXHR) { 
		    		      
				            if (data.teste == "yes") {
					            	if (data.likes > 0){
					            		$(".like-"+idTip).html("<img class='myfavorites'>   " + data.likes);
					            		$(".like-img-"+idTip).css("display","block");
					            	} else {
					            		//$(".like-"+idTip).html("<img class='myfavorites'> 0");
					            		$(".favoritings-"+idTip).css("display","none");
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
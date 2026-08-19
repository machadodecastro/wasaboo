	// CHANGE PROFILE BACKGROUND TO DEFAULT  
	$( document ).ready(function() {	
		$(".change-bkg-default").on('click',function (){    
	    	self = $(this);
	    	var wasabooref = $(this).data("url");
	    	var background = $(this).data("id");
	    	$.ajax({
		    	   type: "GET", 
		    	   url: "//"+wasabooref+"/change-background-default/"+background+"/",
		    	   dataType: 'json',
		    	   data: {background: background},
		    	   async: true,
		    	   contentType: "application/json; charset=utf-8",
		    	   success: function (data, textStatus, jqXHR) { 
			            if (data.teste == "default-background") { 
			            	location.reload();
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
<!-- UPDATE profile name in PROFILE --> 
	$( document ).ready(function() {	
		$(".edit-profile-name").on('click',function(){ 
			//event.preventDefault();
	    	self = $(this);
	
	    	var wasabooref = $(this).data("url");
	    	var profile = $(this).data("id"); 
	    	var nome = $( "#nome" ).val();
	    	$.ajax({
		    	   type: "GET", 
		    	   url: "http://"+wasabooref+"/edit-profile-name/"+profile,
		    	   dataType: 'json',
		    	   data: {profilename: nome},
		    	   async: true,
		    	   contentType: "application/json; charset=utf-8",
		    	   success: function (data, textStatus, jqXHR) { 
			            if (data.teste == "update") { 
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
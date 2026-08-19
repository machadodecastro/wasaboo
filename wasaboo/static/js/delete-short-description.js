<!-- DELETE short description text in PROFILE --> 
	$( document ).ready(function() {	
		$(".deletelink").on('click',function(){ 
			//event.preventDefault();
	    	self = $(this);
	
	    	var wasabooref = $(this).data("url");
	    	var profile = $(this).data("id"); 
	    	var description = $( "#short_description" ).val();
	    	var perfil = $("#profileId").val();
	    	$.ajax({
		    	   type: "GET", 
		    	   url: "http://"+wasabooref+"/delete-short-description/"+profile,
		    	   dataType: 'json',
		    	   data: {profileid: profile},
		    	   async: true,
		    	   contentType: "application/json; charset=utf-8",
		    	   success: function (data, textStatus, jqXHR) { 
			            if (data.teste == "delete") {  
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
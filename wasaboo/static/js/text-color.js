	// CHANGE PROFILE BACKGROUND TO DEFAULT  
	$( document ).ready(function() {	
		$(".white-brush").on('click',function (){    
	    	self = $(this);
	    	var wasabooref = $(this).data("url");
	    	var background = $(this).data("id");
	    	var user = $(this).data("user");
	    	var profile = $(this).data("profile");
	    	$.ajax({
		    	   type: "GET", 
		    	   url: "http://"+wasabooref+"/change-white-text/"+background,
		    	   dataType: 'json',
		    	   data: {background: background, user: user, profile: profile},
		    	   async: true,
		    	   contentType: "application/json; charset=utf-8",
		    	   success: function (data, textStatus, jqXHR) { 
			            if (data.teste == "white-text") { 
			            	$('.profile-name-'+user).css('color','#FFF');
			            	$('.edit-description-'+profile).css('color','#FFF');
			            	$('.white-brush-'+background).css('display','none');
			            	$('.black-brush-'+background).css('display','block');
			            }else{
			            	//alert("Error");
			            }
		    		   		
		    		   },
		                error: function(rs, e) {
		                    //alert(rs.responseText);
		                }
		    	   });    	
		});
		
		$(".black-brush").on('click',function (){    
	    	self = $(this);
	    	var wasabooref = $(this).data("url");
	    	var background = $(this).data("id");
	    	var user = $(this).data("user");
	    	var profile = $(this).data("profile");
	    	$.ajax({
		    	   type: "GET", 
		    	   url: "http://"+wasabooref+"/change-black-text/"+background,
		    	   dataType: 'json',
		    	   data: {background: background, user: user, profile: profile},
		    	   async: true,
		    	   contentType: "application/json; charset=utf-8",
		    	   success: function (data, textStatus, jqXHR) { 
			            if (data.teste == "black-text") { 
			            	$('.profile-name-'+user).css('color','#000');
			            	$('.edit-description-'+profile).css('color','#000');
			            	$('.black-brush-'+background).css('display','none');
			            	$('.white-brush-'+background).css('display','block');
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
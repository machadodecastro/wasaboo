//TURN OFF WORLDS IN INDEX
$( document ).ready(function() {
	$(".world-on").on('click',function(){ 
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var profile = $(this).data("profile");
    	var map = $(this).data("map");

    	$.ajax({
     	   type: "GET", 
     	   dataType: 'json',
     	   data: {profile:profile, map:map},
     	   url: "//"+wasabooref+"/world-on/"+profile+"/",
     	   async: true,
     	   contentType: "application/json; charset=utf-8",
     	   success: function (data, textStatus, jqXHR) {
 	            if (data.teste == "on") {
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

	
$( document ).ready(function() {
	//TURN ON  WORLDS IN INDEX
	$(".world-off").on('click',function(){ 
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var profile = $(this).data("profile");
    	var map = $(this).data("map");

    	$.ajax({
     	   type: "GET", 
     	   dataType: 'json',
     	   data: {profile:profile, map:map},
     	   url: "//"+wasabooref+"/world-off/"+profile+"/",
     	   async: true,
     	   contentType: "application/json; charset=utf-8",
     	   success: function (data, textStatus, jqXHR) {
 	            if (data.teste == "off") {
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
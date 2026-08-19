//Hide a card
$( document ).ready(function() {
	$(".checkbox-map-on").on('click',function(){ 
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var profile = $(this).data("profile");
    	var map = $(this).data("map");

    	$.ajax({
     	   type: "GET", 
     	   dataType: 'json',
     	   data: {profile:profile, map:map},
     	   url: "//"+wasabooref+"/map-off/"+profile+"/",
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
	
	$(".checkbox-map-off").on('click',function(){ 
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var profile = $(this).data("profile");
    	var map = $(this).data("map");

    	$.ajax({
     	   type: "GET", 
     	   dataType: 'json',
     	   data: {profile:profile, map:map},
     	   url: "//"+wasabooref+"/map-on/"+profile+"/",
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


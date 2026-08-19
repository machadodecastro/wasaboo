//FYS
$( document ).ready(function() {
	$(".adidas-on").on('click',function(){ 
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var profile = $(this).data("profile");
    	var map = $(this).data("map");

    	$.ajax({
     	   type: "GET", 
     	   dataType: 'json',
     	   data: {profile:profile, map:map},
     	   url: "//"+wasabooref+"/adidas-on/"+profile+"/",
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
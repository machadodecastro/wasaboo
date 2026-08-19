/*Script for publish short description*/ 
$( document ).ready(function() {	
	$(".publish-short-description").on('click',function(){ 
		event.preventDefault();
    	self = $(this);

    	var wasabooref = "{{url}}";
    	var profile = $(this).data("id"); 
    	var description = $( "#short_description" ).val();
    	$.ajax({
	    	   type: "GET", 
	    	   url: "http://"+wasabooref+"/edit_short_description/"+profile,
	    	   dataType: 'json',
	    	   data: {text: description},
	    	   async: true,
	    	   contentType: "application/json; charset=utf-8",
	    	   success: function (data, textStatus, jqXHR) { 
		            if (data.teste == "description") { 
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

$("#short_description").textareaShortDescriptionCounter();
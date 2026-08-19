// Delete a card in Index  
$( document ).ready(function() {	
	$(".notifications-control").on('click',function (){    
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var tip = $(this).data("id");
    	$.ajax({
	    	   type: "GET",
	    	   dataType: 'json',
	    	   url: "//"+wasabooref+"/delete-notification/"+tip+"/",
	    	   async: true,
	    	   data: {tip: tip},	    	   
	    	   contentType: "application/json; charset=utf-8",
	    	   success: function (data, textStatus, jqXHR) { 
		            if (data.teste == "removednotification") { 
		            	$('.card-'+tip).removeClass('go-play');
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
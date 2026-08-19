// Delete a card in Index  
$( document ).ready(function() {	
	$(".btn-yes").on('click',function (){    
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var tip = $(this).data("id");
    	$.ajax({
	    	   type: "GET",
			   dataType: 'json',
	    	   url: "//"+wasabooref+"/delete-tip/"+tip+"/",
	    	   async: true,
	    	   data: {tip: tip},
	    	   contentType: "application/json; charset=utf-8",
	    	   success: function (data, textStatus, jqXHR) { 
		            if (data.teste == "removedtip") { 
		            	$('.card-'+tip).fadeTo(1, 0);
		            	$('.card-'+tip).remove();
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

//Delete a card  in Card Page
$( document ).ready(function() {	
	$(".btn-yes-in-card").on('click',function (){    
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var tip = $(this).data("id");
    	$.ajax({
	    	   type: "GET", 
			   dataType: 'json',
	    	   url: "//"+wasabooref+"/delete-tip/"+tip+"/",
	    	   data: {tip: tip},
	    	   async: true,
	    	   contentType: "application/json; charset=utf-8",
	    	   success: function (data, textStatus, jqXHR) { 
		            if (data.teste == "removedtip") { 
		            	$('.card-'+tip).fadeTo(1, 0);
		            	$('.card-'+tip).remove();
		            	location.reload();
		            	$('.no-published-warning').show();
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
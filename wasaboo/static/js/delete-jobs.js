// Delete JOBS profile information 
$( document ).ready(function() {	
	$(".delete-jobs").on('click',function (){    
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var tip = $(this).data("id"); 
    	$.ajax({
	    	   type: "GET", 
	    	   url: "http://"+wasabooref+"/delete-jobs/"+tip,
	    	   dataType: 'json',
	    	   data: {tip: tip},
	    	   async: true,
	    	   contentType: "application/json; charset=utf-8",
	    	   success: function (data, textStatus, jqXHR) { 
		            if (data.teste == "removedjobs") { 
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
// Revert a hided card in HIDED
$( document ).ready(function() {
	$(".publish-tip").on('click',function(){ 
		//event.preventDefault();
    	self = $(this);

    	var wasabooref = $(this).data("url");
    	var hideTip = $(this).data("id");	
    	$.ajax({
    	   type: "GET", 
    	   dataType: 'json', 
    	   url: "http://"+wasabooref+"/tips/show/"+hideTip,
    	   async: true,
    	   contentType: "application/json; charset=utf-8",
    	   success: function (data, textStatus, jqXHR) {
	            if (data.teste == "show") {
	            	$('.card-'+hideTip).fadeTo(1, 0);
	            }else{
	            	//alert("Error");
	            }
		    },
            error: function(rs, e) {
                //alert(rs.responseText);
            }
    	   });    	
	});



	$(".publish-no-fade").on('click',function(){ 
		//event.preventDefault();
		self = $(this);
	
		var wasabooref = $(this).data("url");
		var hideTip = $(this).data("id");
		$.ajax({
		   type: "GET", 
		   dataType: 'json', 
		   url: "http://"+wasabooref+"/tips/show/"+hideTip,
		   async: true,
		   contentType: "application/json; charset=utf-8",
		   success: function (data, textStatus, jqXHR) {
	            if (data.teste == "show") {
	            	self.hide();
	            	$(".eye-"+hideTip).show();
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
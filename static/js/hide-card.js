//Hide a card
$( document ).ready(function() {
	$(".eye").on('click',function(){ 
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var hideTip = $(this).data("id");
    	$.ajax({
    	   type: "GET", 
    	   dataType: 'json', 
    	   url: "//"+wasabooref+"/tips-hide/"+hideTip+"/",
    	   async: true,
    	   contentType: "application/json; charset=utf-8",
    	   success: function (data, textStatus, jqXHR) {
	            if (data.teste == "hide") {
	            	$('.card-'+hideTip).fadeOut(1000, function(){ $(this).remove();});
	            }else{
	            	//alert("Error");
	            }
    		   },
                error: function(rs, e) {
                    //alert(rs.responseText);
                }
    	   });    	
	});

	
	$(".hide-no-fade").on('click',function(){ 
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var hideTip = $(this).data("id");
    	$.ajax({
    	   type: "GET", 
    	   dataType: 'json', 
    	   url: "//"+wasabooref+"/tips-hide/"+hideTip+"/",
    	   async: true,
    	   contentType: "application/json; charset=utf-8",
    	   success: function (data, textStatus, jqXHR) {
	            if (data.teste == "hide") {
	            	self.hide();
	            	$(".eye-to-publish-"+hideTip).show();
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


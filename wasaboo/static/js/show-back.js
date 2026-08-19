// Back to card frontend
$( document ).ready(function() {	
	$(".show-back").on('click',function (){    
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var tip = $(this).data("id"); 
    	var content = $(this).data("content");
    	var show = $(this).data("reference");
    	$.ajax({
	    	   type: "GET", 
	    	   url: "http://"+wasabooref+"/show-content/"+tip,
	    	   dataType: 'json',
	    	   data: {tip: tip, content:JSON.stringify(content)},
	    	   async: true,
	    	   contentType: "application/json; charset=utf-8",
	    	   success: function (data, textStatus, jqXHR) {   
		            if (data.teste == "showcontent") {
		            	 
		            	$('.title-content-'+tip).froalaEditor('html.set', content);
		            	$('.title-content-'+tip).froalaEditor('edit.off');
		            	$('.picture-'+tip).show();
		            	$(".show-references-"+tip).show();
		            	$(".show-back-"+tip).hide();
		            	$('.confirm-delete-question-'+tip).hide();
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
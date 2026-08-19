// Show references about the card 
$( document ).ready(function() {	
	$(".show-references").on('click',function (){    
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var tip = $(this).data("id"); 
    	var content = $(this).data("content");
    	var show = $(this).data("reference");
    	$.ajax({
	    	   type: "GET", 
	    	   url: "http://"+wasabooref+"/show-references/"+tip,
	    	   dataType: 'json',
	    	   data: {tip: tip, show:JSON.stringify(show)},
	    	   async: true,
	    	   contentType: "application/json; charset=utf-8",
	    	   success: function (data, textStatus, jqXHR) {   
		            if (data.teste == "showreferences") {		            	
		            	$('.title-content-'+tip).froalaEditor('html.set', show);
		            	$('.title-content-'+tip).froalaEditor('edit.off');
		            	$('.picture-'+tip).hide();
		            	$(".show-references-"+tip).hide();
		            	$(".show-back-"+tip).show();
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

// Show references about the card 
$( document ).ready(function() {	
	$(".show-references").on('click',function (){ 
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var tip = $(this).data("id"); 
    	var content = $(this).data("content");
    	var show = $(this).data("reference");
		$('.dot-'+tip).animate({"animation-duration":"1.3s"}, 0);
    	$.ajax({
	    	   type: "GET", 
	    	   url: "//"+wasabooref+"/show-references/"+tip,
	    	   data: {tip: tip, show:JSON.stringify(show)},
	    	   async: true,
	    	   contentType: "application/json; charset=utf-8",
	    	   success: function (data, textStatus, jqXHR) {
						if (show) {
	   		   			    $('.title-content-'+tip).css('display','block');
	   		   		    }
		            	$('.title-content-'+tip).froalaEditor('html.set', show);
		            	$('.title-content-'+tip).froalaEditor('edit.off');
		            	$('.picture-'+tip).hide();
		            	$(".show-references-"+tip).hide();
		            	$(".show-back-"+tip).show();
		            	$('.confirm-delete-question-'+tip).hide();
						$('.dot-'+tip).animate({"animation-duration":"0s"}, 0);
	    		   },
	                error: function(rs, e) {
	                    //alert(rs.responseText);
	                }
	    	   });    	
	});
});

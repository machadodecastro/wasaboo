// Back to card frontend
$( document ).ready(function() {	
	$(".show-back").on('click',function (){  
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var tip = $(this).data("id"); 
    	var content = $(this).data("content");
		$('.dot-'+tip).animate({"animation-duration":"0s"}, 0);
    	$.ajax({
	    	   type: "GET", 
	    	   url: "//"+wasabooref+"/show-content/"+tip+"/",
	    	   data: {tip: tip, content:JSON.stringify(content)},
	    	   async: true,
	    	   contentType: "application/json; charset=utf-8",
	    	   success: function (data, textStatus, jqXHR) {
						if (content) {
	    		   			$('.title-content-'+tip).css('display','block');
		    		   	} else {
		    		   		$('.title-content-'+tip).css('display','none');
		    		   	}	
		            	$('.title-content-'+tip).froalaEditor('html.set', content);
		            	$('.title-content-'+tip).froalaEditor('edit.off');
		            	$('.picture-'+tip).show();
		            	$('.tag-'+tip).show();
		            	$('.fotorama-'+tip).show();
		            	$(".show-references-"+tip).show();
		            	$(".show-back-"+tip).hide();
		            	$('.confirm-delete-question-'+tip).hide();
	    		},
	                error: function(rs, e) {
	                    //alert(rs.responseText);
	                }
	    	   });    	
	});
});
// Remove card from folder
$( document ).ready(function() {
	$(".btn-folder-remove").on('click',function (){    
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var content = $(this).data("content");
    	var tip = $(this).data("id"); 
    	 
    	$.ajax({
	    	   type: "GET", 
	    	   url: "http://"+wasabooref+"/remove-from-folder/"+tip,
	    	   dataType: 'json',
	    	   data: {tip: tip, content: content},
	    	   async: true,
	    	   contentType: "application/json; charset=utf-8",
	    	   success: function (data, textStatus, jqXHR) { 
		            if (data.teste == "removedfromfolder") { 
		            	$('.title-content-'+tip).froalaEditor('html.set', content);
		            	$('.title-content-'+tip).froalaEditor('edit.off');
		               	$('.confirm-folders-options-'+tip).hide();	
		               	$('.show-references-'+tip).show();
		            	$('.show-back-'+tip).hide();
		            	$('.panel-heading-'+tip).show();
		            	$('.picture-'+tip).show();
		            	$('.choose-folders-'+tip).show();
		            	$('.show-folders-'+tip).hide();
		            	$('.deck-name-'+tip).hide();
		            	$('.folder-container-'+tip).hide();
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


//Remove card from folder in CARD page
$( document ).ready(function() {
	$(".btn-folder-remove-in-card").on('click',function (){    
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var content = $(this).data("content");
    	var reference = $(this).data("reference");
    	var tip = $(this).data("id"); 
    	 
    	$.ajax({
	    	   type: "GET", 
	    	   url: "http://"+wasabooref+"/remove-from-folder/"+tip,
	    	   dataType: 'json',
	    	   data: {tip: tip, content: content},
	    	   async: true,
	    	   contentType: "application/json; charset=utf-8",
	    	   success: function (data, textStatus, jqXHR) { 
		            if (data.teste == "removedfromfolder") { 
		            	$('.title-outdoor-'+tip).show();
		            	$('.title-content-'+tip).froalaEditor('html.set', reference);
		            	$('.title-content-'+tip).froalaEditor('edit.off');
		               	$('.confirm-folders-options-'+tip).hide();	
		            	$('.panel-heading-'+tip).show();
		            	$('.picture-'+tip).show();
		            	$('.choose-folders-in-card-'+tip).show();
		            	$('.show-folders-in-card-'+tip).hide();
		            	$('.deck-name-'+tip).hide();
		            	$('.folder-container-'+tip).hide();
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


//Remove card from folder in DECK page
$( document ).ready(function() {
	$(".btn-folder-remove-in-deck").on('click',function (){    
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var content = $(this).data("content");
    	var reference = $(this).data("reference");
    	var tip = $(this).data("id"); 
    	 
    	$.ajax({
	    	   type: "GET", 
	    	   url: "http://"+wasabooref+"/remove-from-folder/"+tip,
	    	   dataType: 'json',
	    	   data: {tip: tip, content: content},
	    	   async: true,
	    	   contentType: "application/json; charset=utf-8",
	    	   success: function (data, textStatus, jqXHR) { 
		            if (data.teste == "removedfromfolder") { 
		            	$('.card-'+tip).fadeOut(1000, function(){ $(this).remove();});
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
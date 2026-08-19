// Save card into folder
$( document ).ready(function() {
	$(".btn-folder").on('click',function (){    
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var content = $(this).data("content");
    	var tip = $(this).data("id"); 
    	var deck = $(".folder-select-"+tip+" .folder-option:selected").val(); 
    	var folder = $(".folder-select-"+tip+" .folder-option:selected").text();
    	 
    	$.ajax({
	    	   type: "GET", 
	    	   url: "//"+wasabooref+"/save-into-folder/"+tip+"/",
	    	   dataType: 'json',
	    	   data: {tip: tip, deck: deck, folder: folder, content: content},
	    	   async: true,
	    	   cache: false,
	    	   contentType: "application/json; charset=utf-8",
	    	   success: function (data, textStatus, jqXHR) { 
		            if (data.teste == "folderedtip") { 
		            	$('.title-content-'+tip).froalaEditor('html.set', content);
		            	$('.title-content-'+tip).froalaEditor('edit.off');
		               	$('.confirm-folders-options-'+tip).hide();	
		               	$('.show-references-'+tip).show();
		            	$('.show-back-'+tip).hide();
		            	$('.panel-heading-'+tip).show();
		            	$('.picture-'+tip).show();
		            	$('.choose-folders-'+tip).hide();
		            	$('.show-folders-'+tip).show();
		            	$('<span class="deck-name-'+tip+'"><a href="/deck/'+deck+'">'+ folder +'</a></span>').prependTo('.folder-container-'+tip);
		            	$('.folder-container-'+tip).innerHTML('<div class="confirm-folder-btn"> <input type="button" class="btn btn-danger btn-cancel" value="Cancel" data-id="'+tip+'" data-content="'+content+'"> <div></div> <input type="button" class="btn btn-danger btn-folder-remove btn-folder-remove-'+tip+'" value="Remove from folder" data-id="'+tip+'" data-content="'+content+'"></div>');
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


//Save card into folder
$( document ).ready(function() {
	$(".btn-folder-in-card").on('click',function (){    
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var content = $(this).data("content");
    	var reference = $(this).data("reference");
    	var tip = $(this).data("id"); 
    	var deck = $(".folder-select-"+tip+" .folder-option:selected").val(); 
    	var folder = $(".folder-select-"+tip+" .folder-option:selected").text();
    	 
    	$.ajax({
	    	   type: "GET", 
	    	   url: "//"+wasabooref+"/save-into-folder/"+tip+"/",
	    	   dataType: 'json',
	    	   data: {tip: tip, deck: deck, folder: folder, content: content, reference: reference},
	    	   async: true,
	    	   cache: false,
	    	   contentType: "application/json; charset=utf-8",
	    	   success: function (data, textStatus, jqXHR) { 
		            if (data.teste == "folderedtip") { 
		            	$('.title-outdoor-'+tip).show();
		            	$('.title-content-'+tip).froalaEditor('html.set', reference);
		            	$('.title-content-'+tip).froalaEditor('edit.off');
		               	$('.confirm-folders-options-'+tip).hide();	
		            	$('.panel-heading-'+tip).show();
		            	$('.picture-'+tip).show();
		            	$('.choose-folders-in-card-'+tip).hide();
		            	$('.show-folders-in-card-'+tip).show();
		            	$('<span class="deck-name-'+tip+'"><a href="/deck/'+deck+'" class="deck-label">'+ folder +'</a></span>').prependTo('.folder-container-'+tip);
		            	$('.folder-container-'+tip).innerHTML('<div class="confirm-folder-btn"> <input type="button" class="btn btn-danger btn-cancel-in-card" value="Cancel" data-id="'+tip+'" data-content="'+content+'" data-reference="'+reference+'"> <div></div> <input type="button" class="btn btn-danger btn-folder-remove-in-card btn-folder-remove-in-card'+tip+'" value="Remove from folder" data-id="'+tip+'" data-content="'+content+'" data-reference="'+reference+'"></div>');
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
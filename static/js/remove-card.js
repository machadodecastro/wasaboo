//Remove a card by option or infringement
$( document ).ready(function() {

	$(".discard").on('click',function(){ 
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var card_id = $(this).data("id");
    	$.ajax({
    	   type: "GET", 
    	   dataType: 'json', 
    	   data: {card: card_id},
    	   url: "//"+wasabooref+"/remove-by-discard/"+card_id+"/",
    	   async: true,
    	   contentType: "application/json; charset=utf-8",
    	   success: function (data, textStatus, jqXHR) {
	            if (data.teste == "discard") {
	            	$('.close').click();
	            	$('.card-'+card_id).fadeOut(100, function(){ $(this).remove();});
	            	//location.reload();
	        	    $.ajax({
	        	        dataType : 'html',
	        	        contentType: false,
	        	        processData: false,
	        	        success: function(response) { //on success
	        	        	//LOAD SCRIPTS WITHOUT AJAX CALLS
	        	        	$.getScript( '/static/js/scripts-loader.js');
	        	        	
	        	            // AJAX CALLS
	        	            $.getScript( '/static/js/upcards.js');
	        	            $.getScript( '/static/js/show-references.js');
	        	        	$.getScript( '/static/js/show-back.js');
	        	        	$.getScript( '/static/js/favoriting-card.js');
	        	        	$.getScript( '/static/js/desfavoriting-card.js');
	        	        	$.getScript( '/static/js/hide-card.js');
	        	        	$.getScript( '/static/js/publish-card.js');
	        	        	$.getScript( '/static/js/counting-favoritings.js');
	        	        	$.getScript( '/static/js/who-favorited.js');
	        	        	$.getScript( '/static/js/delete-card-btn-yes.js');
	        	        	$.getScript( '/static/js/save-to-folder.js');
	        	        	$.getScript( '/static/js/delete-from-folder.js');
	        	        	$.getScript( '/static/js/jquery.jscroll.js');
	        	        	$.getScript( '/static/js/focus.js');
	        	        	$.getScript( '/static/js/words-count-edit-tip.js');
	        	        	$.getScript( '/static/js/remove-card.js');
	        	        	
	        	        	// LOAD HTML
	        	        	$('.card-waterfall').html(jQuery(response).find('.card-waterfall').html());
	        	        	$('.my-upcards-waterfall').html(jQuery(response).find('.my-upcards-waterfall').html());
	        	        	$('.table-waterfall').html(jQuery(response).find('.table-waterfall').html());
	        	        	//location.reload();
	        	        	
	        	        	// CLOSE MODAL	        	
	        	        	$('body').removeClass('modal-open');
	        	        	$('.close').click();
	        	        }
	        	    });
	            }else{
	            	//alert("Error");
	            }
    		   },
                error: function(rs, e) {
                    //alert(rs.responseText);
                }
    	   });    	
	});
	
	
	$(".harassment").on('click',function(){ 
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var card_id = $(this).data("id");
    	$.ajax({
    	   type: "GET", 
    	   dataType: 'json', 
    	   data: {card: card_id},
    	   url: "//"+wasabooref+"/remove-by-harassment/"+card_id+"/",
    	   async: true,
    	   contentType: "application/json; charset=utf-8",
    	   success: function (data, textStatus, jqXHR) {
	            if (data.teste == "harassment") {
	            	$('.close').click();
	            	$('.card-'+card_id).fadeOut(1000, function(){ $(this).remove();});
	            	$('.play-btn-'+card_id).fadeOut(1000, function(){ $(this).remove();});
	            }else{
	            	//alert("Error");
	            }
    		   },
                error: function(rs, e) {
                    //alert(rs.responseText);
                }
    	   });    	
	});
	

	$(".spam").on('click',function(){ 
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var card_id = $(this).data("id");
    	$.ajax({
    	   type: "GET", 
    	   dataType: 'json', 
    	   data: {card: card_id},
    	   url: "//"+wasabooref+"/remove-by-spam/"+card_id+"/",
    	   async: true,
    	   contentType: "application/json; charset=utf-8",
    	   success: function (data, textStatus, jqXHR) {
	            if (data.teste == "spam") {
	            	$('.close').click();
	            	$('.card-'+card_id).fadeOut(1000, function(){ $(this).remove();});
	            	$('.play-btn-'+card_id).fadeOut(1000, function(){ $(this).remove();});
	            }else{
	            	//alert("Error");
	            }
    		   },
                error: function(rs, e) {
                    //alert(rs.responseText);
                }
    	   });    	
	});

	
	$(".plagiarism").on('click',function(){ 
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var card_id = $(this).data("id");
    	$.ajax({
    	   type: "GET", 
    	   dataType: 'json', 
    	   data: {card: card_id},
    	   url: "//"+wasabooref+"/remove-by-plagiarism/"+card_id+"/",
    	   async: true,
    	   contentType: "application/json; charset=utf-8",
    	   success: function (data, textStatus, jqXHR) {
	            if (data.teste == "plagiarism") {
	            	$('.close').click();
	            	$('.card-'+card_id).fadeOut(1000, function(){ $(this).remove();});
	            	$('.play-btn-'+card_id).fadeOut(1000, function(){ $(this).remove();});
	            }else{
	            	//alert("Error");
	            }
    		   },
                error: function(rs, e) {
                    //alert(rs.responseText);
                }
    	   });    	
	});

	
	$(".joke").on('click',function(){ 
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var card_id = $(this).data("id");
    	$.ajax({
    	   type: "GET", 
    	   dataType: 'json', 
    	   data: {card: card_id},
    	   url: "//"+wasabooref+"/remove-by-joke/"+card_id+"/",
    	   async: true,
    	   contentType: "application/json; charset=utf-8",
    	   success: function (data, textStatus, jqXHR) {
	            if (data.teste == "joke") {
	            	$('.close').click();
	            	$('.card-'+card_id).fadeOut(1000, function(){ $(this).remove();});
	            	$('.play-btn-'+card_id).fadeOut(1000, function(){ $(this).remove();});
	            }else{
	            	//alert("Error");
	            }
    		   },
                error: function(rs, e) {
                    //alert(rs.responseText);
                }
    	   });    	
	});


	$(".out").on('click',function(){ 
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var card_id = $(this).data("id");
    	$.ajax({
    	   type: "GET", 
    	   dataType: 'json', 
    	   data: {card: card_id},
    	   url: "//"+wasabooref+"/remove-by-out/"+card_id+"/",
    	   async: true,
    	   contentType: "application/json; charset=utf-8",
    	   success: function (data, textStatus, jqXHR) {
	            if (data.teste == "out") {
	            	$('.close').click();
	            	$('.card-'+card_id).fadeOut(1000, function(){ $(this).remove();});
	            	$('.play-btn-'+card_id).fadeOut(1000, function(){ $(this).remove();});
	            }else{
	            	//alert("Error");
	            }
    		   },
                error: function(rs, e) {
                    //alert(rs.responseText);
                }
    	   });    	
	});
	
	
	$(".written").on('click',function(){ 
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var card_id = $(this).data("id");
    	$.ajax({
    	   type: "GET", 
    	   dataType: 'json', 
    	   data: {card: card_id},
    	   url: "//"+wasabooref+"/remove-by-written/"+card_id+"/",
    	   async: true,
    	   contentType: "application/json; charset=utf-8",
    	   success: function (data, textStatus, jqXHR) {
	            if (data.teste == "written") {
	            	$('.close').click();
	            	$('.card-'+card_id).fadeOut(1000, function(){ $(this).remove();});
	            	$('.play-btn-'+card_id).fadeOut(1000, function(){ $(this).remove();});
	            }else{
	            	//alert("Error");
	            }
    		   },
                error: function(rs, e) {
                    //alert(rs.responseText);
                }
    	   });    	
	});	


	$(".fake").on('click',function(){ 
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var card_id = $(this).data("id");
    	$.ajax({
    	   type: "GET", 
    	   dataType: 'json', 
    	   data: {card: card_id},
    	   url: "//"+wasabooref+"/remove-by-fake/"+card_id+"/",
    	   async: true,
    	   contentType: "application/json; charset=utf-8",
    	   success: function (data, textStatus, jqXHR) {
	            if (data.teste == "fake") {
	            	$('.close').click();
	            	$('.card-'+card_id).fadeOut(1000, function(){ $(this).remove();});
	            	$('.play-btn-'+card_id).fadeOut(1000, function(){ $(this).remove();});
	            }else{
	            	//alert("Error");
	            }
    		   },
                error: function(rs, e) {
                    //alert(rs.responseText);
                }
    	   });    	
	});
	
	
	$(".image").on('click',function(){ 
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var card_id = $(this).data("id");
    	$.ajax({
    	   type: "GET", 
    	   dataType: 'json', 
    	   data: {card: card_id},
    	   url: "//"+wasabooref+"/remove-by-image/"+card_id+"/",
    	   async: true,
    	   contentType: "application/json; charset=utf-8",
    	   success: function (data, textStatus, jqXHR) {
	            if (data.teste == "image") {
	            	$('.close').click();
	            	$('.card-'+card_id).fadeOut(1000, function(){ $(this).remove();});
	            	$('.play-btn-'+card_id).fadeOut(1000, function(){ $(this).remove();});
	            }else{
	            	//alert("Error");
	            }
    		   },
                error: function(rs, e) {
                    //alert(rs.responseText);
                }
    	   });    	
	});	
	
	
	$(".incorrect").on('click',function(){ 
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var card_id = $(this).data("id");
    	$.ajax({
    	   type: "GET", 
    	   dataType: 'json', 
    	   data: {card: card_id},
    	   url: "//"+wasabooref+"/remove-by-incorrect/"+card_id+"/",
    	   async: true,
    	   contentType: "application/json; charset=utf-8",
    	   success: function (data, textStatus, jqXHR) {
	            if (data.teste == "incorrect") {
	            	$('.close').click();
	            	$('.card-'+card_id).fadeOut(1000, function(){ $(this).remove();});
	            	$('.play-btn-'+card_id).fadeOut(1000, function(){ $(this).remove();});
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


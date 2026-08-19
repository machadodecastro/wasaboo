//Show delete folder confirm question 
$(".delete-confirm-deck").on('click',function (){
	self = $(this);
	var tip = $(this).data("id");
	//show confirm question
   	$('.confirm-delete-folder-'+tip).show();
   	$('.panel-heading-'+tip).hide();
   	$('.deck-label-'+tip).hide();	
});

//Button NO - Cancel folder delete
$(".delete-deck-no").on('click',function (){  
	self = $(this);
	var tip = $(this).data("id"); 
	var content = $(this).data("content"); 
	//hide confirm question
	$('.confirm-delete-folder-'+tip).hide();	
	$('.panel-heading-'+tip).show();
	$('.deck-label-'+tip).show();
});

//Delete a card  
$( document ).ready(function() {	
	$(".delete-deck-yes").on('click',function (){    
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var deck = $(this).data("id");
    	$.ajax({
	    	   type: "GET", 
	    	   url: "//"+wasabooref+"/delete-deck/"+deck+"/",
	    	   dataType: 'json',
	    	   data: {deck: deck},
	    	   async: true,
	    	   contentType: "application/json; charset=utf-8",
	    	   success: function (data, textStatus, jqXHR) { 
		            if (data.teste == "removedfolder") { 
		            	$('.card-'+deck).fadeTo(1, 0);
		            	$('.card-'+deck).remove();
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

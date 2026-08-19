//Share button for facebook and whatsapp on cards toolbar
$(".share-social").on('click',function(){ 
	self = $(this);
	var id = $(this).data("id"); 
	$('.fb-option-'+id).show();
    $('.wa-option-'+id).show();	
    $('.share-social-'+id).hide();	
    setTimeout(function(){ 
    	$('.fb-option-'+id).hide();
    	$('.wa-option-'+id).hide();	
    	$('.share-social-'+id).show(); }, 5000);
});

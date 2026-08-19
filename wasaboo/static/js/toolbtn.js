//Show play/table toolbar
$( document ).ready(function() {	
	//Show play/table toolbar 
	$(".toolbtn").on('click',function(){ 
		self = $(this);
		var id = $(this).data("id"); 
		$('.points-'+id).animate({  borderSpacing: 0 }, {
		    step: function(now,fx) {
		    	$('.points-'+id).removeClass('rudder-active');
		        $(this).css('-webkit-transform','rotate('+now+'deg)'); 
		        $(this).css('-moz-transform','rotate('+now+'deg)');
		        $(this).css('transform','rotate('+now+'deg)');
		      },
		      duration: 500
		  },'linear');    	
		$('.edit-toolbar-'+id).css("display", "none");
		$('.toolbar-'+id).css("display", "grid");
		$('.toolbar-'+id).toggleClass("slidedown slideup");
		$('.toolbtn-'+id).toggleClass("down-arrow up-arrow");
	});
});

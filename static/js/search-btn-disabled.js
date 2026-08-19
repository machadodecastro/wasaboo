<!-- Disable search button if text is empty -->
  $(document).ready(function () {
	    $('#autosearch').keyup(function () {
	        if ($.trim($('#autosearch').val()).length < 1) {
	        	$('.search-btn').prop('disabled', true);
	        } else {
	        	$('.search-btn').prop('disabled', false);
	        }
	    });	
  });
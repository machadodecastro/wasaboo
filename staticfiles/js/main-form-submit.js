// AJAX MAIN FORM SUBMIT
$( document ).ready(function() {
	$("#my_form").submit(function(event){		
	    event.preventDefault(); //prevent default action
	    var wasabooref = "{{url}}";   
	    var tip = $(this).data("id"); 
	    var post_url = $(this).attr("action"); //get form action url
	    var request_method = $(this).attr("method"); //get form GET/POST method
	    var form_data = new FormData(this); //Encode form elements for submission
	    var pathcard = window.location.pathname;
	    var parts = pathcard.split("/");
	    var last_part = parts[parts.length-2];
	    
	    $('.btn-cancel').prop('disabled', true);
	    $(':input[type="submit"]').prop('disabled', true);
		$('.close').prop('disabled', true);
	    $(':input[type="submit"]').val('Publishing...');
		$('.dot').animate({"animation-duration":"1.3s"}, 0);
	    
	    $.ajax({
	    	url : post_url,
	        type: request_method,
	        data : form_data,
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
	        	$.getScript( '/static/js/fotorama.js');
				
        		// LOAD HTML
	        	$('#waterfall').html(jQuery(response).find('#waterfall').html());
	        	$('.profile-waterfall').html(jQuery(response).find('.profile-waterfall').html());
	        	
	        	//USER CREATE CARD IF IT DOESNT EXIST IN PLAY CARDS
	        	if (pathcard == "/card/"+last_part+"/") {
	        		location.reload();
	        	}

	        	// CLOSE MODAL
				$('.close').prop('disabled', false);
	        	$('.close').click();
	        	$('body').removeClass('modal-open');
	        	$('.modal-backdrop').remove();
	        	$('.btn-cancel').prop('disabled', false);
	        	$(':input[type="submit"]').prop('disabled', false);
	        	$(':input[type="submit"]').val('Publish');
	        	
	        }
	    });
	});
});
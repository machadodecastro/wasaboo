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
	    $(':input[type="submit"]').val('Publishing...');
	    
	    $.ajax({
	    	url : post_url,
	        type: request_method,
	        data : form_data,
	        dataType : 'html',
	        contentType: false,
	        processData: false,
	        success: function(response) { //on success
	        	//LOAD SCRIPTS
	        	$.getScript( '/static/js/call-scripts.js');
	        	
	        	// LOAD HTML
	        	$('#waterfall').html(jQuery(response).find('#waterfall').html());
	        	$('.profile-waterfall').html(jQuery(response).find('.profile-waterfall').html());
	        	
	        	//USER CREATE CARD IF IT DOESNT EXIST IN PLAY CARDS
	        	if (pathcard == "/card/"+last_part+"/"){
	        		location.reload();
	        	}
	        	// CLOSE MODAL
	        	$('.close').click();
	        	$('body').removeClass('modal-open');
	        	$('.modal-backdrop').remove();
	        	$('.btn-cancel').prop('disabled', false);
	        	$(':input[type="submit"]').prop('disabled', false);
	        	$(':input[type="submit"]').val('Publish');
	        	
	        },
	        complete: function(response){
	        	setTimeout(function(){ 
	        		alert('Card created successfully!').slideDown("slow"); 
	        	}, 0); 
	        	setTimeout(function(){ 
	        		$('#alertBox').slideUp("slow");
	        	}, 2000);
	        	setTimeout(function(){ 
	        		$('#closeBtn').click();
	        	}, 3000);	        		
	        	
	        }
	    });
	});
});
// Seeing who favorited your card
$( document ).ready(function() {	
	$(".favoritings").on('click',function(){
		//event.preventDefault();
    	self = $(this);

    	var wasabooref = $(this).data("url");
    	var tip = $(this).data("id");
    	$.ajax({
	    	   type: "GET", 
	    	   dataType: 'json', 
	    	   data: {tip: tip},
	    	   url: "//"+wasabooref+"/who-favorited/"+tip+"/",
	    	   async: true,
	    	   contentType: "application/json; charset=utf-8",
	    	   success: function (data, textStatus, jqXHR) {
						$('#whoFavorited').on('shown.bs.modal', function() {
							$('.who_favorited').each(function() {

								var newHTML = [];
								for (var i = 0; i < data.who_favorited; i++) {
									if ( data.who_favorited > 0 ) {
										if (data.upload[i] != 0){
								    		newHTML.push('<ul class="list-group"> <a href="http://www.wasaboo.com/profile/'+data.id[i]+'" class="list-group-item"> <span><img src="'+ data.upload[i] +'" class="user"></span> '+ data.name[i] +'</a></ul>');
										} else if ((data.upload[i] == 0) && (data.type[i] == "f")){
											newHTML.push('<ul class="list-group"> <a href="http://www.wasaboo.com/profile/'+data.id[i]+'" class="list-group-item"> <span><img class="user woman"></span> '+ data.name[i] +'</a></ul>');
										} else if ((data.upload[i] == 0) && (data.type[i] == "m")){
											newHTML.push('<ul class="list-group"> <a href="http://www.wasaboo.com/profile/'+data.id[i]+'" class="list-group-item"> <span><img class="user man"></span> '+ data.name[i] +'</a></ul>');
										} else if((data.upload[i] == 0) && (data.type[i] == "c")){
											newHTML.push('<ul class="list-group"> <a href="http://www.wasaboo.com/profile/'+data.id[i]+'" class="list-group-item"> <span><img class="user company"></span> '+ data.name[i] +'</a></ul>');
										}
									}
									else {
										$(this).html('<ul class="list-group list-group-item"><span class="edit-description"> Nobody favorited your tip </span></ul>');
									}
								}	
								newHTML.push('<div class="modal-header mobile-modal-header"><button type="button" class="btn btn-cancel btn-cancel-{{tip.id}}" data-dismiss="modal">Close</button></div>');
								$(this).html(newHTML);		
								
		            		});

						});
						
						$('#whoFavorited').on('hidden.bs.modal', function() {
							$('.who_favorited').each(function() {
								//location.reload();
								$(this).html("");
							});
						});

						
		          
	    		   },
	                error: function(rs, e) {
	                    //alert(rs.responseText);
	                }
	    	   });    	
	});
});
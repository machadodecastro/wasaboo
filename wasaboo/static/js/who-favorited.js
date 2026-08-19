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
	    	   url: "http://"+wasabooref+"/who-favorited/"+tip,
	    	   async: true,
	    	   contentType: "application/json; charset=utf-8",
	    	   success: function (data, textStatus, jqXHR) {
		            if (data.teste == "whofavorited") {
						$('#whoFavorited').on('shown.bs.modal', function() {
							
							$('.who_favorited').each(function() {
		            		//	$(this).html("{% for c in who_favorited %} <ul class='list-group'> <a href='{% url 'exibir' c.id %}' class='list-group-item'> <div class='profile-image'> {% if c.type = 'f' %} {% if c.upload != '0' %} <span><img src='{{c.upload}}' class='user'></span> {% else %} <span class='user woman'></span> {% endif %} {% elif c.type = 'm' %} {% if c.upload != '0' %} <span><img src='{{c.upload}}' class='user'></span> {% else %} <span class='user man'></span> {% endif %} {% elif c.type = 'c' %} {% if c.upload != '0' %} <span><img src='{{c.upload}}' class='user'></span> {% else %} <span class='user company'></span> {% endif %} {% endif %} <div class='following'> {{ c.name }} </div> </div> </a> </ul>{% empty %} <div class='panel panel-default-profile'> <div class='panel-body'> <span class='edit-description'>Nobody favorited your tip</span> </div> </div> {% endfor %}");
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
								
									if ( data.who_favorited > 0 ) {
										$(this).html(newHTML);		
									} else {
										$(this).html('<ul class="list-group"><span class="following"> Nobody favorited your tip </span></ul>');
									}									
								
		            		});

						});
						
						$('#whoFavorited').on('hidden.bs.modal', function() {
							$('.who_favorited').each(function() {
								//location.reload();
								$(this).html("");
							});
						});

						
		            } else {
		            	//alert("Error");
		            }
	    		   },
	                error: function(rs, e) {
	                    //alert(rs.responseText);
	                }
	    	   });    	
	});
});
$( document ).ready(function() {	
	$(".btn-send-msg").on('mousedown',function (){    
    	self = $(this);
    	var wasabooref = $(this).data("url");
    	var tip = $(this).data("id"); 
    	var destino = $(this).data("destino"); 
    	var origem = $(this).data("origem"); 
    	var status = $(this).data("status"); 
    	var corpo = $("#chat-"+tip).val(); 
    	var criacao = $(this).data("criacao"); 
    	$.ajax({
	    	   type: "GET", 
	    	   url: "//"+wasabooref+"/chat/"+tip+"/",
	    	   dataType: 'json',
	    	   data: {tip: tip, destino: destino, origem: origem, status: status, corpo: corpo, criacao: criacao},
	    	   async: true,
	    	   contentType: "application/json; charset=utf-8",
	    	   success: function (data, textStatus, jqXHR) { 
		            if (data.teste == "sent") { 
		            	$("#chat-"+tip).val('');
		            	$(".btn-send-msg-"+tip).prop('disabled', true);
		            	
		            	$(".messages-"+tip).each(function() {
		            	var newHTML = [];
						for (var i = 0; i < data.chat; i++) {
							newHTML.push('<div style="text-align: left;"><span style="color:orange;"><strong>Eu:</strong> </span><span class="chat-font">'+corpo+'</span></div><br/>');
						}	
						$(this).prepend(newHTML);		
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
});
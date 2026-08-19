	L.mapbox.accessToken = 'pk.eyJ1IjoiaWdvcm1jYXN0cm8iLCJhIjoiY2pzY2dvdHd6MDFtODQ5cXVzM3R0ZGJqOSJ9.ZKO35vLhFzfWieQIzDGJ_g';
	var map = L.mapbox.map('mapid', 'mapbox.streets');
	map.locate({setView: true, maxZoom: 18});
    	
	lc = L.control.locate({
	    strings: {
	        title: "Show me where I am!"
	    }
	}).addTo(map);
	
	function onLocationFound(e) {
	        var radius = e.accuracy / 2;
	        L.marker(e.latlng).addTo(map)
	        .openPopup("You are at "+ e.latlng.toString() + " and within " + radius + " meters from this point. <br/> <a data-toggle='modal' data-target='#newTip' class='dropdown-toggle btn-my-tips new-tip'><div class='user new-card'></div> </a>").openPopup()
	        	        
	        L.circle(e.latlng, radius).addTo(map);
	    }
	    map.on('locationfound', onLocationFound);
	    

    function onLocationError(e) {
        alert(e.message);
    }
    map.on('locationerror', onLocationError);

    var popup = L.popup();
	function onMapClick(e) {
	    popup
	        .setLatLng(e.latlng)
	        //.setContent("You clicked the map at " + e.latlng.toString() + '<br/><a data-toggle="modal" data-target="#newTip" class="dropdown-toggle btn-my-tips new-tip"><div class="user-geo new-card"></div> </a>')
	        .setContent('<a data-toggle="modal" data-target="#newTip" class="dropdown-toggle btn-my-tips new-tip"><img class="fire-options"/>New alert</a>')
	        .openOn(map);
	}
	map.on('click', onMapClick);
	
    var myIcon = L.icon({
	    iconUrl: '/static/img/fire.png',
	    iconSize: [24, 26],
	    iconAnchor: [9, 21],
	    popupAnchor: [0, -14]
	});

    
	function getData(){
		if (img.toString() == '') {
			L.marker( [lat.toString(), lng.toString()], {icon: myIcon} )
			.bindPopup( '<a href="http://127.0.0.1:8000/'+ slg + '-'+ idc + '" target="_blank"><div class="map-content">' + cnt + '<div class="title-content">'+ ref +'</div></div></a> <br/> <div class="profile-image"><div class="image-content"><span class="user"><img src="'+ ava +'" class="user" alt="user picture"></span></div> <div class="author-content">'+ nme +'</div></div> <br/><a class="profile-image" href="http://localhost:8000/windy"><img src="/static/img/wind.png"> See atmosphere conditions</a> <br/>')
			.addTo( map );
		} else {
			L.marker( [lat.toString(), lng.toString()], {icon: myIcon} )
			.bindPopup( '<br/><a href="http://127.0.0.1:8000/'+ slg + '-'+ idc + '" target="_blank"><img style="width:100%" src="/media/'+img+'"/></a> <br/><br/> <a href="http://127.0.0.1:8000/'+ slg + '-'+ idc + '" target="_blank"><div class="map-content">' + cnt + '<div class="title-content">'+ ref +'</div></div></a> <br/> <div class="profile-image"><div class="image-content"><span class="user"><img src="'+ ava +'" class="user" alt="user picture"></span></div><div class="author-content">'+ nme +'</div></div> <br/><a class="profile-image" href="http://localhost:8000/windy"><img src="/static/img/wind.png"> See atmosphere conditions</a> <br/>')
			.addTo( map );				
		}
	}
	map.on('locationfound', getData);
	
    
	$( document ).ready(function() {
		$(".cards").each(function() {
		var self = $(this);
		var wasabooref = $(this).data("url"); 
		var idTip = $(this).data("id");
	       $.ajax({
	    	   type: "GET", 
	    	   dataType: 'json', 
	    	   data: {tip: idTip},
	    	   url: "//"+wasabooref+"/mapping/"+idTip+"/",
	    	   async: false,
	    	   contentType: "application/json; charset=utf-8",
	    	   success: function (data, textStatus, jqXHR) {
	    		   if (data.teste == "yes") {
	    			 $('.card-'+idTip).each(function() {	    			  
	    		
   				    	getData(lat=data.lat[i], lng=data.lng[i], cnt=data.cnt[i],
   				    			slg=data.slg[i], idc=data.idc[i], img=data.img[i],
   				    			ava=data.ava[i], nme=data.nme[i], ref=data.ref[i]);
   				    	   				
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
	
	
	$( document ).ready(function() {
		map.on('click', function(e) { 
	    	$(".lat").val(e.latlng.lat);
	    	$(".lng").val(e.latlng.lng);
		});		
	});

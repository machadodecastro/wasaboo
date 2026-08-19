const options = {
    // Required: API key
    key: 'YYKUkKkQbn6rvga9tVzlM8GCCJnvnVZ7', // REPLACE WITH YOUR KEY !!!

    // Put additional console output
    verbose: true,

    // Optional: Initial state of the map
    lat: 50.4,
    lon: 14.3,
    zoom: 5,
};

// Initialize Windy API
windyInit(options, windyAPI => {
    // windyAPI is ready, and contain 'map', 'store',
    // 'picker' and other usefull stuff
	
    const { map } = windyAPI;
    // .map is instance of Leaflet map  
    
    map.locate({setView: true, maxZoom: 18});
    
    var popup = L.popup();
	function onMapClick(e) {
	    popup
	        .setLatLng(e.latlng)
	        //.setContent("You clicked the map at " + e.latlng.toString() + '<br/><a data-toggle="modal" data-target="#newTip" class="dropdown-toggle btn-my-tips new-tip"><div class="user-geo new-card"></div> </a>')
	        .setContent('<a class="title-content" href="http://localhost:8000/feed"><img src="/static/img/street-view.png"> Back to Street View</a>')
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
			.bindPopup( '<a href="http://localhost:8000/'+ slg + '-'+ idc + '" target="_blank"><div class="map-content">' + cnt + '<div class="title-content">'+ ref +'</div></div></a> <br/> <div class="profile-image"><div class="image-content"><span class="user"><img src="'+ ava +'" class="user" alt="user picture"></span></div> <div class="author-content">'+ nme +'</div></div> <br/><a class="profile-image" href="http://localhost:8000/feed"><img src="/static/img/street-view.png"> Back to Street View</a><br/>')
			.addTo( map );
		} else {
			L.marker( [lat.toString(), lng.toString()], {icon: myIcon} )
			.bindPopup( '<br/><a href="http://localhost:8000/'+ slg + '-'+ idc + '" target="_blank"><img style="width:100%" src="/media/'+img+'"/></a> <br/><br/> <a href="http://127.0.0.1:8000/'+ slg + '-'+ idc + '" target="_blank"><div class="map-content">' + cnt + '<div class="title-content">'+ ref +'</div></div></a> <br/> <div class="profile-image"><div class="image-content"><span class="user"><img src="'+ ava +'" class="user" alt="user picture"></span></div><div class="author-content">'+ nme +'</div></div> <br/><a class="profile-image" href="http://localhost:8000/feed"><img src="/static/img/street-view.png"> Back to Street View</a><br/> ')
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
    
});

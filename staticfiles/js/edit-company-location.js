/* Company location */
$( document ).ready(function() {
	"use strict";
	var edit_geocoder;
	var edit_map;
	
	// setup initial map
	function initialize() {
		edit_geocoder = new google.maps.Geocoder();							// create geocoder object
		var edit_latlng = new google.maps.LatLng(40.6700, -73.9400);			// set default lat/long (new york city)
		var edit_mapOptions = {												// options for map
			zoom: 8,
			center: edit_latlng
		}
		edit_map = new google.maps.Map(document.getElementById('edit-map-canvas'), edit_mapOptions);	// create new map in the map-canvas div
	}
	
	// function to geocode an address and plot it on a map
	function codeAddress(address) {
		edit_geocoder.geocode( { 'address': address}, function(results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				edit_map.setCenter(results[0].geometry.location);			// center the map on address
				var marker = new google.maps.Marker({					// place a marker on the map at the address
					map: edit_map,
					position: results[0].geometry.location
				});
			} else {
				alert('Geocode was not successful for the following reason: ' + status);
			}
		});
	}
	google.maps.event.addDomListener(window, 'load', initialize);		// setup initial map
	$(document).ready(function() {
		// get map button functionality
		$("#edit-get-map-btn").click(function(event){
			event.preventDefault();			
			var edit_address = $("#edit_address").val();							// grab the address from the input field
			codeAddress(edit_address);										// geocode the address
		});
	});
	
	$('#updateLocation').on('shown.bs.modal', function() {
		edit_geocoder = new google.maps.Geocoder();							// create geocoder object
		var edit_latlng = new google.maps.LatLng(40.6700, -73.9400);			// set default lat/long (new york city)
		var edit_mapOptions = {												// options for map
			zoom: 8,
			center: edit_latlng
		}
		edit_map = new google.maps.Map(document.getElementById('edit-map-canvas'), edit_mapOptions);	// create new map in the map-canvas div
	});
	
});
	        		  // Return the first few bytes of the file as a hex string
	    			  function getBLOBFileHeader(url, blob, callback) {
	    			    var fileReader = new FileReader();
	    			    fileReader.onloadend = function(e) {
	    			      var arr = (new Uint8Array(e.target.result)).subarray(0, 4);
	    			      var header = "";
	    			      for (var i = 0; i < arr.length; i++) {
	    			        header += arr[i].toString(16);
	    			      }
	    			      callback(url, header);
	    			    };
	    			    fileReader.readAsArrayBuffer(blob);
	    			  }
	
	    			  function getRemoteFileHeader(url, callback) {
	    			    var xhr = new XMLHttpRequest();
	    			    // Bypass CORS for this demo - naughty, Drakes
	    			    xhr.open('GET', '//cors-anywhere.herokuapp.com/' + url);
	    			    xhr.responseType = "blob";
	    			    xhr.onload = function() {
	    			      callback(url, xhr.response);
	    			    };
	    			    xhr.onerror = function() {
	    			      alert('A network error occurred!');
	    			    };
	    			    xhr.send();
	    			  }
	
	    			  function headerCallback(url, headerString) {
	    			    printHeaderInfo(url, headerString);
	    			  }
	
	    			  function remoteCallback(url, blob) {
	    			    printImage(blob);
	    			    getBLOBFileHeader(url, blob, headerCallback);
	    			  }
	
	    			  function printImage(blob) {
	    			    // Add this image to the document body for proof of GET success
	    			    var fr = new FileReader();
	    			    fr.onloadend = function() {
	    			    	$("#edit_imgPreview").show(); 
	    			    	$("#edit_imgPreview").attr("src", fr.result).css('width', '200');
	    			    	//$(".fr-image-upload-layer").append($("<img>").attr("src", fr.result).css('width', '300'))
	    			        //.after($("<div>").text("Blob MIME type: " + blob.type));
	   			    	
	    			    };
	    			    fr.readAsDataURL(blob);
	    			  }
	
	    			  // Add more from http://en.wikipedia.org/wiki/List_of_file_signatures
	    			  function mimeType(headerString) {
	    			    switch (headerString) {
	    			      case "89504e47":
	    			        type = "image/png";
	    			        $("#edit_imgPreview").show();
	    			        $(".upload-drop-image").hide();
	    			        $(".uploaded-preview-image").hide();	    			        
	    			        $("#edit_rmImg").show();
	    			        $("#edit_rotateImg").show();
	    			        $("#edit_desrotateImg").show();
	    			        $("#edit_warningNotImage").hide();
	    			        $("#edit_warningClickUpload").hide();
	    			        break;
	    			      case "47494638":
	    			        type = "image/gif";
	    			        $("#edit_imgPreview").show();
	    			        $(".upload-drop-image").hide();
	    			        $(".uploaded-preview-image").hide();
	    			        $("#edit_rmImg").show();
	    			        $("#edit_rotateImg").show();
	    			        $("#edit_desrotateImg").show();
	    			        $("#edit_warningNotImage").hide();
	    			        $("#edit_warningClickUpload").hide();
	    			        break;
	    			      case "ffd8ffe0":
	    			      case "ffd8ffe1":
	    			      case "ffd8ffe2":
	    			        type = "image/jpeg";
	    			        $("#edit_imgPreview").show();
	    			        $(".upload-drop-image").hide();
	    			        $(".uploaded-preview-image").hide();
	    			        $("#edit_rmImg").show();
	    			        $("#edit_rotateImg").show();
	    			        $("#edit_desrotateImg").show();
	    			        $("#edit_warningNotImage").hide();
	    			        $("#edit_warningClickUpload").hide();
	    			        break;
	    			      default:
	    			        type = "unknown";    			        
	    			        $("#edit_imgPreview").hide();
	    			        $(".upload-drop-image").show();
	    			        $(".uploaded-preview-image").show();
	    			        $("#edit_rmImg").hide();
	    			        $("#edit_rotateImg").hide();
	    			        $("#edit_desrotateImg").hide();
	    			        $("#edit_file").val("");
	    			        //alert("File is not an image");
	    			        $("#edit_warningClickUpload").hide();
	    			        $("#edit_warningNotImage").remove();
	    			        $('<span id="edit_warningNotImage" class="title-tip">File is not an image</span>').appendTo('.fr-image-upload-layer');
	    			        break;
	    			    }
	    			    return type;
	    			  }
	
	    			  function printHeaderInfo(url, headerString) {
	    			    $("hr").after($("#edit_imgInfo").text("Real MIME type: " + mimeType(headerString)))
	    			      .after($("#edit_imgInfo").text("File header: 0x" + headerString))
	    			      .after($("#edit_imgInfo").text(url));
	    			  }
	
	    			  /* Demo driver code */
	 				  
	    			  var imageURLsArray = [];
	    			 
	    			  // Check for FileReader support
	    			  if (window.FileReader && window.Blob) {
	    			    // Load all the remote images from the urls array
	    			    for (var i = 0; i < imageURLsArray.length; i++) {
	    			      getRemoteFileHeader(imageURLsArray[i], remoteCallback);
	    			    }
	
	    			    /* Handle local files */
	    			    $("#edit_file").on('change', function(event) {
	    			      var file = event.target.files[0];
	    			      if (file.size >= 4 * 1024 * 1024) {
	    			        //alert("File size must be at most 4MB");
	    			        $("#edit_imgPreview").hide();
	    			        $("#edit_rmImg").hide();
	    			        $(".upload-drop-image").show();
	    			        $(".uploaded-preview-image").show();
	    			        $("#edit_file").val("");
	    			        $("#edit_warningClickUpload").hide();
	    			        $("#edit_warningNotImage").hide();
	    			        $("#edit_warningNotImage").remove();
	    			        $('<span id="edit_warningNotImage" class="title-tip">File size must be at most 4MB</span>').appendTo('.fr-image-upload-layer');
	    			        return;
	    			      }
	    			      remoteCallback(escape(file.name), file);
	    			    });
	
	    			  } else {
	    			    // File and Blob are not supported
	    			    $("hr").after( $("<div>").text("It seems your browser doesn't support FileReader") );
	    			  } /* Drakes, 2015 */
	    			  
	    			  $("#edit_rmImg").on('click', function(event) { 
	    				  $("#edit_file").val("");
	    				  $("#edit_imgPreview").hide();
	    				  $(".upload-drop-image").show();
	    				  $(".uploaded-preview-image").show();
	    				  $(this).hide();
	    				  $("#edit_rotateImg").hide();
	  			          $("#edit_desrotateImg").hide();
	  			          $("#edit_warningClickUpload").show();
	    			  });

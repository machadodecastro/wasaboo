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
	    			    	$("#imgPreview").show(); 
	    			    	$("#imgPreview").attr("src", fr.result).css('width', '200');
	    			    	$(':input[type="submit"]').prop('disabled', false);
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
	    			        $("#imgPreview").show();
	    			        $(".upload-drop-image").hide();
	    			        $(".uploaded-preview-image").hide();	    			        
	    			        $("#rmImg").show();
	    			        $("#rotateImg").show();
	    			        $("#desrotateImg").show();
	    			        $(".warning").hide();
	    			        $("#warningClickUpload").hide();
	    			        break;
	    			      case "47494638":
	    			        type = "image/gif";
	    			        $("#imgPreview").show();
	    			        $(".upload-drop-image").hide();
	    			        $(".uploaded-preview-image").hide();
	    			        $("#rmImg").show();
	    			        $("#rotateImg").show();
	    			        $("#desrotateImg").show();
	    			        $(".warning").hide();
	    			        $("#warningClickUpload").hide();
	    			        break;
	    			      case "ffd8ffe0":
	    			      case "ffd8ffe1":
	    			      case "ffd8ffe2":
	    			        type = "image/jpeg";
	    			        $("#imgPreview").show();
	    			        $(".upload-drop-image").hide();
	    			        $(".uploaded-preview-image").hide();
	    			        $("#rmImg").show();
	    			        $("#rotateImg").show();
	    			        $("#desrotateImg").show();
	    			        $(".warning").hide();
	    			        $("#warningClickUpload").hide();
	    			        break;
	    			      default:
	    			        type = "unknown";    			        
	    			        $("#imgPreview").hide();
	    			        $(".upload-drop-image").show();
	    			        $(".uploaded-preview-image").show();
	    			        $("#rmImg").hide();
	    			        $("#rotateImg").hide();
	    			        $("#desrotateImg").hide();
	    			        $("#file").val("");
	    			        //alert("File is not an image");
	    			        $("#warningClickUpload").hide();
	    			        $('.warning').remove();
	    			        var newParagraph = document.createElement("p");
	    			        newParagraph.innerHTML = "<span class='warning title-tip'>File is not an image</span>";
	    			        $(".upload-area").append(newParagraph);
	    			        //$("#warningNotImage").remove();
	    			        //$('<span id="warningNotImage" class="title-tip">File is not an image</span>').append('.fr-image-upload-layer');
	    			        break;
	    			    }
	    			    return type;
	    			  }
	
	    			  function printHeaderInfo(url, headerString) {
	    			    $("hr").after($("#imgInfo").text("Real MIME type: " + mimeType(headerString)))
	    			      .after($("#imgInfo").text("File header: 0x" + headerString))
	    			      .after($("#imgInfo").text(url));
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
	    			    $("#file").on('change', function(event) {
	    			      var file = event.target.files[0];
	    			      if (file.size >= 4 * 1024 * 1024) {
	    			        //alert("File size must be at most 4MB");
	    			        $("#imgPreview").hide();
	    			        $("#rmImg").hide();
	    			        $(".upload-drop-image").show();
	    			        $(".uploaded-preview-image").show();
	    			        $("#file").val("");
	    			        $("#warningClickUpload").hide();
	    			        $('.warning').remove();
	    			        var newParagraph = document.createElement("p");
	    			        newParagraph.innerHTML = "<span class='warning title-tip'>File size must be at most 4MB</span>";
	    			        $(".upload-area").append(newParagraph);
	    			        //$("#warningNotImage").hide();
	    			        //$("#warningNotImage").remove();
	    			        //$('<span id="warningNotImage" class="title-tip">File size must be at most 4MB</span>').appendTo('.fr-image-upload-layer');
	    			        return;
	    			      }
	    			      remoteCallback(escape(file.name), file);
	    			    });
	
	    			  } else {
	    			    // File and Blob are not supported
	    			    $("hr").after( $("<div>").text("It seems your browser doesn't support FileReader") );
	    			  } /* Drakes, 2015 */
	    			  
	    			  $("#rmImg").on('click', function(event) { 
	    				  $("#file").val("");
	    				  $("#imgPreview").hide();
	    				  $(".upload-drop-image").show();
	    				  $(".uploaded-preview-image").show();
	    				  $(this).hide();
	    				  $("#rotateImg").hide();
	  			          $("#desrotateImg").hide();
	  			          $("#warningClickUpload").show();
	  			          if ($.trim($('#content').val()).length < 1) {
	  			        	  $(':input[type="submit"]').prop('disabled', true);
	  			          }
	    			  });
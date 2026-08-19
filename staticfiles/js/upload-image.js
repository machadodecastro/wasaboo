					  //Outdoor 1
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
	    			  
	    			//Outdoor 2
	    			  function getBLOBFileHeader2(url, blob, callback) {
	    			    var fileReader2 = new FileReader();
	    			    fileReader2.onloadend = function(e) {
	    			      var arr = (new Uint8Array(e.target.result)).subarray(0, 4);
	    			      var header = "";
	    			      for (var i = 0; i < arr.length; i++) {
	    			        header += arr[i].toString(16);
	    			      }
	    			      callback(url, header);
	    			    };
	    			    fileReader2.readAsArrayBuffer(blob);
	    			  }
	    			  
	    			//Outdoor 3
	    			  function getBLOBFileHeader3(url, blob, callback) {
	    			    var fileReader3 = new FileReader();
	    			    fileReader3.onloadend = function(e) {
	    			      var arr = (new Uint8Array(e.target.result)).subarray(0, 4);
	    			      var header = "";
	    			      for (var i = 0; i < arr.length; i++) {
	    			        header += arr[i].toString(16);
	    			      }
	    			      callback(url, header);
	    			    };
	    			    fileReader3.readAsArrayBuffer(blob);
	    			  }
	    			  
	    			//Outdoor 4
	    			  function getBLOBFileHeader4(url, blob, callback) {
	    			    var fileReader4 = new FileReader();
	    			    fileReader4.onloadend = function(e) {
	    			      var arr = (new Uint8Array(e.target.result)).subarray(0, 4);
	    			      var header = "";
	    			      for (var i = 0; i < arr.length; i++) {
	    			        header += arr[i].toString(16);
	    			      }
	    			      callback(url, header);
	    			    };
	    			    fileReader4.readAsArrayBuffer(blob);
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
	    			  
	    			  //Outdoor 1
	    			  function headerCallback(url, headerString) {
	    			    printHeaderInfo(url, headerString);
	    			  }
	    			  
	    			  //Outdoor 2
	    			  function headerCallback2(url, headerString) {
		    		    printHeaderInfo2(url, headerString);
		    		  }
	    			  
	    			  //Outdoor 3
	    			  function headerCallback3(url, headerString) {
		    		    printHeaderInfo3(url, headerString);
		    		  }
	    			  
	    			  //Outdoor 4
	    			  function headerCallback4(url, headerString) {
		    		    printHeaderInfo4(url, headerString);
		    		  }
	
	    			  //Outdoor 1
	    			  function remoteCallback(url, blob) {
	    			    printImage(blob);
	    			    getBLOBFileHeader(url, blob, headerCallback);
	    			  }
	    			  
	    			  //Outdoor 2
	    			  function remoteCallback2(url, blob) {
	    			    printImage2(blob);
	    			    getBLOBFileHeader2(url, blob, headerCallback2);
	    			  }
	    			  
	    			  //Outdoor 3
	    			  function remoteCallback3(url, blob) {
	    			    printImage3(blob);
	    			    getBLOBFileHeader3(url, blob, headerCallback3);
	    			  }
	    			  
	    			  //Outdoor 4
	    			  function remoteCallback4(url, blob) {
	    			    printImage4(blob);
	    			    getBLOBFileHeader4(url, blob, headerCallback4);
	    			  }
	
	    			  //Outdoor 1
	    			  function printImage(blob) {
	    			    // Add this image to the document body for proof of GET success
	    			    var fr = new FileReader();
	    			    fr.onloadend = function() {
	    			    	$("#imgPreview").show(); 
	    			    	$("#imgPreview").attr("src", fr.result).css('width', '100');
	    			    	$(':input[type="submit"]').prop('disabled', false);
	    			    	//$(".fr-image-upload-layer").append($("<img>").attr("src", fr.result).css('width', '300'))
	    			        //.after($("<div>").text("Blob MIME type: " + blob.type));
	    			    };
	    			    fr.readAsDataURL(blob);
	    			  }
	    			  
	    			  //Outdoor 2
	    			  function printImage2(blob) {
	    			    // Add this image to the document body for proof of GET success
	    			    var fr2 = new FileReader();
	    			    fr2.onloadend = function() {
	    			    	$("#imgPreview2").show(); 
	    			    	$("#imgPreview2").attr("src", fr2.result).css('width', '100');
	    			    	$(':input[type="submit"]').prop('disabled', false);
	    			    	//$(".fr-image-upload-layer").append($("<img>").attr("src", fr.result).css('width', '300'))
	    			        //.after($("<div>").text("Blob MIME type: " + blob.type));
	    			    };
	    			    fr2.readAsDataURL(blob);
	    			  }
	    			  
	    			  //Outdoor 3
	    			  function printImage3(blob) {
	    			    // Add this image to the document body for proof of GET success
	    			    var fr3 = new FileReader();
	    			    fr3.onloadend = function() {
	    			    	$("#imgPreview3").show(); 
	    			    	$("#imgPreview3").attr("src", fr3.result).css('width', '100');
	    			    	$(':input[type="submit"]').prop('disabled', false);
	    			    	//$(".fr-image-upload-layer").append($("<img>").attr("src", fr.result).css('width', '300'))
	    			        //.after($("<div>").text("Blob MIME type: " + blob.type));
	    			    };
	    			    fr3.readAsDataURL(blob);
	    			  }	 
	    			  
	    			  //Outdoor 4
	    			  function printImage4(blob) {
	    			    // Add this image to the document body for proof of GET success
	    			    var fr4 = new FileReader();
	    			    fr4.onloadend = function() {
	    			    	$("#imgPreview4").show(); 
	    			    	$("#imgPreview4").attr("src", fr4.result).css('width', '100');
	    			    	$(':input[type="submit"]').prop('disabled', false);
	    			    	//$(".fr-image-upload-layer").append($("<img>").attr("src", fr.result).css('width', '300'))
	    			        //.after($("<div>").text("Blob MIME type: " + blob.type));
	    			    };
	    			    fr4.readAsDataURL(blob);
	    			  }		    			  
	
	    			  //Outdoor 1
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
	    			  
	    			  
	    			  //Outdoor 2
	    			  function mimeType2(headerString) {
		    			    switch (headerString) {
		    			      case "89504e47":
		    			        type = "image/png";
		    			        $("#imgPreview2").show();
		    			        $(".upload-drop-image2").hide();
		    			        $(".uploaded-preview-image2").hide();	    			        
		    			        $("#rmImg2").show();
		    			        $("#rotateImg2").show();
		    			        $("#desrotateImg2").show();
		    			        $(".warning2").hide();
		    			        $("#warningClickUpload2").hide();
		    			        break;
		    			      case "47494638":
		    			        type = "image/gif";
		    			        $("#imgPreview2").show();
		    			        $(".upload-drop-image2").hide();
		    			        $(".uploaded-preview-image2").hide();
		    			        $("#rmImg2").show();
		    			        $("#rotateImg2").show();
		    			        $("#desrotateImg2").show();
		    			        $(".warning2").hide();
		    			        $("#warningClickUpload2").hide();
		    			        break;
		    			      case "ffd8ffe0":
		    			      case "ffd8ffe1":
		    			      case "ffd8ffe2":
		    			        type = "image/jpeg";
		    			        $("#imgPreview2").show();
		    			        $(".upload-drop-image2").hide();
		    			        $(".uploaded-preview-image2").hide();
		    			        $("#rmImg2").show();
		    			        $("#rotateImg2").show();
		    			        $("#desrotateImg2").show();
		    			        $(".warning2").hide();
		    			        $("#warningClickUpload2").hide();
		    			        break;
		    			      default:
		    			        type = "unknown";    			        
		    			        $("#imgPreview2").hide();
		    			        $(".upload-drop-image2").show();
		    			        $(".uploaded-preview-image2").show();
		    			        $("#rmImg2").hide();
		    			        $("#rotateImg2").hide();
		    			        $("#desrotateImg2").hide();
		    			        $("#file2").val("");
		    			        //alert("File is not an image");
		    			        $("#warningClickUpload2").hide();
		    			        $('.warning2').remove();
		    			        var newParagraph = document.createElement("p");
		    			        newParagraph.innerHTML = "<span class='warning title-tip'>File is not an image</span>";
		    			        $(".upload-area2").append(newParagraph);
		    			        //$("#warningNotImage").remove();
		    			        //$('<span id="warningNotImage" class="title-tip">File is not an image</span>').append('.fr-image-upload-layer');
		    			        break;
		    			    }
		    			    return type;
		    			  }
	    			  
	    			  //Outdoor 3
	    			  function mimeType3(headerString) {
		    			    switch (headerString) {
		    			      case "89504e47":
		    			        type = "image/png";
		    			        $("#imgPreview3").show();
		    			        $(".upload-drop-image3").hide();
		    			        $(".uploaded-preview-image3").hide();	    			        
		    			        $("#rmImg3").show();
		    			        $("#rotateImg3").show();
		    			        $("#desrotateImg3").show();
		    			        $(".warning3").hide();
		    			        $("#warningClickUpload3").hide();
		    			        break;
		    			      case "47494638":
		    			        type = "image/gif";
		    			        $("#imgPreview3").show();
		    			        $(".upload-drop-image3").hide();
		    			        $(".uploaded-preview-image3").hide();
		    			        $("#rmImg3").show();
		    			        $("#rotateImg3").show();
		    			        $("#desrotateImg3").show();
		    			        $(".warning3").hide();
		    			        $("#warningClickUpload3").hide();
		    			        break;
		    			      case "ffd8ffe0":
		    			      case "ffd8ffe1":
		    			      case "ffd8ffe2":
		    			        type = "image/jpeg";
		    			        $("#imgPreview3").show();
		    			        $(".upload-drop-image3").hide();
		    			        $(".uploaded-preview-image3").hide();
		    			        $("#rmImg3").show();
		    			        $("#rotateImg3").show();
		    			        $("#desrotateImg3").show();
		    			        $(".warning3").hide();
		    			        $("#warningClickUpload3").hide();
		    			        break;
		    			      default:
		    			        type = "unknown";    			        
		    			        $("#imgPreview3").hide();
		    			        $(".upload-drop-image3").show();
		    			        $(".uploaded-preview-image3").show();
		    			        $("#rmImg3").hide();
		    			        $("#rotateImg3").hide();
		    			        $("#desrotateImg3").hide();
		    			        $("#file3").val("");
		    			        //alert("File is not an image");
		    			        $("#warningClickUpload3").hide();
		    			        $('.warning3').remove();
		    			        var newParagraph = document.createElement("p");
		    			        newParagraph.innerHTML = "<span class='warning title-tip'>File is not an image</span>";
		    			        $(".upload-area3").append(newParagraph);
		    			        //$("#warningNotImage").remove();
		    			        //$('<span id="warningNotImage" class="title-tip">File is not an image</span>').append('.fr-image-upload-layer');
		    			        break;
		    			    }
		    			    return type;
		    			  }	    
	    			  
	    			  
	    			  //Outdoor 4
	    			  function mimeType4(headerString) {
		    			    switch (headerString) {
		    			      case "89504e47":
		    			        type = "image/png";
		    			        $("#imgPreview4").show();
		    			        $(".upload-drop-image4").hide();
		    			        $(".uploaded-preview-image4").hide();	    			        
		    			        $("#rmImg4").show();
		    			        $("#rotateImg4").show();
		    			        $("#desrotateImg4").show();
		    			        $(".warning4").hide();
		    			        $("#warningClickUpload4").hide();
		    			        break;
		    			      case "47494638":
		    			        type = "image/gif";
		    			        $("#imgPreview4").show();
		    			        $(".upload-drop-image4").hide();
		    			        $(".uploaded-preview-image4").hide();
		    			        $("#rmImg4").show();
		    			        $("#rotateImg4").show();
		    			        $("#desrotateImg4").show();
		    			        $(".warning4").hide();
		    			        $("#warningClickUpload4").hide();
		    			        break;
		    			      case "ffd8ffe0":
		    			      case "ffd8ffe1":
		    			      case "ffd8ffe2":
		    			        type = "image/jpeg";
		    			        $("#imgPreview4").show();
		    			        $(".upload-drop-image4").hide();
		    			        $(".uploaded-preview-image4").hide();
		    			        $("#rmImg4").show();
		    			        $("#rotateImg4").show();
		    			        $("#desrotateImg4").show();
		    			        $(".warning4").hide();
		    			        $("#warningClickUpload4").hide();
		    			        break;
		    			      default:
		    			        type = "unknown";    			        
		    			        $("#imgPreview4").hide();
		    			        $(".upload-drop-image4").show();
		    			        $(".uploaded-preview-image4").show();
		    			        $("#rmImg4").hide();
		    			        $("#rotateImg4").hide();
		    			        $("#desrotateImg4").hide();
		    			        $("#file4").val("");
		    			        //alert("File is not an image");
		    			        $("#warningClickUpload4").hide();
		    			        $('.warning4').remove();
		    			        var newParagraph = document.createElement("p");
		    			        newParagraph.innerHTML = "<span class='warning title-tip'>File is not an image</span>";
		    			        $(".upload-area4").append(newParagraph);
		    			        //$("#warningNotImage").remove();
		    			        //$('<span id="warningNotImage" class="title-tip">File is not an image</span>').append('.fr-image-upload-layer');
		    			        break;
		    			    }
		    			    return type;
		    			  }	    			  
	    			  
	    			  //Outdoor 1
	    			  function printHeaderInfo(url, headerString) {
	    			    $("hr").after($("#imgInfo").text("Real MIME type: " + mimeType(headerString)))
	    			      .after($("#imgInfo").text("File header: 0x" + headerString))
	    			      .after($("#imgInfo").text(url));
	    			  }
	    			  
	    			  //Outdoor 2
	    			  function printHeaderInfo2(url, headerString) {
	    			    $("hr").after($("#imgInfo2").text("Real MIME type: " + mimeType2(headerString)))
	    			      .after($("#imgInfo2").text("File header: 0x" + headerString))
	    			      .after($("#imgInfo2").text(url));
	    			  }
	    			  
	    			  //Outdoor 3
	    			  function printHeaderInfo3(url, headerString) {
	    			    $("hr").after($("#imgInfo3").text("Real MIME type: " + mimeType3(headerString)))
	    			      .after($("#imgInfo3").text("File header: 0x" + headerString))
	    			      .after($("#imgInfo3").text(url));
	    			  }	
	    			  
	    			  //Outdoor 4
	    			  function printHeaderInfo4(url, headerString) {
	    			    $("hr").after($("#imgInfo4").text("Real MIME type: " + mimeType4(headerString)))
	    			      .after($("#imgInfo4").text("File header: 0x" + headerString))
	    			      .after($("#imgInfo4").text(url));
	    			  }	    			  
	
	 				  
	    			  var imageURLsArray = [];
	    			  var imageURLsArray2 = [];
	    			  var imageURLsArray3 = [];
	    			  var imageURLsArray4 = [];
	    			 
	    			  //Outdoor 1
	    			  // Check for FileReader support
	    			  if (window.FileReader && window.Blob) {
	    			    // Load all the remote images from the urls array
	    			    for (var i = 0; i < imageURLsArray.length; i++) {
	    			      getRemoteFileHeader(imageURLsArray[i], remoteCallback);
	    			    }
	
	    			    /* Outdoor 1 */
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
	    			  
	    			  
	    			//Outdoor 2
	    			  // Check for FileReader support
	    			  if (window.FileReader && window.Blob) {
	    			    // Load all the remote images from the urls array
	    			    for (var i = 0; i < imageURLsArray2.length; i++) {
	    			      getRemoteFileHeader2(imageURLsArray2[i], remoteCallback2);
	    			    }
	
	    			    /* Outdoor 2 */
	    			    $("#file2").on('change', function(event) {
	    			      var file2 = event.target.files[0];
	    			      if (file2.size >= 4 * 1024 * 1024) {
	    			        //alert("File size must be at most 4MB");
	    			        $("#imgPreview2").hide();
	    			        $("#rmImg2").hide();
	    			        $(".upload-drop-image2").show();
	    			        $(".uploaded-preview-image2").show();
	    			        $("#file2").val("");
	    			        $("#warningClickUpload2").hide();
	    			        $('.warning2').remove();
	    			        var newParagraph = document.createElement("p");
	    			        newParagraph.innerHTML = "<span class='warning title-tip'>File size must be at most 4MB</span>";
	    			        $(".upload-area2").append(newParagraph);
	    			        //$("#warningNotImage").hide();
	    			        //$("#warningNotImage").remove();
	    			        //$('<span id="warningNotImage" class="title-tip">File size must be at most 4MB</span>').appendTo('.fr-image-upload-layer');
	    			        return;
	    			      }
	    			      remoteCallback2(escape(file2.name), file2);
	    			    });
	    			  } else {
	    			    // File and Blob are not supported
	    			    $("hr").after( $("<div>").text("It seems your browser doesn't support FileReader") );
	    			  } /* Drakes, 2015 */
	    			  
	    			  
		    			//Outdoor 3
	    			  // Check for FileReader support
	    			  if (window.FileReader && window.Blob) {
	    			    // Load all the remote images from the urls array
	    			    for (var i = 0; i < imageURLsArray3.length; i++) {
	    			      getRemoteFileHeader3(imageURLsArray3[i], remoteCallback3);
	    			    }
	
	    			    /* Outdoor 3 */
	    			    $("#file3").on('change', function(event) {
	    			      var file3 = event.target.files[0];
	    			      if (file3.size >= 4 * 1024 * 1024) {
	    			        //alert("File size must be at most 4MB");
	    			        $("#imgPreview3").hide();
	    			        $("#rmImg3").hide();
	    			        $(".upload-drop-image3").show();
	    			        $(".uploaded-preview-image3").show();
	    			        $("#file3").val("");
	    			        $("#warningClickUpload3").hide();
	    			        $('.warning3').remove();
	    			        var newParagraph = document.createElement("p");
	    			        newParagraph.innerHTML = "<span class='warning title-tip'>File size must be at most 4MB</span>";
	    			        $(".upload-area3").append(newParagraph);
	    			        //$("#warningNotImage").hide();
	    			        //$("#warningNotImage").remove();
	    			        //$('<span id="warningNotImage" class="title-tip">File size must be at most 4MB</span>').appendTo('.fr-image-upload-layer');
	    			        return;
	    			      }
	    			      remoteCallback3(escape(file3.name), file3);
	    			    });
	    			  } else {
	    			    // File and Blob are not supported
	    			    $("hr").after( $("<div>").text("It seems your browser doesn't support FileReader") );
	    			  } /* Drakes, 2015 */	    			  
	    			  
	    			  
		    		  //Outdoor 4
	    			  // Check for FileReader support
	    			  if (window.FileReader && window.Blob) {
	    			    // Load all the remote images from the urls array
	    			    for (var i = 0; i < imageURLsArray4.length; i++) {
	    			      getRemoteFileHeader4(imageURLsArray4[i], remoteCallback4);
	    			    }
	
	    			    /* Outdoor 4 */
	    			    $("#file4").on('change', function(event) {
	    			      var file4 = event.target.files[0];
	    			      if (file4.size >= 4 * 1024 * 1024) {
	    			        //alert("File size must be at most 4MB");
	    			        $("#imgPreview4").hide();
	    			        $("#rmImg4").hide();
	    			        $(".upload-drop-image4").show();
	    			        $(".uploaded-preview-image4").show();
	    			        $("#file4").val("");
	    			        $("#warningClickUpload4").hide();
	    			        $('.warning4').remove();
	    			        var newParagraph = document.createElement("p");
	    			        newParagraph.innerHTML = "<span class='warning title-tip'>File size must be at most 4MB</span>";
	    			        $(".upload-area4").append(newParagraph);
	    			        //$("#warningNotImage").hide();
	    			        //$("#warningNotImage").remove();
	    			        //$('<span id="warningNotImage" class="title-tip">File size must be at most 4MB</span>').appendTo('.fr-image-upload-layer');
	    			        return;
	    			      }
	    			      remoteCallback4(escape(file4.name), file4);
	    			    });
	    			  } else {
	    			    // File and Blob are not supported
	    			    $("hr").after( $("<div>").text("It seems your browser doesn't support FileReader") );
	    			  } /* Drakes, 2015 */
	    			  
	    			  
	    			  //Outdoor 1
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
	    			  
	    			  //Outdoor 2
	    			  $("#rmImg2").on('click', function(event) { 
	    				  $("#file2").val("");
	    				  $("#imgPreview2").hide();
	    				  $(".upload-drop-image2").show();
	    				  $(".uploaded-preview-image2").show();
	    				  $(this).hide();
	    				  $("#rotateImg2").hide();
	  			          $("#desrotateImg2").hide();
	  			          $("#warningClickUpload2").show();
	  			          if ($.trim($('#content').val()).length < 1) {
	  			        	  $(':input[type="submit"]').prop('disabled', true);
	  			          }
	    			  });
	    			  
	    			  //Outdoor 3
	    			  $("#rmImg3").on('click', function(event) { 
	    				  $("#file3").val("");
	    				  $("#imgPreview3").hide();
	    				  $(".upload-drop-image3").show();
	    				  $(".uploaded-preview-image3").show();
	    				  $(this).hide();
	    				  $("#rotateImg3").hide();
	  			          $("#desrotateImg3").hide();
	  			          $("#warningClickUpload3").show();
	  			          if ($.trim($('#content').val()).length < 1) {
	  			        	  $(':input[type="submit"]').prop('disabled', true);
	  			          }
	    			  });	    			  
	    			  
	    			  //Outdoor 4
	    			  $("#rmImg4").on('click', function(event) { 
	    				  $("#file4").val("");
	    				  $("#imgPreview4").hide();
	    				  $(".upload-drop-image4").show();
	    				  $(".uploaded-preview-image4").show();
	    				  $(this).hide();
	    				  $("#rotateImg4").hide();
	  			          $("#desrotateImg4").hide();
	  			          $("#warningClickUpload4").show();
	  			          if ($.trim($('#content').val()).length < 1) {
	  			        	  $(':input[type="submit"]').prop('disabled', true);
	  			          }
	    			  });	    			  
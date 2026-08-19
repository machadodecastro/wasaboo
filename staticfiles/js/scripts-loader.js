//Froala Editor new reference about a new card
$('.new_reference').froalaEditor({
		key: 'KB-32jD-16llg1D-8H1qA-32y==',
        toolbarButtons: ['bold', 'italic', 'paragraphFormat', 'align', 'formatOL', 'formatUL', 'outdent', 'indent', 'quote',  
                         'selectAll', 'undo', 'redo', 'insertVideo', 'insertTable', 'insertFile', 'emoticons', 'embedly'],
        imageInsertButtons: [''],		
        imageEditButtons: [''],
		videoInsertButtons: ['videoByURL'],
		videoEditButtons: ['videoRemove'],
		linkEditButtons: [''],
        imagePasteProcess: false,
        imageUpload: true,
        imageMove: false,
        imagePaste: false,
        pastePlain: false,
        pasteDeniedTags: ['a', 'abbr', 'address', 'area', 'article', 'aside', 'audio', 'b', 'base', 'bdi', 'bdo', 
                          'blockquote', 'br', 'button', 'canvas', 'caption', 'cite', 'code', 'col', 'colgroup', 
                          'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'div', 'dl', 'dt', 'em', 'embed', 
                          'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                          'header', 'hgroup', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'keygen', 'label',
                          'legend', 'li', 'link', 'main', 'map', 'mark', 'menu', 'menuitem', 'meter', 'nav', 
                          'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'param', 'pre', 
                          'progress', 'queue', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 'style', 'section', 
                          'select', 'small', 'source', 'span', 'strike', 'strong', 'sub', 'summary', 'sup', 
                          'table', 'tbody', 'td', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 
                          'track', 'u', 'ul', 'var', 'video', 'wbr'],
        quickInsertTags: false,
        fontSize: false,
        shortcuts: false,
        fontFamily: false,
        disableRightClick: false,
        linkAlwaysBlank: true,
        toolbarButtonsMD: ['bold', 'italic', 'paragraphFormat', 'align', 'formatOL', 'formatUL', 'outdent', 'indent', 'quote',  
                           'selectAll', 'undo', 'redo', 'insertImage', 'insertVideo', 'insertTable'],
        toolbarButtonsSM: ['bold', 'italic', 'paragraphFormat', 'align', 'formatOL', 'formatUL', 'outdent', 'indent', 'quote',  
                           'selectAll', 'undo', 'redo', 'insertImage', 'insertVideo','insertTable'],
        toolbarButtonsXS: ['bold', 'italic', 'paragraphFormat', 'align', 'formatOL', 'formatUL', 'outdent', 'indent', 'quote',  
                           'undo', 'redo', 'insertImage', 'insertVideo', 'insertTable'], 
        charCounterMax: 1000,
        zIndex: 2501,
        paragraphFormat: {
        	N: 'Normal',
        	//H1: 'Heading 1',
            PRE: 'Code'
        },
        inlineMode: false,
        imageMaxSize: 4 * 1024 * 1024
}).on('froalaEditor.image.beforeUpload', function (e, editor, files) {
      if (files.length) {
        var reader = new FileReader();
        reader.onload = function (e) {
          var result = e.target.result;
          editor.image.insert(result, null, null, editor.image.get());
        };
        reader.readAsDataURL(files[0]);
      }
      return false;
    });


// Froala Editor reference when editing cards-->
$('.reference').froalaEditor({
        key: 'KB-32jD-16llg1D-8H1qA-32y==',
        toolbarButtons: ['bold', 'italic', 'paragraphFormat', 'align', 'formatOL', 'formatUL', 'outdent', 'indent', 'quote',  
                         'selectAll', 'undo', 'redo', 'insertVideo', 'insertTable', 'insertFile', 'emoticons', 'embedly'],
        imageInsertButtons: [''],
        imageEditButtons: [''],
		videoInsertButtons: ['videoByURL'],
		videoEditButtons: ['videoRemove'],
        linkEditButtons: [''],
        imagePasteProcess: false,
        imageUpload: true,
        imageMove: false,
        imagePaste: false,
        pastePlain: false,
        pasteDeniedTags: ['a', 'abbr', 'address', 'area', 'article', 'aside', 'audio', 'b', 'base', 'bdi', 'bdo', 
                          'blockquote', 'br', 'button', 'canvas', 'caption', 'cite', 'code', 'col', 'colgroup', 
                          'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'div', 'dl', 'dt', 'em', 'embed', 
                          'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                          'header', 'hgroup', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'keygen', 'label',
                          'legend', 'li', 'link', 'main', 'map', 'mark', 'menu', 'menuitem', 'meter', 'nav', 
                          'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'param', 'pre', 
                          'progress', 'queue', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 'style', 'section', 
                          'select', 'small', 'source', 'span', 'strike', 'strong', 'sub', 'summary', 'sup', 
                          'table', 'tbody', 'td', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 
                          'track', 'u', 'ul', 'var', 'video', 'wbr'],
        quickInsertTags: false,
        fontSize: false,
        shortcuts: false,
        fontFamily: false,
        disableRightClick: false,
        linkAlwaysBlank: true,
        toolbarButtonsMD: ['bold', 'italic', 'paragraphFormat', 'align', 'formatOL', 'formatUL', 'outdent', 'indent', 'quote',  
                           'selectAll', 'undo', 'redo', 'insertImage', 'insertVideo','insertTable'],
        toolbarButtonsSM: ['bold', 'italic', 'paragraphFormat', 'align', 'formatOL', 'formatUL', 'outdent', 'indent', 'quote',  
                           'selectAll', 'undo', 'redo', 'insertImage', 'insertVideo', 'insertTable'],
        toolbarButtonsXS: ['bold', 'italic', 'paragraphFormat', 'align', 'formatOL', 'formatUL', 'outdent', 'indent', 'quote',  
                           'undo', 'redo', 'insertImage', 'insertVideo', 'insertTable'], 
        charCounterMax: 1000,
        zIndex: 2501,
        paragraphFormat: {
        	N: 'Normal',
        	//H1: 'Heading 1',
            PRE: 'Code'
        },
        paragraphy: false,
        inlineMode: true,

        // Set max image size to 5MB.
        imageMaxSize: 5 * 1024 * 1024,

        // Allow to upload PNG and JPG.
        imageAllowedTypes: ['jpeg', 'jpg', 'png']
}).on('froalaEditor.image.beforeUpload', function (e, editor, files) {
      if (files.length) {
        var reader = new FileReader();
        reader.onload = function (e) {
          var result = e.target.result;
          editor.image.insert(result, null, null, editor.image.get());
        };
        reader.readAsDataURL(files[0]);
      }
      return false;
    })
    .on('froalaEditor.image.inserted', function (e, editor, $img, response) {
    });


// Transform class into Froala Editor for index page -->
$('.title-content').froalaEditor({
    key: 'KB-32jD-16llg1D-8H1qA-32y==',
	toolbarButtons: [''],
    quickInsertTags: [''],
    disableRightClick: false, 
    fontSize: false,
    fontFamily: false,
    toolbarButtonsMD: [''],
    toolbarButtonsSM: [''],
    toolbarButtonsXS: [''], 
    charCounterCount: false,
    contenteditable: false,
    imageEditButtons: [''],
    imageInsertButtons: [''],
    placeholderText: '',
    imagePasteProcess: false,
    pastePlain: false,
    paragraphy: false
});


// Show references and avoid editing -->
$('.reference-content').froalaEditor({
    key: 'KB-32jD-16llg1D-8H1qA-32y==',
	toolbarButtons: [''],
    quickInsertTags: [''],
    disableRightClick: false, 
    fontSize: false,
    fontFamily: false,
    toolbarButtonsMD: [''],
    toolbarButtonsSM: [''],
    toolbarButtonsXS: [''], 
    charCounterCount: false,
    contenteditable: false,
    imageEditButtons: [''],
    imageInsertButtons: [''],
    placeholderText: '',
    imagePasteProcess: false,
    pastePlain: false,
    paragraphy: false
});


// Avoid writing inside cards
$( document ).ready(function() {
	  $(".title-content").on("keydown", function(e) {
	      e.preventDefault();
	  });
});


// Avoid image drag and drop AND press RETURN
$( document ).ready(function() {
	  $(".title-content").each(function() {
	    	self = $(this);
	    	var wasabooref = "{{url}}";
	    	var tip = $(this).data("id");
	    	var content = $(this).data("content");
	    		
	    	$('.title-content-'+tip).froalaEditor('html.set', content); //set content
           	$('.title-content-'+tip).froalaEditor('edit.off'); //disable all froala editors in index
	  });
});	

//Avoid writing inside cards
$( document ).ready(function() {
	  $(".reference-content").on("keydown", function(e) {
	      e.preventDefault();
	  });
});


// Avoid image drag and drop AND press RETURN
$( document ).ready(function() {
	  $(".reference-content").each(function() {
	    	self = $(this);
	    	var wasabooref = "{{url}}";
	    	var tip = $(this).data("id");
	    	var reference = $(this).data("reference");
	    		
	    	$('.reference-content-'+tip).froalaEditor('html.set', reference); //set content
           	$('.reference-content-'+tip).froalaEditor('edit.off'); //disable all froala editors in index
	  });
});	


//Show play/table toolbar 
$(".toolbtn").on('click',function(){ 
	self = $(this);
	var id = $(this).data("id"); 
	$('.points-'+id).animate({  borderSpacing: 0 }, {
	    step: function(now,fx) {
	    	$('.points-'+id).removeClass('rudder-active');
	        $(this).css('-webkit-transform','rotate('+now+'deg)'); 
	        $(this).css('-moz-transform','rotate('+now+'deg)');
	        $(this).css('transform','rotate('+now+'deg)');
	      },
	      duration: 500
	  },'linear');    	
	$('.edit-toolbar-'+id).css("display", "none");
	$('.toolbar-'+id).css("display", "grid");
	$('.toolbar-'+id).toggleClass("slidedown slideup");
	$('.toolbtn-'+id).toggleClass("down-arrow up-arrow");
});


// Show Edit-Toolbar buttons  --> 
$(".rudder").on('click',function(){
	self = $(this);
	var id = $(this).data("id");    	
	$('.points-'+id).animate({  borderSpacing: -90 }, {
	    step: function(now,fx) {
	    	$('.points-'+id).addClass('rudder-active');
	        $(this).css('-webkit-transform','rotate('+now+'deg)'); 
	        $(this).css('-moz-transform','rotate('+now+'deg)');
	        $(this).css('transform','rotate('+now+'deg)');    	            	        
	      },
	      duration: 500
	  },'linear');    	
	$('.toolbar-'+id).css("display", "none");
	$('.edit-toolbar-'+id).css("display", "grid"); 
});

// Back from edit options to play/table toolbar  --> 
$(".backtools").on('click',function(){
	self = $(this);
	var id = $(this).data("id");
	$('.points-'+id).animate({  borderSpacing: 90 }, {
	    step: function(now,fx) {
	    	$('.points-'+id).removeClass('rudder-active');
	        $(this).css('-webkit-transform','rotate('+now+'deg)'); 
	        $(this).css('-moz-transform','rotate('+now+'deg)');
	        $(this).css('transform','rotate('+now+'deg)');    	        
	      },
	      duration: 500
	  },'linear');
	$('.edit-toolbar-'+id).css("display", "none");
	$('.toolbar-'+id).css("display", "grid");
});

	
// Show delete confirm question 
$(".show-confirm").on('click',function (){
	self = $(this);
	var tip = $(this).data("id"); 
   	$('.title-content-'+tip).froalaEditor('html.set');
   	$('.title-content-'+tip).froalaEditor('edit.off');
   	$('.confirm-delete-question-'+tip).show();
   	$('.panel-heading-'+tip).hide();
   	$('.picture-'+tip).hide();
   	$('.tag-'+tip).hide();
   	$('.fotorama-'+tip).hide();
});

//Show delete confirm question 
$(".show-confirm-in-card").on('click',function (){
	self = $(this);
	var tip = $(this).data("id"); 
	$('.title-outdoor-'+tip).hide();
   	$('.title-content-'+tip).froalaEditor('html.set');
   	$('.title-content-'+tip).froalaEditor('edit.off');
   	$('.confirm-delete-question-in-card-'+tip).show();
   	$('.panel-heading-'+tip).hide();
   	$('.picture-'+tip).hide();
   	$('.tag-'+tip).hide();
   	$('.fotorama-'+tip).hide();
});

// Button NO - Return from delete confirm question 
$(".btn-no").on('click',function (){  
	self = $(this);
	var tip = $(this).data("id"); 
	var content = $(this).data("content"); 
	$('.title-content-'+tip).froalaEditor('html.set', content);
	$('.title-content-'+tip).froalaEditor('edit.off');
   	$('.confirm-delete-question-'+tip).hide();	
   	$(".show-references-"+tip).show();
	$(".show-back-"+tip).hide();
	$('.panel-heading-'+tip).show();
	$('.picture-'+tip).show();
	$('.tag-'+tip).show();
	$('.fotorama-'+tip).show();
});

//Button NO - Return from delete confirm question in CARD page 
$(".btn-no-in-card").on('click',function (){  
	self = $(this);
	var tip = $(this).data("id"); 
	var content = $(this).data("content"); 
	var reference = $(this).data("reference"); 
	$('.title-outdoor-'+tip).show();
	$('.title-content-'+tip).froalaEditor('html.set', reference);
	$('.title-content-'+tip).froalaEditor('edit.off');
   	$('.confirm-delete-question-in-card-'+tip).hide();	
	$('.panel-heading-'+tip).show();
	$('.picture-'+tip).show();
	$('.tag-'+tip).show();
	$('.fotorama-'+tip).show();
});


// List folder options 
$(".choose-folders").on('click',function (){  
	self = $(this);
	var tip = $(this).data("id"); 
	var content = $(this).data("content");
   	$('.title-content-'+tip).froalaEditor('html.set');
   	$('.title-content-'+tip).froalaEditor('edit.off');
   	$('.confirm-folders-options-'+tip).show();
   	$('.panel-heading-'+tip).hide();
   	$('.picture-'+tip).hide();
   	$('.tag-'+tip).hide();
   	$('.fotorama-'+tip).hide();
   	$('.title-content-'+tip).css('display','block');	
});

//List folder options in Card page
$(".choose-folders-in-card").on('click',function (){  
	self = $(this);
	var tip = $(this).data("id");
	var content = $(this).data("content");
	$('.title-outdoor-'+tip).hide();	
   	$('.title-content-'+tip).froalaEditor('html.set');
   	$('.title-content-'+tip).froalaEditor('edit.off');
   	$('.title-content-'+tip).hide();
   	$('.reference-content-'+tip).hide();
   	$('.confirm-folders-options-'+tip).show();
   	$('.panel-heading-'+tip).hide();
   	$('.picture-'+tip).hide();
   	$('.tag-'+tip).hide();
   	$('.fotorama-'+tip).hide();
});


// Show folder name where card was saved
$(".show-folders").on('click',function (){  
	self = $(this);
	var tip = $(this).data("id");
	var content = $(this).data("content");
   	$('.title-content-'+tip).froalaEditor('html.set');
   	$('.title-content-'+tip).froalaEditor('edit.off');
   	$('.folder-container-'+tip).show();
   	$('.panel-heading-'+tip).hide();
   	$('.picture-'+tip).hide(); 
   	$('.tag-'+tip).hide();
   	$('.fotorama-'+tip).hide();
   	$('.title-content-'+tip).css('display','block');
});

//Show folder name where card was saved in Card page
$(".show-folders-in-card").on('click',function (){
	self = $(this);
	var tip = $(this).data("id"); 
	var content = $(this).data("content");
	$('.title-outdoor-'+tip).hide();
   	$('.title-content-'+tip).froalaEditor('html.set');
   	$('.title-content-'+tip).froalaEditor('edit.off');
   	$('.title-content-'+tip).hide();
   	$('.reference-content-'+tip).hide();
   	$('.folder-container-'+tip).show();
   	$('.panel-heading-'+tip).hide();
   	$('.picture-'+tip).hide(); 
   	$('.tag-'+tip).hide();
   	$('.fotorama-'+tip).hide();
});


// Button CANCEL - Return from list folder options 
$(".btn-cancel").on('click',function (){  
	self = $(this);
	var tip = $(this).data("id"); 
	var content = $(this).data("content");
	$('.title-content-'+tip).froalaEditor('html.set', content);
	$('.title-content-'+tip).froalaEditor('edit.off');
   	$('.confirm-folders-options-'+tip).hide();
   	$('.folder-container-'+tip).hide();
   	$('.chat-container-'+tip).hide();
   	$(".show-references-"+tip).show();
	$(".show-back-"+tip).hide();
	$('.panel-heading-'+tip).show();
	$('.picture-'+tip).show();
	$('.tag-'+tip).show();
	if (content) {
		$('.title-content-'+tip).css('display','block');
   	} else {
   		$('.title-content-'+tip).css('display','none');
   	}
	$('.fotorama-'+tip).show();
});

//Button CANCEL - Return from list folder options 
$(".btn-cancel-in-card").on('click',function (){  
	self = $(this);
	var tip = $(this).data("id"); 
	var content = $(this).data("content"); 
	var reference = $(this).data("reference");
	$('.title-outdoor-'+tip).show();
	$('.title-content-'+tip).froalaEditor('html.set', reference);
	$('.title-content-'+tip).froalaEditor('edit.off');
	$('.title-content-'+tip).show();
	$('.reference-content-'+tip).show();
   	$('.confirm-folders-options-'+tip).hide();
   	$('.folder-container-'+tip).hide();
   	$('.chat-container-'+tip).hide();
	$('.panel-heading-'+tip).show();
	$('.picture-'+tip).show();
	$('.tag-'+tip).show();
	$('.fotorama-'+tip).show();
});


//Start Chat
$(".chat").on('click',function (){ 
	self = $(this);
	var tip = $(this).data("id"); 
	var content = $(this).data("content");
	$('.title-outdoor-'+tip).hide();
   	$('.title-content-'+tip).froalaEditor('html.set');
   	$('.title-content-'+tip).froalaEditor('edit.off');
   	$('.title-content-'+tip).hide();
   	$('.reference-content-'+tip).hide();
   	$('.chat-container-'+tip).show();
   	$('.panel-heading-'+tip).hide();
   	$('.picture-'+tip).hide(); 
   	$('.tag-'+tip).hide();
   	$('.fotorama-'+tip).hide();
});


//Card tips
$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
    $('[data-tt="tooltip"]').tooltip();
});


// ROTATE OUTDOOR 1 
$( document ).ready(function() {
	$("#rotateImg").on('mouseover', function(event) {
		  var id = $(this).data("id");
		  var value = 0
		  $("#rotateImg").rotate({
		    bind:
		    {
		      click: function(){
		        value =90;
		        $(".imgpreview-"+id).rotate({ animateTo:value});
		        $("#direction").val('1');
		      }
		    }
		  });
	});
	$("#desrotateImg").on('mouseover', function(event) {
		  var id = $(this).data("id");
		  var value = 0
		  $("#desrotateImg").rotate({
		    bind:
		    {
		      click: function(){
		        value =0;
		        $(".imgpreview-"+id).rotate({ animateTo:value});
		        $("#direction").val('0');
		      }
		    }
		  });
	});	
});

//ROTATE OUTDOOR 2 
$( document ).ready(function() {
	$("#rotateImg2").on('mouseover', function(event) {
		  var id = $(this).data("id");
		  var value = 0
		  $("#rotateImg2").rotate({
		    bind:
		    {
		      click: function(){
		        value =90;
		        $(".imgpreview2-"+id).rotate({ animateTo:value});
		        $("#direction2").val('1');
		      }
		    }
		  });
	});
	$("#desrotateImg2").on('mouseover', function(event) {
		  var id = $(this).data("id");
		  var value = 0
		  $("#desrotateImg2").rotate({
		    bind:
		    {
		      click: function(){
		        value =0;
		        $(".imgpreview2-"+id).rotate({ animateTo:value});
		        $("#direction2").val('0');
		      }
		    }
		  });
	});	
});


//ROTATE OUTDOOR 3 
$( document ).ready(function() {
	$("#rotateImg3").on('mouseover', function(event) {
		  var id = $(this).data("id");
		  var value = 0
		  $("#rotateImg3").rotate({
		    bind:
		    {
		      click: function(){
		        value =90;
		        $(".imgpreview3-"+id).rotate({ animateTo:value});
		        $("#direction3").val('1');
		      }
		    }
		  });
	});
	$("#desrotateImg3").on('mouseover', function(event) {
		  var id = $(this).data("id");
		  var value = 0
		  $("#desrotateImg3").rotate({
		    bind:
		    {
		      click: function(){
		        value =0;
		        $(".imgpreview3-"+id).rotate({ animateTo:value});
		        $("#direction3").val('0');
		      }
		    }
		  });
	});	
});


//ROTATE OUTDOOR 4
$( document ).ready(function() {
	$("#rotateImg4").on('mouseover', function(event) {
		  var id = $(this).data("id");
		  var value = 0
		  $("#rotateImg4").rotate({
		    bind:
		    {
		      click: function(){
		        value =90;
		        $(".imgpreview4-"+id).rotate({ animateTo:value});
		        $("#direction4").val('1');
		      }
		    }
		  });
	});
	$("#desrotateImg4").on('mouseover', function(event) {
		  var id = $(this).data("id");
		  var value = 0
		  $("#desrotateImg4").rotate({
		    bind:
		    {
		      click: function(){
		        value =0;
		        $(".imgpreview4-"+id).rotate({ animateTo:value});
		        $("#direction4").val('0');
		      }
		    }
		  });
	});	
});

//Scroll page
$('.scroll').jscroll({
    autoTriggerUntil: 3
});



//Filter cards to play to another one
function searchCards() {
    // Declare variables
    var input, filter, ul, li, a, i;
    input = document.getElementById('myCards');
    filter = input.value.toUpperCase();
    ul = document.getElementById("myULCards");
    li = ul.getElementsByTagName('li');

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("div")[0];
        if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {        	
        	li[i].style.opacity = 1;
        	$(li[i]).prependTo( $( "#myULCards" ) );
        } else {
            li[i].style.opacity = 0;
            $(li[i]).appendTo( $( "#myULCards" ) );          
        }        
    }
}

//Filter played cards to you
function searchHolds() {
    // Declare variables
    var input, filter, ul, li, a, i;
    input = document.getElementById('myHolds');
    filter = input.value.toUpperCase();
    ul = document.getElementById("myULHolds");
    li = ul.getElementsByTagName('li'); 

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) { 
        a = li[i].getElementsByTagName("div")[0];
        if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {        	
        	li[i].style.opacity = 1;
        	$(li[i]).prependTo( $( "#myULHolds" ) );
        } else {
            li[i].style.opacity = 0;
            $(li[i]).appendTo( $( "#myULHolds" ) );          
        }        
    }
}

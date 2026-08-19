//Froala Editor new reference about a new card
	$('.new_reference').froalaEditor({
            toolbarButtons: ['bold', 'italic', 'paragraphFormat', 'align', 'formatOL', 'formatUL', 'outdent', 'indent', 'quote',  
                             'selectAll', 'undo', 'redo'],
            imageInsertButtons: [''],
            imageEditButtons: [''],
            pastePlain: false,
            imagePasteProcess: false,
            imageUpload: true,
            imageMove: false,
            imagePaste: false,
            quickInsertTags: false,
            fontSize: false,
            shortcuts: false,
            fontFamily: false,
            disableRightClick: false,
            linkAlwaysBlank: true,
            toolbarButtonsMD: ['bold', 'italic', 'paragraphFormat', 'align', 'formatOL', 'formatUL', 'outdent', 'indent', 'quote',  
                               'selectAll', 'undo', 'redo'],
            toolbarButtonsSM: ['bold', 'italic', 'paragraphFormat', 'align', 'formatOL', 'formatUL', 'outdent', 'indent', 'quote',  
                               'selectAll', 'undo', 'redo'],
            toolbarButtonsXS: ['bold', 'italic', 'paragraphFormat', 'align', 'formatOL', 'formatUL', 'outdent', 'indent', 'quote',  
                               'undo', 'redo'], 
            charCounterMax: 1000,
            zIndex: 2501,
            paragraphFormat: {
            	N: 'Normal',
            	//H1: 'Heading 1',
                PRE: 'Code'
            },
            inlineMode: false,
            imageUploadURL: 'blob:http://127.0.0.1:8000/tip/new',
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
            toolbarButtons: ['bold', 'italic', 'paragraphFormat', 'align', 'formatOL', 'formatUL', 'outdent', 'indent', 'quote',  
                             'selectAll', 'undo', 'redo'],
            imageInsertButtons: ['imageUpload', 'imageByURL'],
            imageEditButtons: ['imageReplace', 'imageAlign', 'imageDisplay', 'imageAlt', 'imageRemove'],
            pastePlain: true,
            imagePasteProcess: true,
            quickInsertTags: [''],
            fontSize: false,
            fontFamily: false,
            disableRightClick: false,
            linkAlwaysBlank: true,
            toolbarButtonsMD: ['bold', 'italic', 'paragraphFormat', 'align', 'formatOL', 'formatUL', 'outdent', 'indent', 'quote',  
                               'selectAll', 'undo', 'redo'],
            toolbarButtonsSM: ['bold', 'italic', 'paragraphFormat', 'align', 'formatOL', 'formatUL', 'outdent', 'indent', 'quote',  
                               'selectAll', 'undo', 'redo'],
            toolbarButtonsXS: ['bold', 'italic', 'paragraphFormat', 'align', 'formatOL', 'formatUL', 'outdent', 'indent', 'quote',  
                               'undo', 'redo'], 
            charCounterMax: 1000,
            zIndex: 2501,
            paragraphFormat: {
            	N: 'Normal',
            	//H1: 'Heading 1',
                PRE: 'Code'
            },
            paragraphy: false,
            inlineMode: true,
         // Set the image upload parameter.
            imageUploadParam: 'image_param',

            // Set the image upload URL.
            imageUploadURL: '/upload_image',

            // Additional upload params.
            imageUploadParams: {id: 'edit_reference'},

            // Set request type.
            imageUploadMethod: 'POST',

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

/* Limit words in Edit Tip */
(function($){
	$.fn.textareaEditTipCounter = function(options) {
		// setting the defaults
		// $("textarea").textareaCounter({ limit: 100 });
		var defaults = {
			limit: 100
		};	
		var options = $.extend(defaults, options);

		// and the plugin begins
		return this.each(function() {
			var obj, text, wordcount, limited;
			
			obj = $(this);
			obj.after('<span style="position:absolute;color: #ccc; font-size: 15px; clear: both; margin-top: 20px; display: block;" class="counter-edit-tip">Max. '+options.limit+' characters</span>');

			obj.keyup(function() {
			    text = obj.val();
			    if(text === "") {
			    	wordcount = 0;
			    } else {
				    wordcount = $.trim(text).split("").length;
				}
			    if(wordcount > options.limit) {
			        $(".counter-edit-tip").html('<span style="color: #ccc;">0/100</span>');
					limited = $.trim(text).split("", options.limit);
					limited = limited.join("");
					$(this).val(limited);
			    } else {
			        $(".counter-edit-tip").html((options.limit - wordcount)+' words left');
			    } 
			});
		});
	};
})(jQuery);



/* Script for counting the words in Edit Tip */
$(".edit_content").textareaEditTipCounter();

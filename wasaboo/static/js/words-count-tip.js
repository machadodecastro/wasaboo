/* Limit words in textarea */
(function($){
	$.fn.textareaCounter = function(options) {
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
			obj.after('<span style="float:left;color: #ccc; font-size: 15px; clear: both; padding: 24px 0; margin-top: 20px; display: block;" id="counter-text">Max. '+options.limit+' characters</span>');

			obj.keyup(function() {
			    text = obj.val();
			    if(text === "") {
			    	wordcount = 0;
			    } else {
				    wordcount = $.trim(text).split("").length;
				}
			    if(wordcount > options.limit) {
			        $("#counter-text").html('<span style="float:right;color: #ccc;">0/100</span>');
					limited = $.trim(text).split("", options.limit);
					limited = limited.join("");
					$(this).val(limited);
			    } else {
			        $("#counter-text").html((options.limit - wordcount)+'/100');
			    } 
			});
		});
	};
})(jQuery);


/* Script for counting the words of a tip */
$("#content").textareaCounter();

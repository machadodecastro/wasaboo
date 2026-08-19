/* Limit words in Who Am I Profile page */
(function($){
	$.fn.textareaCompanyCounter = function(options) {
		// setting the defaults
		// $("textarea").textareaCounter({ limit: 100 });
		var defaults = {
			limit: 327
		};	
		var options = $.extend(defaults, options);
 
		// and the plugin begins
		return this.each(function() {
			var obj, text, wordcount, limited;
			
			obj = $(this);
			obj.after('<span style="color: #ccc; font-size: 11px; clear: both; margin-top: 3px; display: block;" id="counter-company">Max. '+options.limit+' words</span>');

			obj.keyup(function() {
			    text = obj.val();
			    if(text === "") {
			    	wordcount = 0;
			    } else {
				    wordcount = $.trim(text).split("").length;
				}
			    if(wordcount > options.limit) {
			        $("#counter-company").html('<span style="color: #ccc;">0 words left</span>');
					limited = $.trim(text).split("", options.limit);
					limited = limited.join("");
					$(this).val(limited);
			    } else {
			        $("#counter-company").html((options.limit - wordcount)+' words left');
			    } 
			});
		});
	};
})(jQuery);


/* Script for counting the words of Who Am I Profile page */
$("#company_content").textareaCompanyCounter();

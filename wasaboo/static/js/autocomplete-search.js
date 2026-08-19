<!-- Autocomplete search -->
$( document ).ready(function() {
    // In a perfect world, this would be its own library file that got included
    // on the page and only the ``$(document).ready(...)`` below would be present.
    // But this is an example.
    var Autocomplete = function(options) {
      this.form_selector = options.form_selector
      this.url = options.url || '/autocomplete/'
      this.delay = parseInt(options.delay || 300)
      this.minimum_length = parseInt(options.minimum_length || 1)
      this.form_elem = null
      this.query_box = null
    }

    Autocomplete.prototype.setup = function() {
      var self = this

      this.form_elem = $(this.form_selector)
      this.query_box = this.form_elem.find('input[name=q]')

      // Watch the input box.
      this.query_box.on('keyup', function() {
        var query = self.query_box.val()

        if(query.length < self.minimum_length) {
          $('.ac-results').remove()
          return false
        }

        self.fetch(query)
      })

      // On selecting a result, populate the search field.
      this.form_elem.on('click', '.ac-result', function(ev) {
        self.query_box.val($(this).text())
        $('.ac-results').remove()
        $('.autocomplete-me').submit()
        return false
      })
      // On click outside.
      $(window).click(function() {
        $('.ac-results').remove()
      })      
    }

    Autocomplete.prototype.fetch = function(query) {
      var self = this

      $.ajax({
        url: this.url
      , data: {
          'q': query
        }
      , success: function(data) {
          self.show_results(data)
        }
      })
    }

    Autocomplete.prototype.show_results = function(data) {
      // Remove any existing results.
      $('.ac-results').remove()

      var results = data.results ||  []
      var authors = data.authors ||  []
      var results_wrapper = $('<div class="ac-results"></div>')
      var base_elem = $('<a href="#"><div style="margin: 0 10px;border-bottom: 1px solid #efefef;color:#ccc;"></div><div class="result-wrapper ac-result"></div></a>')
      var base_author = $('<a href="#"><span style="margin: 0 10px;color:#ccc;"> <div class="author-result ac-result" style="display:inline-block;"></div></span></a><br/><br/>')
	  
      if(results.length > 0) {
        for(var res_offset in results) {
          var elem= base_elem.clone()
          elem.find('.ac-result').text(results[res_offset])
          results_wrapper.append(elem)

          var elema= base_author.clone()
		      elema.find('.author-result').text(authors[res_offset])
		      results_wrapper.append(elema)	
        }        		    	    
      }
      else {
        var elem = base_elem.clone()
        elem.text("No results found.")
        results_wrapper.remove(elem)
      }
      
      this.query_box.after(results_wrapper)
    }

    $(document).ready(function() {
      window.autocomplete = new Autocomplete({
        form_selector: '.autocomplete-me'
      })
      window.autocomplete.setup()
    })
});
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
      var outdoors = data.outdoors ||  []
      var authors = data.authors ||  []
      var profile_id = data.profile_id ||  []
      var slug = data.slug ||  []
      var id = data.id ||  []
      
      var campaigns = data.campaigns ||  []
      
      var uploads = data.uploads ||  []
      
      
      var results_wrapper = $('<div class="ac-results"></div>')
      var base_elem = $('<a href="#"><div style="margin: 0 10px;color:#ccc;"></div><div class="result-wrapper ac-result"></div></a>')
      var base_author = $('<a href="#"> <div class="author-result" style="margin: 0 10px;display:inline-block;"></div></span></a><br/><br/>')
	  var base_campaign = $('<a href="#"><span style="margin: 0 10px;color:#ccc;"><img class="flag-menu"/> <div class="campaign-result ac-result" style="display:inline-block;"></div></span></a><br/><br/>')
	 	  

      if(results.length) {
        for(var res_offset in results) {
          
          var elem= base_elem.clone() //conteudo do outdoor
          var elem2= base_elem.clone() //imagem do outdoor
          var elem3= base_author.clone() //nome do perfil
          var elem4= base_campaign.clone() //campanha
          
          elem.find('.ac-result').text(results[res_offset])
          elem2.find('.ac-result').text(outdoors[res_offset])
          elem3.find('.author-result').text(authors[res_offset])
          elem4.find('.campaign-result').text(campaigns[res_offset])
          
          //Se outdoor tiver título
          if (elem.text() != ''){
        	              
            //Se tiver imagem
            if (elem2.text() != '') {
              results_wrapper.append('<a href="/'+slug[res_offset]+'-'+id[res_offset]+'"><div class="auto-title">'+results[res_offset]+'</div></a>')
              results_wrapper.append('<a href="/'+slug[res_offset]+'-'+id[res_offset]+'"> <span class="auto-outdoor"><img src="/media/'+outdoors[res_offset]+'" class="auto-img"></span></a><br/>')
            } else {
                results_wrapper.append('<a href="/'+slug[res_offset]+'-'+id[res_offset]+'"><div class="auto-title-sem-imagem">'+results[res_offset]+'</div></a>')
            }
            //Nome do autor
            //results_wrapper.append('<span style="margin: 0 10px;color:#ccc;"><span class="user"><img src="'+uploads[res_offset]+'" class="user" alt="user picture"></span>')
            results_wrapper.append('<a href="/profile/'+profile_id[res_offset]+'"> <div class="auto-author">'+authors[res_offset]+'</div></span></a><br/><br/>')
            results_wrapper.append('<hr/>')
          
          //Caso não tenha título
          } else {
              
        	//Se tiver imagem
            if (elem2.text() != '') {
              results_wrapper.append('<a href="/'+slug[res_offset]+'-'+id[res_offset]+'"> <span class="auto-outdoor"><img src="/media/'+outdoors[res_offset]+'" style="width:100px;height:auto;"></span></a>')
              //results_wrapper.append('<span style="margin: 0 10px;color:#ccc;"><span class="user"><img src="'+uploads[res_offset]+'" class="user" alt="user picture"></span>')
              results_wrapper.append('<a href="/profile/'+profile_id[res_offset]+'"> <div class="auto-author">'+authors[res_offset]+'</div></span></a><br/><br/>')
              results_wrapper.append('<hr/>')              
            }
               
          }
          

          /*
          if (elem.text() != ''){
              results_wrapper.append(elem)
            }
            
            if (elem2.text() != '') {
             	results_wrapper.append('<span style="margin: 0 10px;color:#ccc;"><img src="/media/'+outdoors[res_offset]+'" style="width:100px;height:auto;"></span><br/><br/>')
            }
            
            results_wrapper.append('<span style="margin: 0 10px;color:#ccc;"><span class="user"><img src="'+uploads[res_offset]+'" class="user" alt="user picture"></span>')
            results_wrapper.append(authors[res_offset])
            
            if (elem4.text() != ''){
  	          results_wrapper.append(elem4)
  	      }
          */

          
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
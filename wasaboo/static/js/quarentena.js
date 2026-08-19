<!-- Edit card no Ajax -->
<script type="text/javascript">
	$(document).ready(function(){
		jQuery('.pencil-{{tip.id}}').click(function(e) {
			var wasabooref = "{{url}}";
			var idCard = $(this).data("id");
			var url = "http://" + wasabooref + "/edit-card/"+idCard;
			
			$('.modal-container').load(url,function(result){
				$('#updateCard-{{tip.id}}').modal({show:true});
			});
		});
	});
</script>
	
	
	
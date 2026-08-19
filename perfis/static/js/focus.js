/* Focus when open the textarea modal */
$('#newTip').on('shown.bs.modal', function() {
    $(this).find('textarea[name="content"]').focus();
});

/* Focus when open the input profile name */
$('#updateProfileName').on('shown.bs.modal', function() {
    $(this).find('input[name="nome"]').focus();
});

/* Focus when open the textarea for short description */
$('#updateShortDescription').on('shown.bs.modal', function() {
    $(this).find('textarea[name="description"]').focus();
});	

/* Focus when open the textarea for Who am I profile edition */
$('#newWhoAmI').on('shown.bs.modal', function() {
    $(this).find('textarea[name="whoami_content"]').focus();
});	

/* Focus when open the textarea for Who am I profile edition */
$('#updateTip').on('shown.bs.modal', function() {
    $(this).find('textarea[name="content"]').focus();
});		

/* Focus when open the textarea for Who am I EDIT profile edition */
$('#updateWhoAmI').on('shown.bs.modal', function() {
    $(this).find('textarea[name="whoami_content"]').focus();
});	

/* Focus when open the textarea for Knows About profile edition */
$('#newKnows').on('shown.bs.modal', function() {
    $(this).find('input[name="topic"]').focus();
});

/* Focus when open the textarea for Knows About EDIT profile edition */
$('#updateKnows').on('shown.bs.modal', function() {
    $(this).find('input[name="topic"]').focus();
});	

/* Focus when open the input for Jobs profile edition */
$('#newJobs').on('shown.bs.modal', function() {
    $(this).find('input[name="company"]').focus();
});

/* Focus when open the input for Jobs EDIT profile edition */
$('#updateJobs').on('shown.bs.modal', function() {
    $(this).find('input[name="company"]').focus();
});

/* Focus when open the input for Where I Live profile edition */
$('#newLive').on('shown.bs.modal', function() {
    $(this).find('input[name="location"]').focus();
});

/* Focus when open the input for Where I Live EDIT profile edition */
$('#updateLive').on('shown.bs.modal', function() {
    $(this).find('input[name="location"]').focus();
});

/* Focus when open the textarea for Hobbies profile edition */
$('#newHobby').on('shown.bs.modal', function() {
    $(this).find('textarea[name="hobby_content"]').focus();
});	

/* Focus when open the textarea for Hobbies EDIT profile edition */
$('#updateHobby').on('shown.bs.modal', function() {
    $(this).find('textarea[name="hobby_content"]').focus();
});	

/* Focus when open the textarea for Company profile */
$('#newCompany').on('shown.bs.modal', function() {
    $(this).find('textarea[name="company_content"]').focus();
});	

/* Focus when open the textarea for Company EDIT profile */
$('#updateCompany').on('shown.bs.modal', function() {
    $(this).find('textarea[name="company_content"]').focus();
});	

/* Focus when open the input for Job Offers */
$('#newOffer').on('shown.bs.modal', function() {
    $(this).find('input[name="offer_title"]').focus();
});

/* Focus when open the input for Job Offers EDIT */
$('#updateOffer').on('shown.bs.modal', function() {
    $(this).find('input[name="offer_title"]').focus();
});
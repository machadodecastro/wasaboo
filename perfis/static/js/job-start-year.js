var start_start_year = 1900;
var end_start_year = new Date().getFullYear();
var option_start_year ="";
var options_start_year = "";
for(var year_start_year = start_start_year ; year_start_year <= end_start_year; year_start_year++){
   edit_start_year_option = "<option selected class='start_year' style='background-color:#93c4d3;color:#fff;'></option>";
   option_start_year = "<option disabled selected value></option>";
   options_start_year += "<option>"+ year_start_year +"</option>";
}
document.getElementById("start_year").innerHTML = option_start_year + options_start_year;

document.getElementById("edit_start_year").innerHTML = edit_start_year_option + options_start_year;





var start_end_year = 1900;
var end_end_year = new Date().getFullYear();
var option_end_year ="";
var options_end_year = "";
for(var year_end_year = start_end_year ; year_end_year <= end_end_year; year_end_year++){
   edit_end_year_option = "<option selected class='end_year_living' style='background-color:#93c4d3;color:#fff;'></option>";
   option_end_year = "<option disabled selected value></option>";
   options_end_year += "<option>"+ year_end_year +"</option>";
}
document.getElementById("end_year_living").innerHTML = option_end_year + options_end_year;

document.getElementById("edit_end_year_living").innerHTML = edit_end_year_option + options_end_year;
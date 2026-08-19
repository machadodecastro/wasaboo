var start = 1900;
var end = new Date().getFullYear();
var option ="";
var options = "";
for(var year = start ; year <=end; year++){
   edit_option = "<option selected class='graduation' style='background-color:#93c4d3;color:#fff;'></option>";
   option = "<option disabled selected value></option>";
   options += "<option>"+ year +"</option>";
}
document.getElementById("graduation").innerHTML = option + options;

document.getElementById("edit_graduation").innerHTML = edit_option + options;

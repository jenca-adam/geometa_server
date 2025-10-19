if(!localStorage.token){
    location.replace("/login");
}
$("#site").hide();
$(document).ready(() =>{
    $("#site").show();
    $(".tabs").tabs();
});

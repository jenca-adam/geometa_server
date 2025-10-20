if (localStorage.isAdmin=="true"){
    $("#logout").removeClass("hidden");
}
else{
    $("#login").removeClass("hidden");
}
$("#logout").click(function(){
    localStorage.isAdmin = "false";
    localStorage.removeItem("token");
    location.reload();
})
$("#login").click(function(){
    location.replace("/login");
});

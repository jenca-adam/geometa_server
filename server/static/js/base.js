if (localStorage.isAdmin=="true"){
    $("#logout").removeClass("hidden");
    $("#admin").removeClass("hidden");
}
else{
    $("#login").removeClass("hidden");
}
$("#logout").click(function(){
    localStorage.isAdmin = "false";
    localStorage.removeItem("token");
    location.replace("/");
})
$("#login").click(function(){
    location.replace("/login");
});

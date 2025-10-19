$(".dropdown-bar").click(function(){
    const p = $(this).parent()
    if ($(p).hasClass("open")){
        $(p).removeClass("open");
        $(p).children(".dropdown-contents").one("transitionend", function(){$(this).hide()});
        //$(this).find(".dropdown-contents").slideUp(200).hide();
    }
    else{
        $(p).children(".dropdown-contents").show();
        $(p).addClass("open");
    }
});
$(".dropdown-contents").hide();

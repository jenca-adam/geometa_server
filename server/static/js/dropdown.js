$(".dropdown-bar").click(function(){
    const p = $(this).parent()
    if ($(p).hasClass("open")){
                $(p).removeClass("open");
        $(p).children(".dropdown-contents").one("transitionend", function(){$(this).hide(); $(p).children(".dropdown-contents").children().addClass("hidden");
});
        //$(this).find(".dropdown-contents").slideUp(200).hide();
    }
    else{
        $(p).children(".dropdown-contents").children().removeClass("hidden");
        $(p).children(".dropdown-contents").show();
        $(p).addClass("open");
    }
});
$(".dropdown-contents").hide();

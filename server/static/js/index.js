function prepareEditMetaForm(id){
    const data = META_DATA[id];
    if(!data) return;
    $("#edit-meta-token").val(localStorage.token);
    $("#edit-meta-id").val(id);
    $("#edit-meta-title").val(data.title);
    $("#edit-meta-desc").val(data.description);
    $("#edit-meta-link").val(data.link);
    $("#edit-meta-current-image").attr("src", data.image);
    $("#edit-meta-export").attr("href", `/export_meta?id=${id}&format=mma`).attr("download",`geometa-export-${id}.json`);
}
function prepareViewMeta(id){
    const data = META_DATA[id];
    if(!data) return;
    $("#show-meta-title").text(data.title);
    $("#show-meta-desc").text(data.description);
    $("#show-meta-link").attr("href", data.link);
    $("#show-meta-current-image").attr("src", data.image);
    $("#show-meta-export").attr("href", `/export_meta?id=${id}&format=mma`).attr("download",`geometa-export-${id}.json`);
}
$(".export-button").click(function(){
    
});
$("#site").hide();
$(document).ready(() =>{
    $("#site").show();
    $(".tabs").tabs();
});
$(".meta").click(function(){
    console.log("click");
    if (localStorage.isAdmin=="true"){
    prepareEditMetaForm($(this).data("id"));
    $("#meta-edit-container").removeClass("hidden");
    }
    else{
        prepareViewMeta($(this).data("id"));
        $("#meta-show-container").removeClass("hidden");
    }

});
$("#edit-meta-image").change(function(){
    const files = $(this).prop('files');
    if(!files.length){
        return;
    }
    const file = files[0];
    var reader = new FileReader();
       reader.readAsDataURL(file);
       reader.onload = function () {
         $("#edit-meta-current-image").attr("src", reader.result);
       };
});
$("#edit-meta-open-link").click(function(){window.open($("#edit-meta-link").val())});
$("#edit-meta-close").click(function(){$("#meta-edit-container").addClass("hidden")});
$("#show-meta-close").click(function(){$("#meta-show-container").addClass("hidden")});
$("#edit-meta-submit").click(function(){
    const formData = new FormData($("#edit-meta-form")[0]);
    fetch("/api/edit_meta", {method:"POST", body:formData}).then((result)=>{
        result.json().then((json)=>{
            if (json.status!="ok"){
                $("#form-error").text(json.message);
            }
            else{
                location.reload();
            }
        });
    });
});

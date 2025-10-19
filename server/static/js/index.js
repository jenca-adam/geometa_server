function prepareEditMetaForm(id){
    const data = META_DATA[id];
    if(!data) return;
    $("#edit-meta-token").val(localStorage.token);
    $("#edit-meta-id").val(id);
    $("#edit-meta-title").val(data.title);
    $("#edit-meta-desc").val(data.description);
    $("#edit-meta-link").val(data.link);
    $("#edit-meta-current-image").attr("src", data.image);
}
if(!localStorage.token){
    location.replace("/login");
}
$("#site").hide();
$(document).ready(() =>{
    $("#site").show();
    $(".tabs").tabs();
});
$(".meta").click(function(){
    prepareEditMetaForm($(this).data("id"));
    $("#meta-edit-container").removeClass("hidden");
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

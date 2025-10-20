if (localStorage.isAdmin!="true"){
    location.replace("/login");
}
$(".tabs").tabs()
$("#global-export-submit").click(function(){
    const formData = new FormData($("#global-export-form")[0]);
    const reqParams = new URLSearchParams({"fmt":formData.get("format"), "token":localStorage.token});
    const url = "/api/export_all?" + reqParams.toString();
    fetch(url).then((response)=>{response.json().then((json)=>{
        if (json.status!="ok"){
            $("#form-error").text(json.message);
        }
        else{
            const blob = new Blob([JSON.stringify(json.data)], {type:"application/json"});
            const a = document.createElement("a");
            a.download = "geometa-export.json";
            a.href = URL.createObjectURL(blob);
            a.click();
        }
    })});
});

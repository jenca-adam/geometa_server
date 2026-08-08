function addTag(tagList, tagName, tagId){
    const tagEl = $("<li>", {class:"tag", "data-id":tagId})
    tagEl.text(tagName);
    tagEl.append($("<span>", {class:"iconify tag-remove", "data-icon":"mdi-trash"}));
    tagList.append(tagEl);
}
function hasTag(tagList, tagId){
    return !!tagList.find(`.tag[data-id=${tagId}]`).length;
}
function getTagIdArray(tagList){
    return tagList.find('.tag').map(function(){return parseInt($(this).data("id"))}).get();
}
$(document).on("click", ".tag-remove", function(){$(this).parent().remove()});
$(document).on("click", ".add-tag", function(){
    const tl = $(this).parent().parent().children(".taglist");
    console.log(tl);
    const option = $(this).parent().children(".tag-select")[0].selectedOptions[0];
    if (!hasTag(tl, option.value)){
        addTag(tl, option.innerText, option.value);
    }
});

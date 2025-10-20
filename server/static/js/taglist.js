function addTag(tagList, tagName, tagId){
    const tagEl = $("<li>", {class:"tag", "data-id":tagId})
    tagEl.text(tagName);
    tagEl.append($("<span>", {class:"iconify tag-remove", "data-icon":"mdi-trash"}));
    tagList.append(tagEl);
}

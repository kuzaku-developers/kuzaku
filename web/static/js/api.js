function save(guild_id, item, value) {
    var formData = new FormData();
    formData.append("item", item);
    formData.append("value", value);
    
    fetch(`/api/settings/change/${guild_id}`, {method: "POST", body: formData})
        .then(res => res.text())
        .then(res => {
            if(res == "done") console.log('SUCCESS! Setting saved successfully.');
            else console.log('Sorry, an error occured.');
    });
}
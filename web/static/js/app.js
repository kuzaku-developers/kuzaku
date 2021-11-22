function toast(message) {
    // Get the snackbar DIV
    var x = document.getElementById("snackbar");
    x.innerHTML = message;
    // Add the "show" class to DIV
    x.className = "show";
  
    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}


function save(guild_id, item, value) {
    var formData = new FormData();
    formData.append("item", item);
    formData.append("value", value);
    
    fetch(`/api/settings/change/${guild_id}`, {method: "POST", body: formData})
        .then(res => res.text())
        .then(res => {
            if(res == "done") toast('Настройки успешно изменены!');
            else toast('Произошла ошибка!');
    });
}
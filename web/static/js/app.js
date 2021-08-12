document.addEventListener('DOMContentLoaded', () => {
    var dropdownTriggers = document.querySelectorAll('.dropdown-trigger');
    M.Dropdown.init(dropdownTriggers, { constrainWidth: false });
});

function save(guild_id, item, value) {
    var formData = new FormData();
    formData.append("item", item);
    formData.append("value", value);
    
    fetch(`/api/settings/change/${guild_id}`, {method: "POST", body: formData})
        .then(res => res.text())
        .then(res => {
            if(res == "done") M.toast({html: 'SUCCESS! Setting saved successfully.'});
            else M.toast({html: 'Sorry, an error occured.'});
    });
}
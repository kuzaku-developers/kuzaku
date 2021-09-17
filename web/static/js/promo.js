function toast(message) {
    // Get the snackbar DIV
    var x = document.getElementById("snackbar");
    x.innerHTML = message;
    // Add the "show" class to DIV
    x.className = "show";
  
    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
  }

function use_promo(userid) {
    var formData = new FormData();
    formData.append("id", userid);
    if (document.getElementById("codeinput").value == 'sus') window.location.href = 'amogus';;
    formData.append("promocode", document.getElementById("codeinput").value);
    console.log(formData)
    fetch(`/api/v1/usecode`, {method: "POST", body: formData})
        .then(res => res.text())
        .then(res => {
            if(res == "activated") toast('Промокод успешно активирован!');
            else if(res == "notexist") toast('Такого промокода не существует.');
            else if(res == 'nouses') toast('У этого промокода не осталось использований!');
            else if (res == 'used') toast('Вы уже использовали данный промокод!');
    });
}


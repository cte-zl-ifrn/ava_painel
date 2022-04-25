var searchIcon = document.getElementsByClassName("search-box__icon")[0];
var searchBox = document.getElementsByClassName("search-box")[0];

searchIcon.addEventListener("click", activateSearch);

function activateSearch() {
    searchBox.classList.toggle("active");
}

function search() {
    var input, filter, cards, cardContainer, title, i;
    input = document.getElementById("searchbar");
    filter = input.value.toLowerCase();
    cardContainer = document.getElementById("couser");
    cards = cardContainer.getElementsByClassName("card");
    for (i = 0; i < cards.length; i++) {
        title = cards[i].querySelector(".card-title");
        if (title.innerText.toLowerCase().indexOf(filter) > -1) {
            cards[i].style.right = "";
        } else {
            cards[i].style.display = "none";
        }
    }
}
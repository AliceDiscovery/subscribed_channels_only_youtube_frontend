// implements search box functionality

const searchUrl = "/search/";

function performSearch() {
    var searchTerms = document.getElementById('searchInput').value;
    if (searchTerms.trim() !== "") {
        window.location.href = searchUrl + encodeURIComponent(searchTerms);
    }
}

document.getElementById('searchButton').addEventListener('click', performSearch);

document.getElementById('searchInput').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
    console.log('typed enter');
        event.preventDefault();
        performSearch();
    }
});

function editPlaceholder(id, html)
{
	fetch(html)
	    .then(response => response.text())
		.then(data => {
		  document.getElementById(id).innerHTML = data;
		});
}
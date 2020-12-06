let health = document.getElementsByClassName("health_scale");
[...health].forEach(el => {
	let num = parseInt(el.textContent);
	if(num >= 5 && num <= 6)
		el.style.backgroundColor = "yellow";
	else if(num >= 3 && num <= 4)
		el.style.backgroundColor = "orange";
	else if(num >= 0 && num <= 2)
		el.style.backgroundColor = "red";
});

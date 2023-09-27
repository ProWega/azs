function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
 
console.log("Hello");
sleep(2000).then(() => { 
	console.log("World!");
	const card = document.querySelector('div.card')
	console.log(card)
	card.onclick = function() {

  /*if (card.className == "card") {
    card.className = "card full";  
  } else {
    card.className = "card";
  }*/
}
});


/*
card.onclick = function() {
  alert('hi')
  if (card.className == "card") {
    card.className = "card full";  
  } else {
    card.className = "card";
  }
}
*/
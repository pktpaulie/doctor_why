/* class MyFooter extends HTMLElement {
  connectedCallback(){
    this.innerHTML = `
      <footer>
      @ 2023 Pauline Korukundo
      `
  }
}
customElements.define('my-footer', MyFooter)
 */
function hide(target){
  var target = document.getElementById(target);
  target.setAttribute("style", "display:none;");
}



window.setTimeout(function() {
    var element = document.querySelector('.flash');
    if (element) {
        element.classList.remove('flash');
    }
}, 5000);

var updateBtns = document.getElementsByClassName('update-cart')

for(var i=0; i<updateBtns.length; i++){
  updateBtns[i].addEventListener('click', function(){
    var productId = this.dataset.product
    var action = this.dataset.action
    console.log('USER:', user)
    if(user === 'AnonymouseUser'){
      console.log('Not logged in')
    }else{
      updateUserOrder(productId, action)
    }
  })
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
			}, 
			body:JSON.stringify({'itemId':itemId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    console.log('Data:', data)
		});
}

function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}


// Assign all elements
const demoId = document.getElementById('demo');
const demoClass = document.getElementsByClassName('demo');
const demoTag = document.getElementsByTagName('article');
const demoQuery = document.querySelector('#demo-query');
const demoQueryAll = document.querySelectorAll('.demo-query-all');

// Change border of ID demo to purple
demoId.style.border = '1px solid purple';

// Change border of class demo to orange
for (i = 0; i < demoClass.length; i++) {
  demoClass[i].style.border = '1px solid orange';
}

// Change border of tag demo to blue
for (i = 0; i < demoTag.length; i++) {
  demoTag[i].style.border = '1px solid blue';
}

// Change border of ID demo-query to red
demoQuery.style.border = '1px solid red';

// Change border of class query-all to green
demoQueryAll.forEach(query => {
  query.style.border = '1px solid green';
});

class MyFooter extends HTMLElement {
  connectedCallback(){
    this.innerHTML = `
      <footer>
      @ 2023 Pauline Korukundo
      `
  }
}
customElements.define('my-footer', MyFooter)

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


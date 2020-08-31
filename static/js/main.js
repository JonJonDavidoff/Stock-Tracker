function removeClass(elem, cl) {
	elem.forEach(el => {
		el.classList.remove(cl);
	})
}

var stockInp  = document.querySelector(".search_stock_inp");
var stockDropdown = document.querySelector(".search_stock_dropdown");

stockInp.addEventListener("keyup", function (e) {
  var v = this.value;

  if (v.length > 0) {
  	stockDropdown.style.display = "inline-block";
  	let stock_comp = document.querySelectorAll(".comp_content li");
  	//console.log(stock_comp);
  	stock_comp.forEach(comp => {
  		comp.style.display = "none";
  		let name = comp.dataset.company;
  		if (name.includes(v)) {
  			comp.style.display = "flex";
  		} 


  	})

  } else {
  	stockDropdown.style.display = "none";
  }

})

var chartToggle= document.querySelectorAll("[data-chartToggle]");
var chartFilterAll= document.querySelectorAll("[data-chartFilter]");

//console.log(chartFilter);

chartToggle.forEach(chart => {
	chart.addEventListener("click", function () {
		removeClass(chartToggle, "active");
		this.classList.add("active");
		var chart = this.dataset.charttoggle;
		removeClass(chartFilterAll, "active");

		chartFilterAll.forEach(ch => {
			var chkch = ch.dataset.chartfilter;
			if (chkch === chart) {
				ch.classList.add("active");
			}
		});

	})
})


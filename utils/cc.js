
// cookie and click value
var cookieBank = 0;
var cookieBankHTML = document.getElementById("cookieBank");

var cookie = document.getElementById("cookie");

var clickVal = 1;
var upClickValHTML = document.getElementById("upClickVal");
var upClickValP = document.getElementById("upClickValP");
var upClickVal = 2; // multiplies current click val with this val when upgraded
var upClickValCost = 50;

var printsmth = function(e){
    console.log("clicked button");
};
var updateCB = function (cookieBankValue){
    cookieBankHTML.innerHTML = "Cookies: " + cookieBank;
}

var addToCookieBank = function(cookies){
    cookieBank += cookies;
    console.log("Cookie bank: " + cookieBank);
    updateCB(cookieBank);
};

cookie.addEventListener('click', function() {addToCookieBank(clickVal);} );

// click
var upgradeClickVal = function(val){
    if (cookieBank - upClickValCost > 0){
	// take out cost of upgrade
	cookieBank -= upClickValCost;
	updateCB(cookieBank);
	// increase click val
	clickVal *= upClickVal;
	// increase upgrade cost
	upClickValCost *= 2;
	// update description
	upClickValP.innerHTML = "Cost: " + upClickValCost + " --- Upgrade Click Value to " + clickVal*upClickVal + " cps";
    }
};

upClickValHTML.addEventListener('click', function() { upgradeClickVal(upClickVal);});

// generator

var generatorfuntimes = function(gen, html){
    if (cookieBank-gen.cost >= 0){
	addToCookieBank(-gen.cost);
	gen.num += 1;
	gen.updateCost();
	setInterval(function(){
	    addToCookieBank(gen.cps);
	}, 1000);
	html.innerHTML = "Cost: " + Math.floor(gen.cost) + " --- Generates " + gen.cps + " cps. You have " + gen.num + " gen" + gen.id;
    }

}

class Generator {
    constructor(id, num, cost, cps){
	this.id = id;
	this.num = num;
	this.cost = cost;
	this.cps = cps;
    }
    updateCost(){
	this.cost *= 1.1;
    }

}
var gen0button = document.getElementById("gen0");
var gen0HTML = document.getElementById("gen0p");
var gen0 = new Generator(0,0, 100, 1);

gen0button.addEventListener('click', function() { generatorfuntimes(gen0, gen0HTML);})

var gen1button = document.getElementById("gen1");
var gen1HTML = document.getElementById("gen1p");
var gen1 = new Generator(1,0, 1100, 8);

gen1button.addEventListener('click', function() { generatorfuntimes(gen1, gen1NumHTML);})



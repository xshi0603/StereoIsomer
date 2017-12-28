
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
var buyGenerator = function(genID, cost, addtoCBVal, interval){
    if (cookieBank - cost > 0){
	addToCookieBank(-cost);
	var p = document.getElementById("gen"+genID+"Num");
	p.innerHTML += 1;
    }
};

var gen0 = document.getElementById("gen0");
var gen0Cost = 100;
var gen0NumHTML = document.getElementById("gen0Num");
var gen0Num = 0;
gen0.addEventListener('click', function() {
    if (cookieBank - gen0Cost >= 0){
	addToCookieBank(-gen0Cost);
	gen0Num += 1;
	setInterval(function() {
	    addToCookieBank(10);
	} ,1000);
	gen0NumHTML.innerHTML = "You have " + gen0Num + " gen0";
    }
});

var gen1 = document.getElementById("gen1");
var gen1Cost = 10000;
var gen1NumHTML = document.getElementById("gen1Num");
var gen1Num = 0;
gen1.addEventListener('click', function() {
    console.log("ckick lgen");
    if (cookieBank - gen1Cost >= 0){
	addToCookieBank(-gen1Cost);
	gen1Num += 1;
	setInterval(function() {
	    addToCookieBank(1000);
	} ,1000);
	gen1NumHTML.innerHTML = "You have " + gen1Num + " gen1";
    }
});



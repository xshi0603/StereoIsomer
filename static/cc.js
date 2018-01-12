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
    cookieBank += Math.ceil(cookies);
    console.log("Cookie bank: " + cookieBank);
    updateCB(cookieBank);
};

cookie.addEventListener('click', function() {
    addToCookieBank(clickVal);
});

// click upgrade
var upgradeClickVal = function(val){
    if (cookieBank - upClickValCost >= 0){
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
class Generator {
    constructor(id, num, cost, cps, upVal){
	this.id = id;
	this.num = num;
	this.cost = cost;
	this.cps = cps;
	this.upVal = upVal;
    }
    updateCost(){
	this.cost *= 1.1;
    }
    upgradeCPS(mult){
	this.cps *= mult;
	this.upVal = Math.floor(this.upVal*1.1);
    }
}

var updateHTML = function(gen, html){
    html.innerHTML = "Cost: " + Math.floor(gen.cost) + " --- Generates " + gen.cps + " cps. You have " + gen.num + " gen" + gen.id;
};

var generatorfuntimes = function(gen, html){
    if (cookieBank-gen.cost >= 0){
	addToCookieBank(-gen.cost);
	gen.num += 1;
	gen.updateCost();
	setInterval(function(){
	    addToCookieBank(gen.cps);
	}, 1000);
	updateHTML(gen, html);
    }
}

var gen0button = document.getElementById("gen0");
var gen0HTML = document.getElementById("gen0p");
var gen0 = new Generator(0,0, 100, 1, 100);
var up0 = document.getElementById("up0");

gen0button.addEventListener('click', function() { generatorfuntimes(gen0, gen0HTML);});
up0.addEventListener('click', function(){
    console.log("clicked up");
    if(cookieBank-gen0.upVal>=0){
	addToCookieBank(-gen0.upVal);
	gen0.upgradeCPS(2);
	updateHTML(gen0, gen0HTML);
	console.log("upVal: " + gen0.upVal);
    }
});
					  
var gen1button = document.getElementById("gen1");
var gen1HTML = document.getElementById("gen1p");
var gen1 = new Generator(1,0, 1100, 8, 1500);

gen1button.addEventListener('click', function() { generatorfuntimes(gen1, gen1HTML);});


//--------SAVING----------

var saving = function(e) {    
    
    var value2 = "hello";
    
    var values = {"username" : "insertuser",
		  "cookies" : cookieBank,
		  "cps" : "insertcps",
		  "gen0" : gen0.num,
		  "gen1" : gen1.num,
		  "clickVal" : clickVal,
		  //"generators" : {"gen0" : 1,
		  //		  "gen1" : 2 }, 
    }
    
    console.log(values);

    $.ajax({
	    url:'/save',
		type: 'POST',
		//processData : "false",
		//dataType: "json",
		data: $.param(values),
		sucess: function (d) {
		console.log(d);
		//console.log(JSON.parse(d));
		//d = JSON.parse(d);
		//document.getElementById('h2').innerHTML = d['uc'];
	    }
	});
    console.log('goodbye');
};

document.getElementById("save").addEventListener( 'click', saving );
//savebutton.addEventListener('click', function() { saving();});

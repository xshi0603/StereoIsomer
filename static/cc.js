// cookie and click value
var cookieBank = 0;
var cookieBankHTML = document.getElementById("cookieBank");

var cookie = document.getElementById("cookie");

var clickVal = 1;
var upClickValHTML = document.getElementById("upClickVal");
var upClickValP = document.getElementById("upClickValP");
var upClickVal = 2; // multiplies current click val with this val when upgraded
var upClickValCost = 50;
var upClickNum = 0; //amount of times upClick has been upgraded

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
	// increment counter
	upClickNum += 1;
    }
};

var upgradeClickVal2 = function(){//for loading

    // increase click val                                                                                                                                                     
    clickVal *= upClickVal;
    // increase upgrade cost                                                                                                                                                  
    upClickValCost *= 2;
    // update description                                                                                                                                                     
    upClickValP.innerHTML = "Cost: " + upClickValCost + " --- Upgrade Click Value to " + clickVal*upClickVal + " cps";
    // increment counter
    upClickNum += 1;
    
};

upClickValHTML.addEventListener('click', function() { upgradeClickVal(upClickVal);});

// generator
class Generator {
    constructor(id, num, cost, cps, upVal, upMult){
	this.id = id;
	this.num = num;
	this.cost = cost;
	this.cps = cps;
	this.upVal = upVal;
	this.upMult = upMult;
    }
    updateCost(){
	this.cost *= 1.1;
    }
    upgradeCPS(){
	this.cps = this.cps*this.upMult;
	this.upVal = Math.floor(this.upVal*2);
    }
}

var updateHTML = function(gen, genHTML, upHTML){
    genHTML.innerHTML = "Cost: " + Math.floor(gen.cost) + " --- Generates " + Math.round(gen.cps) + " cps. You have " + gen.num;
    upHTML.style.title = "Cost: " + gen.upVal + "--- Multiplier: " + gen.upMult;
};

var generatorfuntimes = function(gen, html, htmlup){
    if (cookieBank-gen.cost >= 0){
	addToCookieBank(-gen.cost);
	gen.num += 1;
	gen.updateCost();
	setInterval(function(){
		addToCookieBank(gen.cps);
	    }, 1000);
	updateHTML(gen, html, htmlup);
    }
};
    
var generatorfuntimes2 = function(gen, html, htmlup){

    gen.num += 1;
    gen.updateCost();
    setInterval(function(){
	    addToCookieBank(gen.cps);
	}, 1000);
    updateHTML(gen, html, htmlup);

};





//---- GENERATOR 0 ------
var gen0button = document.getElementById("gen0");
var gen0HTML = document.getElementById("gen0p");
var gen0Upgraded = 0;
var gen0 = new Generator(0,0, 100, 1, 500, 1.5);
var up0HTML = document.getElementById("up0");
var up0 = document.getElementById("up0");

gen0button.addEventListener('click', function() { generatorfuntimes(gen0, gen0HTML, up0HTML);});

up0.addEventListener('click', function(){
	console.log("clicked up");
	if(cookieBank-gen0.upVal>=0){
	    addToCookieBank(-gen0.upVal);
	    gen0.upgradeCPS();
	    gen0Upgraded += 1;
	    updateHTML(gen0, gen0HTML, up0HTML);
	    console.log("upVal: " + gen0.upVal + " cps: " + gen0.cps);
	}
    });

var upGen0 = function(){ //for loading
    gen0.upgradeCPS()
    gen0Upgraded += 1;
    updateHTML(gen0, gen0HTML, up0HTML);
}

//---- GENERATOR 1 ------
var gen1button = document.getElementById("gen1");
var gen1HTML = document.getElementById("gen1p");
var gen1Upgraded = 0;
var gen1 = new Generator(0,0, 1100, 8, 5000, 2);
var up1HTML = document.getElementById("up1p");
var up1 = document.getElementById("up1");

gen1button.addEventListener('click', function() { generatorfuntimes(gen1, gen1HTML, up1HTML);});

up1.addEventListener('click', function(){
	console.log("clicked up");
	if(cookieBank-gen1.upVal>=0){
	    addToCookieBank(-gen1.upVal);
	    gen1.upgradeCPS();
	    gen1Upgraded += 1;
	    updateHTML(gen1, gen1HTML, up1HTML);
	    console.log("upVal: " + gen1.upVal + " cps: " + gen1.cps);
	    
	}
    });

var upGen1 = function(){ //for loading                                                                                                                    
    gen1.upgradeCPS()
    gen1Upgraded += 1;
    updateHTML(gen1, gen1HTML, up1HTML);
}

//---- GENERATOR 2 ------ 

var gen2button = document.getElementById("gen2");
var gen2HTML = document.getElementById("gen2p");
var gen2Upgraded = 0;
var gen2 = new Generator(0,0, 12000, 47, 10000, 3);
var up2HTML = document.getElementById("up2p");
var up2 = document.getElementById("up2");
gen2button.addEventListener('click', function() { generatorfuntimes(gen2, gen2HTML, up2HTML);});

up2.addEventListener('click', function(){
	console.log("clicked up");
	if(cookieBank-gen2.upVal>=0){
	    addToCookieBank(-gen2.upVal);
	    gen2.upgradeCPS();
	    gen2Upgraded += 1;
	    updateHTML(gen2, gen2HTML, up2HTML);
	    console.log("upVal: " + gen2.upVal + " cps: " + gen2.cps);
	}
    });

var upGen2 = function(){ //for loading                                                                                                                                
    gen2.upgradeCPS()
    gen2Upgraded += 1;
    updateHTML(gen2, gen2HTML, up2HTML);
}

//-------LOADING----------                                                              
var username;

$.get("/getpythonuser", function(data) {
	console.log("LOADING");
	console.log("username");
        console.log($.parseJSON(data));
        username = $.parseJSON(data);
    });

$.get("/getpythoncookies", function(data) {
	console.log("cookies");
	console.log($.parseJSON(data));
	cookieBank = $.parseJSON(data);
	updateCB(0);
    });

$.get("/getpythongen0", function(data) {
	var gen0_num = $.parseJSON(data);
	console.log("gen0:");
	console.log(gen0_num);
	
	for (i = 0; i < gen0_num; i++) { 
	    generatorfuntimes2(gen0, gen0HTML, up0HTML);
	    console.log("upgraded 0");
	}
    });

$.get("/getpythongen1", function(data) {
        var gen1_num = $.parseJSON(data);
	console.log("gen1:");
        console.log(gen1_num);

        for (i = 0; i < gen1_num; i++) {
            generatorfuntimes2(gen1, gen1HTML, up1HTML);
            console.log("upgraded 1");
        }
    });

$.get("/getpythongen2", function(data) {
        var gen2_num = $.parseJSON(data);
	console.log("gen2:");
        console.log(gen2_num);

        for (i = 0; i < gen2_num; i++) {
            generatorfuntimes2(gen2, gen2HTML, up2HTML);
            console.log("upgraded 2");
        }
    });

$.get("/getpythonclick", function(data) {
        var click = $.parseJSON(data);
        console.log("click:");
        console.log(click);

        for (i = 0; i < click; i++) {
	    upgradeClickVal2();
            console.log("upgraded click");
        }
    });

$.get("/getpythonup0", function(data) {
        var up0L = $.parseJSON(data);
        console.log("up0L:");
        console.log(up0L);

        for (i = 0; i < up0L; i++) {
	    upGen0();
            console.log("upgraded gen0");
        }
    });

$.get("/getpythonup1", function(data) {
        var up1L = $.parseJSON(data);
        console.log("up1L:");
        console.log(up1L);

        for (i = 0; i < up1L; i++) {
            upGen1();
            console.log("upgraded gen1");
        }
    });

$.get("/getpythonup2", function(data) {
        var up2L = $.parseJSON(data);
        console.log("up2L:");
        console.log(up2L);

        for (i = 0; i < up2L; i++) {
            upGen2();
            console.log("upgraded gen2");
        }
    });

//gen0button.addEventListener('click', function() { generatorfuntimes(gen0, gen0HTML, up0HTML);});

//------------------------   

/*
var gen1button = document.getElementById("gen1");
var gen1HTML = document.getElementById("gen1p");
var gen1 = new Generator(1,0, 1100, 8, 2000);

gen1button.addEventListener('click', function() { generatorfuntimes(gen1, gen1HTML);});

var up1 = document.getElementById("up1");
up1.addEventListener('click', function(){
    console.log("clicked up");
    if(cookieBank-gen1.upVal>=0){
	addToCookieBank(-gen1.upVal);
	gen1.upgradeCPS(2);
	updateHTML(gen1, gen1HTML);
	console.log("upVal: " + gen1.upVal);
    }
});
*/

//--------SAVING----------

var saving = function(e) {    
    
    console.log("saving");
    
    var values = {"username" : username,
		  "cookies" : cookieBank,
		  "gen0" : gen0.num,
		  "gen1" : gen1.num,
		  "gen2" : gen2.num,
		  "clickNum" : upClickNum,
		  "gen0Up" : gen0Upgraded,
		  "gen1Up" : gen1Upgraded,
		  "gen2Up" : gen2Upgraded
    };
    
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
    console.log('saving done');
};

document.getElementById("save").addEventListener( 'click', saving );
//savebutton.addEventListener('click', function() { saving();});

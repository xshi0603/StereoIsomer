var cookieBank = 0;
//Cookie
var addToCookieBank = function(cookies){
    cookieBank += cookies;
};

var cookie = document.getElementById("cookie");
cookie.addEventListener("onclick", function(e){ addToCookieBank(10); });


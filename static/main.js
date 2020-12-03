var strongRegexPass = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
var mediumRegexPass = new RegExp("^(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{6,})");
var noteTitleRegex = new RegExp("^[a-zA-Z0-9]{4,10}$");

password_strength = function(value) {
    if(strongRegexPass.test(value)) {
        console.log("Strong");
        document.getElementById('register_submit').disabled = false;
    } else if(mediumRegexPass.test(value)) {
        console.log("Medium");
        document.getElementById('register_submit').disabled = false;
    } else {
        console.log("Weak");
        document.getElementById('register_submit').disabled = true;
    }
};

password_match = function(value) {
    if(document.getElementById("password").value === value) {
        console.log("Match");
        document.getElementById('register_submit').disabled = false;
    } else {
        document.getElementById('register_submit').disabled = true;
        console.log("Not Match");
    }
};




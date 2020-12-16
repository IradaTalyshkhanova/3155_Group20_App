var strongRegexPass = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})"); // at least 8 char, one lowercase, one uppercase, one number, one special char
var mediumRegexPass = new RegExp("^(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{6,})"); // at least 6 char, one lowercase, one uppercase, one number
var noteTitleRegex = new RegExp("^[a-zA-Z0-9]{4,10}$"); // only letters and numbers
var budgetRegex = /^(?<=^| )\d+(\.\d+)?(?=$| )|(?<=^| )\.\d+(?=$| )$/; // only digits and one period, no letters

password_strength = function(value) {
    if(strongRegexPass.test(value)) { // check if strong password
        console.log("Strong");
        pass_err = "Passwords is strong strength.";
        document.getElementById('register_submit').disabled = false || password_match(pass_err);
    } else if(mediumRegexPass.test(value)) { // check if med password
        console.log("Medium");
        pass_err = "Passwords is medium strength.";
        document.getElementById('register_submit').disabled = false || password_match(pass_err);
    } else { // else is weak
        console.log("Weak");
        pass_err = "Passwords is too weak and/or do not match";
        document.getElementById("error_reg").innerHTML = pass_err;
        document.getElementById('register_submit').disabled = true;
    }
};

password_match = function(pass_err) {
    if(document.getElementById("password").value === document.getElementById("confirm_password").value) { // does password and confirm password field match
        console.log("Match");
        document.getElementById("error_reg").innerHTML = pass_err;
        return false;
    } else {
        console.log("Not Match");
        document.getElementById("error_reg").innerHTML = "Passwords do not match";
        return true;
    }
};

// not used
title_pass = function(value) {
    if(document.getElementById("").value === value) {
        console.log("Match");
        document.getElementById('note_submit').disabled = false;
    } else {
        document.getElementById('note_submit').disabled = true;
        console.log("Title must only have letters");
    }
};

todo_field = function(value) {
    if (value.length > 0) { // input must not be empty
        document.getElementById('submit_todo').disabled = false;
    } else {
        document.getElementById('submit_todo').disabled = true;
    }
}

budget_field_check = function(value) {
    console.log(value)
    if(budgetRegex.test(value)) { // check if budget is dollar amount, i.e. 1.02 or 03.83
        console.log("passed")
        document.getElementById('budget_submit').disabled = false;
    } else {
        console.log("fail")
        document.getElementById('budget_submit').disabled = true;
    }
}
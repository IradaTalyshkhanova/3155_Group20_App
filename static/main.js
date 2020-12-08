var strongRegexPass = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
var mediumRegexPass = new RegExp("^(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{6,})");
var noteTitleRegex = new RegExp("^[a-zA-Z0-9]{4,10}$");

password_strength = function(value) {
    if(strongRegexPass.test(value)) {
        console.log("Strong");
        pass_err = "Passwords is strong strength.";
        document.getElementById('register_submit').disabled = false || password_match(pass_err) || all_fields_complete();
    } else if(mediumRegexPass.test(value)) {
        console.log("Medium");
        pass_err = "Passwords is medium strength.";
        document.getElementById('register_submit').disabled = false || password_match(pass_err) || all_fields_complete();
    } else {
        console.log("Weak");
        pass_err = "Passwords is too weak.";
        document.getElementById('register_submit').disabled = true || password_match(pass_err) || all_fields_complete();
    }
};

password_match = function(pass_err) {
    if(document.getElementById("password").value === document.getElementById("confirm_password").value) {
        console.log("Match");
        document.getElementById("error_reg").innerHTML = pass_err + "";
        return false;
    } else {
        console.log("Not Match");
        document.getElementById("error_reg").innerHTML = pass_err + " Passwords do not match";
        return true;
    }
};

all_fields_complete = function() {
    if(document.getElementById("email").value.length > 0 &&
        document.getElementById("name").value.length > 0 &&
        document.getElementById("password").value.length > 0 &&
        document.getElementById("confirm_password").value.length > 0) {
        console.log("Done!");
        return false;
    } else {
        console.log("Not done!");
        return true;
    }
}

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
    if (value.length > 0) {
        document.getElementById('submit_todo').disabled = false;
    } else {
        document.getElementById('submit_todo').disabled = true;
    }
}

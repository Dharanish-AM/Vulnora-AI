function login() {
    var password = "supersecretpassword12345"; // VULNERABLE: Hardcoded secret
    var userInput = document.getElementById("input").value;
    
    // VULNERABLE: Eval
    eval(userInput);
    
    // VULNERABLE: InnerHTML
    document.getElementById("output").innerHTML = userInput;
}

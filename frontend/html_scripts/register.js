let email = document.getElementById("emailInput")
let password = document.getElementById("passwordInput")
let registerForm = document.getElementById("registerForm")
let submitButton = document.getElementById("submitButton")
let name = document.getElementById("nameInput")
let lastName = document.getElementById("lastNameInput")


registerForm.addEventListener("submit", event => {
    event.preventDefault()

    let json_register_body = JSON.stringify({user_body: {email: email.value, password: password.value, name: name.value, last_name: lastName.value}})
    let json_login_body = JSON.stringify({user_body: {email: email.value, password: password.value}})

    fetch("http://localhost:8000/register", {method: "POST", credentials: "include", body: json_register_body}).then(response => {
        console.log(response)
        if (response.ok) {
            fetch("http://localhost:8000/create_token", {method: "POST", credentials: "include", body: json_login_body}).then(response => {
                if (response.ok) {
                    window.location.href = "../html_pages/main_page.html"
                }
                else {
                    console.log("Произошла ошибка, попробуйте ещё раз")
                }
            })
        }
    })
})
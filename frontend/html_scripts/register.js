import {json_fetch} from "./funcs.js";

let email = document.getElementById("emailInput")
let password = document.getElementById("passwordInput")
let name = document.getElementById("nameInput")
let lastName = document.getElementById("lastNameInput")
let registerForm = document.getElementById("registerForm")


registerForm.addEventListener("submit", event => {
    event.preventDefault()

    let user_data = {
        name: name.value,
        last_name: lastName.value,
        email: email.value,
        password: password.value
    }

    void json_fetch("http://localhost:8000/register", {
        method: "POST",
        credentials: "include",
        body: user_data
    })
    json_fetch("http://localhost:8000/create_token", {method: "POST", body: user_data}).then(response => {
        if (response.ok) {
            window.location.href = "../html_pages/main_page.html"
        }
        else alert("Произошла ошибка при создании токена! Попробуйте ещё раз")
    })})

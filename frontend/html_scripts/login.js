import {json_fetch} from "./funcs.js";


export const BaseUrl = "http://localhost:8000"


async function isLogined() {
    fetch(`${BaseUrl}/initPage`, {credentials: "include"}).then(resp => {
        if (resp.ok) {
            window.location.href = "../html_pages/main_page.html"
        }
        else console.log(resp)
    })
}

await isLogined()

let email = document.getElementById("emailInput")
let password = document.getElementById("passwordInput")
let submitButton = document.getElementById("submitButton")
let loginForm = document.getElementById("loginForm")

loginForm.addEventListener("submit", loginUser)


async function loginUser(event) {
    event.preventDefault()
    let user_data = {
        email: email.value,
        password: password.value
    }
    email.value = ''
    password.value = ''
    json_fetch(`${BaseUrl}/create_token`, {method: "POST", body: user_data}).then(response => {
        console.log(response)
        if (response.ok) {
            window.location.href = "../html_pages/main_page.html"
        }
        else {
            console.log("Authentication error. Try again")
        }
    })
}




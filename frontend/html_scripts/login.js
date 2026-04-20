
let BaseUrl = "http://localhost:8000"


async function isLogined() {
    fetch(`${BaseUrl}/initPage`, {credentials: "include"}).then(resp => {
        if (resp.ok) {
            window.location.href = "../html_pages/main_page.html"
        }
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
    let user_json_body = JSON.stringify({user_body: {email: email.value, password: password.value}})
    email.value = ''
    password.value = ''
    fetch(`${BaseUrl}/create_token`, {method: "POST", body: user_json_body, credentials: "include"}).then(response => {
        console.log(response)
        if (response.ok) {
            window.location.href = "../html_pages/main_page.html"
        }
        else {
            console.log("Authentication error. Try again")
        }
    })
}




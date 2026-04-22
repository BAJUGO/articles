import {json_fetch} from "./funcs.js";


document.getElementById("addArticleButton").addEventListener("click", add_article)

async function add_article(event) {
    event.preventDefault()
    let title = document.getElementById("articleTitle")
    let mainText = document.getElementById("articleMainText")
    if (title.value === '' || mainText.value === '') {
        alert("Try to fill all necessary field")
        return
    }

    let body = JSON.stringify({article_body: {title: title.value, main_text: mainText.value}})

    json_fetch(`http://localhost:8000/articles/add_article`, {body: body, method: "POST", credentials: "include",}).then(response => {
        console.log(response)
    })


}
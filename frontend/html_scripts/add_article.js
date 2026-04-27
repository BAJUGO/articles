import {json_fetch} from "./funcs.js";

async function add_article(event) {
    event.preventDefault()
    let title = document.getElementById("articleTitle").value
    let mainText = document.getElementById("articleMainText").value
    if (title === '' || mainText === '') {
        alert("Try to fill all necessary field")
        return
    }
    let articleData = {
        title: title,
        main_text: mainText
    }

    json_fetch(`http://localhost:8000/articles/add_article`, {
        body: articleData,
        method: "POST",
    }).then(response => {
        console.log(response)
    })
}

document.getElementById("addArticleButton").addEventListener("click", add_article)
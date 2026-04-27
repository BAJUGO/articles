import {json_fetch} from "./funcs.js";

async function update_article(event) {
    event.preventDefault()
    let id = document.getElementById("article_id").value
    let title = document.getElementById("article_title").value
    let main_text = document.getElementById("article_main_text").value

    json_fetch(`http://localhost:8000/articles/${id}`, {method: "PATCH",
        body: {
  ...(title && { title }),
  ...(main_text && { main_text })
}
    }).then(response => {
        console.log(response)
    })
}

document.getElementById("update_article_button").addEventListener("click", update_article)
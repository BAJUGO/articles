import {mapping} from "./funcs_getter.js";

document.getElementById("deleteUserForm").addEventListener("submit", delete_user)
document.getElementById("deleteArticleForm").addEventListener("submit", delete_article)


async function delete_object(event, object_type, object_id) {
    event.preventDefault()
    fetch(`http://localhost:8000/${mapping[object_type]}/${object_id}`, {method: "DELETE", credentials: "include"}).then(response => {
        console.log(response)
    })

}

async function delete_user(event) {
    let user_id = document.getElementById("userIdInput")
    await delete_object(event, "user", user_id.value)
    user_id.value = ''
}

async function delete_article(event) {
    let article_id = document.getElementById("articleIdInput")
    await delete_object(event, "article", article_id.value)
    article_id.value = ''
}
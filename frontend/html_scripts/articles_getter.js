import {initPage, json_fetch} from "./funcs.js";

void initPage()

const renderArticle = (article) => `
    <div class="article-card">
        <h4>${article.title}</h4>
        <p>${article.main_text || ''}</p>
        <small>User ID: ${article.user_id}</small><br>
        <small>ID: ${article.id}</small>
    </div>  
`;


async function send_get_request(where_to_send, container) {
    const data = await json_fetch(`http://localhost:8000/${where_to_send}`)
    console.log(data)
    container.innerHTML = data.items.map(renderArticle).join(`<hr>`);
}


async function get_article_by_id(event) {
    event.preventDefault()
    const id = document.getElementById("article_id").value;
    const container = document.getElementById("ul_1")
    void send_get_request(`articles/${id}`, container)
}

async function get_articles(event) {
    event.preventDefault()
    const container = document.getElementById("ul_2")
    void send_get_request("articles/get_articles", container)
}

async function get_articles_of_user(event) {
    event.preventDefault()
    const id = document.getElementById("user_id").value
    const container = document.getElementById("ul_3")
    void send_get_request(`articles/user/${id}`, container)
}


let form_article_by_id = document.getElementById("form_article_by_id")
form_article_by_id.addEventListener('submit', get_article_by_id)


let form_all_articles = document.getElementById("form_all_articles")
form_all_articles.addEventListener('submit', get_articles)


let form_articles_by_user = document.getElementById("form_articles_by_user")
form_articles_by_user.addEventListener('submit', get_articles_of_user)

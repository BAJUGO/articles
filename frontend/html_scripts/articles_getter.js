import {initPage, json_fetch} from "./funcs.js";
import {get_all_articles_of_user, get_all_objects, get_object_by_id} from "./funcs_getter.js";

void initPage()


const renderArticle = (article) => `
    <div class="article-card">
        <h4>${article.title}</h4>
        <p>${article.main_text || ''}</p>
        <small>ID: ${article.id}</small>
    </div>  
`;


async function get_article_by_id(event) {
    event.preventDefault()
    const id = document.getElementById("article_id").value;
    const container = document.getElementById("ul_1")

    try {
        const data = await json_fetch(`http://localhost:8000/articles/${id}`, {credentials: "include"});
        container.innerHTML = data.items.map(renderArticle).join('<hr>');
    } catch (err) {
        console.log(err)
        container.innerHTML = `<li class="error">Ошибка загрузки</li>`;
    }
}



let form_article_by_id = document.getElementById("form_article_by_id")
form_article_by_id.addEventListener('submit', get_article_by_id)

let form_all_articles = document.getElementById("form_all_articles")
form_all_articles.addEventListener('submit', event => {
    void get_all_objects("article", event)
})

let form_articles_by_user = document.getElementById("form_articles_by_user")
form_articles_by_user.addEventListener('submit', event => {
    void get_all_articles_of_user(event)
})
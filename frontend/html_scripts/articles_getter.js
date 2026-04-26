import {initPage} from "./funcs.js";
import {get_all_articles_of_user, get_all_objects, get_object_by_id} from "./funcs_getter.js";

void initPage()



let form_article_by_id = document.getElementById("form_article_by_id")
form_article_by_id.addEventListener('submit', event => {
    void get_object_by_id("article", event)
})

let form_all_articles = document.getElementById("form_all_articles")
form_all_articles.addEventListener('submit', event => {
    void get_all_objects("article", event)
})

let form_articles_by_user = document.getElementById("form_articles_by_user")
form_articles_by_user.addEventListener('submit', event => {
    void get_all_articles_of_user(event)
})
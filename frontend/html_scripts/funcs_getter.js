import {create_articles_of_user_on_page, create_content_on_page, initPage, json_fetch} from "./funcs.js";


export const mapping = {
    article: "articles",
    user: "users",
}

export async function get_object_by_id(object_type, event){
    event.preventDefault()
    document.getElementById('ul_1').innerHTML = ''
    let id = document.getElementById(`${object_type}_id`)
    void initPage()
    json_fetch(`http://localhost:8000/${mapping[object_type]}/${id.value}`, {
        method: "GET",
        credentials: "include"
    }).then(response => {
        create_content_on_page(response, "ul_1")
        console.log(response)

    })
    id.value = ''
}


export async function get_all_objects(object_type, event) {
    event.preventDefault()
    document.getElementById('ul_2').innerHTML = ''
    const path = mapping[object_type]
    void initPage()
    json_fetch(`http://localhost:8000/${path}/get_${path}`, {
        method: "GET",
        credentials: "include"
    }).then(response => {
        console.log(response)
        for (let object_number in response) {
            create_content_on_page(response[object_number], "ul_2")
        }
    })
}


export async function get_all_articles_of_user(event) {
    event.preventDefault()
    let id = document.getElementById("user_id");
    document.getElementById('ul_3').innerHTML = '';
    void initPage();
    json_fetch(`http://localhost:8000/articles/user/${id.value}`, {
        method: "GET",
        credentials: "include"
    }).then(response => {
        create_articles_of_user_on_page(response, "ul_3")
    });
    id.value = '';
}
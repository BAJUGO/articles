import {mapping} from "./funcs_getter.js";


const article_attrs = ["title", "main_text"]
const user_attrs = ["name", "last_name", "password"]


export async function update_article(event) {
    await update_object(event, "article", article_attrs)
}

export async function update_user(event) {
    await update_object(event, "user", user_attrs)
}


export async function update_object(event, object_type, list_of_attrs) {
    event.preventDefault()
    let id_el = document.getElementById(`${object_type}_id`)
    let id = id_el.valueAsNumber
    const attrs = list_of_attrs
    let future_body = {}
    for (let attr in attrs) {
        let el = document.getElementById(`${object_type}_${attrs[attr]}`)
        if (!el.value) {
            continue
        }
        let attr_value
        if (el.type === "number") attr_value = el.valueAsNumber
        else attr_value = el.value
        future_body[attrs[attr]] = attr_value
    }
    console.log(future_body)
    let body_json = JSON.stringify({"update_body": future_body})
    fetch(`http://localhost:8000/${mapping[object_type]}/${id}`, {method: "PATCH", credentials: "include", body: body_json}).then(response => {
        console.log(response)
    })

}
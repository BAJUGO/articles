
export async function json_fetch(url, options = {}) {
    let resp = await fetch(url, {
        ...options,
        body: options.form ?? options.body,
        method: options.method ?? "GET"
    })
    return resp.json()
}


export function create_content_on_page(value, id_of_ul) {
    let ul_to_changed = document.getElementById(id_of_ul)
    let li_to_add = document.createElement("li")
    let main_element = document.createElement("h1")
    let sub_ul = document.createElement("ul")
    if (value["detail"]) {
        main_element.innerText = "This object wasn't found"
        sub_ul.innerHTML = value["detail"]
        li_to_add.appendChild(main_element)
        li_to_add.appendChild(sub_ul)
        ul_to_changed.appendChild(li_to_add)
        return
    }

    main_element.innerText = value["title"] ?? value["name"]
    li_to_add.appendChild(main_element)

    for (let obj in value) {
        if (obj === "title" || obj === "name") continue;
        let object = document.createElement("li")
        object.innerText = `${obj} - ${value[obj]}`
        sub_ul.appendChild(object)
    }
    li_to_add.appendChild(sub_ul)
    ul_to_changed.appendChild(li_to_add)
    ul_to_changed.appendChild(document.createElement("hr"))


}


export async function initPage() {
    let response = await fetch("http://localhost:8000/initPage", {credentials: "include"})
    if (!response.ok) {
        window.location.href = "../index.html"
    }
}



export async function unloginUser(event) {
    event.preventDefault()
    fetch(`http://localhost:8000/delete_cookies`, {credentials: "include"}).then(response => {
        if (response.ok) {
            window.location.href = "../index.html"
        }
    })
}

export async function includeUnlogin() {
    void initPage()
    document.getElementById("unlogin").addEventListener('click', (event) => {
        unloginUser(event)
    })
}
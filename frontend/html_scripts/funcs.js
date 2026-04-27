
export async function json_fetch(url, options = {}) {
    let resp = await fetch(url, {
        ...options,
        body: options.form ?? options.body,
        method: options.method ?? "GET"
    })
    return resp.json()
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
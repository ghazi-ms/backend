loadXMLFeed = () => {

    const url = "";
    fetch(url).then(response => response.text()).then(data => {

        let parser = new DOMParser();
        let xml = parser.parseFromString(data, "");

        console.log(xml);
    })
}

document.addEventListener("DOMContentLoaded",loadXMLFeed);

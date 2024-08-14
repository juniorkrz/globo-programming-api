// Put this in your console to generate channels.json
// You must be on a page that contains Globo programming
// Example: https://redeglobo.globo.com/globobrasilia/programacao

function checkUrl() {
    return window.url && window.url.startsWith('https://redeglobo.globo.com/')
}

function exportJSON(jsonObject, fileName) {
    const jsonString = JSON.stringify(jsonObject, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    console.log(`File ${fileName} saved in your downloads folder!`)
}

function normalizeName(name) {
    return name
        .toLowerCase()
        .trim()
        .normalize('NFD')
        .replaceAll(/[\u0300-\u036f]/g, '')
        .replaceAll(' ', '-')
}

function getUrls() {
    document.getElementById('dropdown-summary__button').click();
    const xpath = '//li[@aria-describedby="dropdown-option-description"]//a';
    const elements = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

    const channels = {};

    let counter = 0;
    for (let i = 0; i < elements.snapshotLength; i++) {
        const element = elements.snapshotItem(i)
        const name = element.lastElementChild.textContent.trim();
        const code = normalizeName(element.lastElementChild.textContent);
        const category = normalizeName(element.firstElementChild.textContent);
        const categoryName = element.firstElementChild.textContent.trim();
        const url = element.getAttribute('href').slice(0, -1);
        if (categoryName && category && code && url) {
            if (!channels[category]) {
                channels[category] = {
                    name: categoryName,
                    channels: {}
                }
            }

            channels[category].channels[code] = {
                name,
                url
            };

            counter++;
        }
    }

    document.getElementById('dropdown-summary__button').click();
    console.log('Channels found: ', counter);
    return channels;
}

if (checkUrl()) {
    const channels = getUrls();
    exportJSON(channels, 'channels.json');
} else {
    console.log('You are not on a Globo programming page!')
    console.log('You must be on a page that contains Globo programming')
    console.log('Example: https://redeglobo.globo.com/globobrasilia/programacao')
}

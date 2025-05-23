// Crawl the DOM for all text nodes
function getAllTextNodes(node = document.body, conditional = n => true) {
    if (!node) return [];
    if (conditional(node) === false) return [];
    // If parent node,
    if (node.hasChildNodes()) {
        // Recursively collect all decendents.
        const nodes = [];
        for (let childNode of node.childNodes) {
            nodes.push(...getAllTextNodes(childNode, conditional));
        }
        return nodes;
    }
    // Else if text node, return self in an array.
    else if (node.nodeType === Node.TEXT_NODE) return [node];
    // Else return an empty array.
    else return [];
}

function formatLink(node) {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    const arr = node.textContent.split(urlRegex).map(i => {
        if (!urlRegex.test(i)) return i;
        const a = document.createElement('a');
        a.href = i;
        a.textContent = i;
        a.target = '_blank';
        a.rel = 'noreferrer';
        return a;
    });
    node.replaceWith(...arr);
}

function formatLinks(rootNode = document.body) {
    // Filter links from text nodes.
    const conditional = (node) => node.tagName !== 'A';
    // Get all text nodes.
    const nodes = getAllTextNodes(rootNode, conditional);
    // Create links from text nodes.
    nodes.forEach(formatLink);
}

document.addEventListener("DOMContentLoaded", () => formatLinks());


        (function () {
            const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
            const nodes = [];
            let node;
            while ((node = walker.nextNode())) {
                const parent = node.parentElement;
                if (!parent || parent.closest('script, style, noscript, .vc-ampersand') || !node.nodeValue.includes('&')) continue;
                nodes.push(node);
            }
            nodes.forEach((textNode) => {
                const fragment = document.createDocumentFragment();
                textNode.nodeValue.split('&').forEach((part, index, parts) => {
                    if (index) {
                        const ampersand = document.createElement('span');
                        ampersand.className = 'vc-ampersand';
                        ampersand.textContent = '&';
                        fragment.appendChild(ampersand);
                    }
                    if (part) fragment.appendChild(document.createTextNode(part));
                });
                textNode.parentNode.replaceChild(fragment, textNode);
            });
        }());


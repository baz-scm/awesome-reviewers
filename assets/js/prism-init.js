// Prism.js initialization for Awesome Reviewers
// This script initializes Prism syntax highlighting after the DOM is loaded

document.addEventListener('DOMContentLoaded', function() {
    if (typeof Prism !== 'undefined') {
        Prism.highlightAll();

        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            const codeBlocks = node.querySelectorAll('pre code');
                            codeBlocks.forEach(function(block) {
                                Prism.highlightElement(block);
                            });
                        }
                    });
                }
            });
        });

        const drawerContent = document.getElementById('drawer-content');
        if (drawerContent) {
            observer.observe(drawerContent, {
                childList: true,
                subtree: true
            });
        }
    } else {
        console.warn('Prism.js not loaded - syntax highlighting unavailable');
    }
});

function highlightNewContent(container) {
    if (typeof Prism !== 'undefined' && container) {
        const codeBlocks = container.querySelectorAll('pre code');
        codeBlocks.forEach(function(block) {
            Prism.highlightElement(block);
        });
    }
}

window.highlightNewContent = highlightNewContent;

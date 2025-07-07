// Highlight.js initialization for Awesome Reviewers
// This script initializes syntax highlighting after the DOM is loaded

document.addEventListener('DOMContentLoaded', function() {
    // Wait for hljs to be available (loaded from CDN)
    if (typeof hljs !== 'undefined') {
        // Configure highlight.js
        hljs.configure({
            // Don't highlight on load automatically - we'll do it manually
            noHighlightRe: /^no-highlight$/i,
            languageDetectRe: /\blang(?:uage)?-([\w-]+)\b/i,
            classPrefix: 'hljs-',
            // Languages we support
            languages: ['c', 'cpp', 'csharp', 'css', 'html', 'json', 'yaml', 'toml', 
                       'python', 'javascript', 'typescript', 'jsx', 'tsx', 'go', 
                       'java', 'kotlin', 'php', 'ruby', 'rust']
        });

        // Highlight all code blocks
        hljs.highlightAll();
        
        // Also highlight any dynamically loaded content (for the drawer)
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            // Find any new code blocks and highlight them
                            const codeBlocks = node.querySelectorAll('pre code, code:not(.hljs)');
                            codeBlocks.forEach(function(block) {
                                if (!block.classList.contains('hljs')) {
                                    hljs.highlightElement(block);
                                }
                            });
                        }
                    });
                }
            });
        });

        // Observe the drawer content for dynamic highlighting
        const drawerContent = document.getElementById('drawer-content');
        if (drawerContent) {
            observer.observe(drawerContent, {
                childList: true,
                subtree: true
            });
        }

        console.log('Highlight.js initialized with language support for:', 
                   ['C', 'C++', 'C#', 'CSS', 'HTML', 'JSON', 'YAML', 'TOML', 
                    'Python', 'JavaScript', 'TypeScript', 'JSX', 'TSX', 'Go', 
                    'Java', 'Kotlin', 'PHP', 'Ruby', 'Rust']);
    } else {
        console.warn('Highlight.js not loaded - syntax highlighting unavailable');
    }
});

// Function to manually highlight new content (useful for dynamic content)
function highlightNewContent(container) {
    if (typeof hljs !== 'undefined' && container) {
        const codeBlocks = container.querySelectorAll('pre code, code:not(.hljs)');
        codeBlocks.forEach(function(block) {
            if (!block.classList.contains('hljs')) {
                hljs.highlightElement(block);
            }
        });
    }
}

// Export for use in other scripts if needed
window.highlightNewContent = highlightNewContent;
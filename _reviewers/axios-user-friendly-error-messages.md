---
title: "User-friendly error messages"
description: "Error messages should be concise and clearly communicate what went wrong without unnecessary verbosity. When implementing error handling, maintain consistent code style and organize related operations logically within appropriate blocks."
repository: "axios/axios"
label: "Error Handling"
language: "Html"
comments_count: 2
repository_stars: 107000
---

Error messages should be concise and clearly communicate what went wrong without unnecessary verbosity. When implementing error handling, maintain consistent code style and organize related operations logically within appropriate blocks.

Example:
```javascript
// Instead of this:
try {
    data = JSON.parse(data);
} catch (e) {
    output.innerHTML = "Error : Is blank or not JSON string type. Please check your data.";
    data = null;
}

// Do this:
try {
    data = JSON.parse(data);
    
    // Keep related operations in the try block
    axios.post('/post/server', data)
        .then(function (res) {
            output.className = 'container';
            output.innerHTML = res.data;
        })
        .catch(function (err) {
            output.className = 'container text-danger';
            output.innerHTML = err.message;
        });
} catch (e) {
    // Use concise, clear error messages
    output.innerHTML = "Error: empty string or invalid JSON";
    output.className = 'container text-danger';
}
```

This approach improves user experience by providing clear feedback while maintaining clean, logically structured code with consistent styling.
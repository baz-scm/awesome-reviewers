---
title: Escape XML content securely
description: 'Always use proper XML entity escaping instead of CDATA blocks when embedding
  XML-like content within XML documents. CDATA sections can be vulnerable to XML injection
  attacks if the content isn''t properly validated or controlled. '
repository: RooCodeInc/Roo-Code
label: Security
language: Xml
comments_count: 1
repository_stars: 17288
---

Always use proper XML entity escaping instead of CDATA blocks when embedding XML-like content within XML documents. CDATA sections can be vulnerable to XML injection attacks if the content isn't properly validated or controlled. 

For example, instead of:
```xml
<tool_use><![CDATA[
<update_todo_list>
<todos>
  [ ] First item
  [ ] Second item
</todos>
</update_todo_list>
]]></tool_use>
```

Use properly escaped XML entities:
```xml
<tool_use>
  &lt;update_todo_list&gt;
    &lt;todos&gt;
      [ ] First item
      [ ] Second item
    &lt;/todos&gt;
  &lt;/update_todo_list&gt;
</tool_use>
```

This practice prevents XML injection vulnerabilities that could allow attackers to manipulate XML processing, potentially leading to data exposure, unauthorized access, or other security breaches in systems that parse and process your XML documents.
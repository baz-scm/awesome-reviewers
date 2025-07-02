---
title: Defensive null checking
description: Always perform explicit null/undefined checks before accessing properties
  or using values that could be null or undefined. Use strict equality checks rather
  than relying on JavaScript's truthy/falsy evaluation which can lead to subtle bugs.
repository: aws/aws-sdk-js
label: Null Handling
language: Javascript
comments_count: 7
repository_stars: 7628
---

Always perform explicit null/undefined checks before accessing properties or using values that could be null or undefined. Use strict equality checks rather than relying on JavaScript's truthy/falsy evaluation which can lead to subtle bugs.

Common patterns to adopt:
1. Check objects before accessing their properties:
   ```javascript
   // Bad:
   if (error.code === 'AuthorizationHeaderMalformed') { /* ... */ }
   
   // Good:
   if (error && error.code === 'AuthorizationHeaderMalformed') { /* ... */ }
   ```

2. Be careful with array index checks:
   ```javascript
   // Bad - indexOf returns 0 for first item which is falsy:
   if (list.indexOf(member)) { return true; }
   
   // Good:
   if (list.indexOf(member) >= 0) { return true; }
   ```

3. Use typeof checks before accessing browser/environment-specific objects:
   ```javascript
   // Bad:
   return window.localStorage !== null;
   
   // Good:
   return AWS.util.isBrowser() && window.localStorage !== null && typeof window.localStorage === 'object';
   ```

4. Provide defaults for parameters that could be undefined:
   ```javascript
   // Bad:
   function handleParams(params) {
     params.property = 'value'; // Fails if params is null/undefined
   }
   
   // Good:
   function handleParams(params) {
     params = params || {};
     params.property = 'value';
   }
   ```

5. Use type checks for numeric values instead of truthy checks:
   ```javascript
   // Bad - fails for zero values:
   if (params.$waiter.delay) {
     this.config.delay = params.$waiter.delay;
   }
   
   // Good:
   if (typeof params.$waiter.delay === 'number') {
     this.config.delay = params.$waiter.delay;
   }
   ```

Consistent null checking prevents the most common class of runtime errors and produces more predictable code.


[
  {
    "discussion_id": "1132762746",
    "pr_number": 4365,
    "pr_file": "lib/maintenance_mode_message.js",
    "created_at": "2023-03-10T18:51:40+00:00",
    "commented_code": "* require('aws-sdk/lib/maintenance_mode_message').suppress = true;\n */\nfunction emitWarning() {\n  if (typeof process !== 'undefined')",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "1132762746",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 4365,
        "pr_file": "lib/maintenance_mode_message.js",
        "discussion_id": "1132762746",
        "commented_code": "@@ -14,10 +14,19 @@ module.exports = {\n  * require('aws-sdk/lib/maintenance_mode_message').suppress = true;\n  */\n function emitWarning() {\n+  if (typeof process !== 'undefined')",
        "comment_created_at": "2023-03-10T18:51:40+00:00",
        "comment_author": "trivikr",
        "comment_body": "Check for process being undefined\r\n```suggestion\r\n  if (typeof process === 'undefined')\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "43063573",
    "pr_number": 697,
    "pr_file": "lib/services/s3.js",
    "created_at": "2015-10-26T22:38:51+00:00",
    "commented_code": "return true;\n    } else if (error && error.code === 'RequestTimeout') {\n      return true;\n    } else if (error.code === 'AuthorizationHeaderMalformed' &&",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "43063573",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 697,
        "pr_file": "lib/services/s3.js",
        "discussion_id": "43063573",
        "commented_code": "@@ -272,6 +272,10 @@ AWS.util.update(AWS.S3.prototype, {\n       return true;\n     } else if (error && error.code === 'RequestTimeout') {\n       return true;\n+    } else if (error.code === 'AuthorizationHeaderMalformed' &&",
        "comment_created_at": "2015-10-26T22:38:51+00:00",
        "comment_author": "chrisradek",
        "comment_body": "Just to be safe, can you also add a check that error exists, similar to the conditional before this one?\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "85010899",
    "pr_number": 1189,
    "pr_file": "scripts/lib/ts-generator.js",
    "created_at": "2016-10-25T22:00:14+00:00",
    "commented_code": "var fs = require('fs');\nvar path = require('path');\n\nvar CUSTOM_CONFIG_ENUMS = {\n    DUALSTACK: {\n        FILE_NAME: 'config_use_dualstack',\n        INTERFACE: 'UseDualstackConfigOptions'\n    }\n};\n\nfunction TSGenerator(options) {\n    this._sdkRootDir = options.SdkRootDirectory || process.cwd();\n    this._apiRootDir = path.join(this._sdkRootDir, 'apis');\n    this._metadataPath = path.join(this._apiRootDir, 'metadata.json');\n    this._clientsDir = path.join(this._sdkRootDir, 'clients');\n    this.metadata = null;\n    this.typings = {};\n    this.fillApiModelFileNames(this._apiRootDir);\n}\n\n/**\n * Loads the AWS SDK metadata.json file.\n */\nTSGenerator.prototype.loadMetadata = function loadMetadata() {\n    var metadataFile = fs.readFileSync(this._metadataPath);\n    this.metadata = JSON.parse(metadataFile);\n    return this.metadata;\n};\n\n/**\n * Modifies metadata to include api model filenames.\n */\nTSGenerator.prototype.fillApiModelFileNames = function fillApiModelFileNames(apisPath) {\n    var modelPaths = fs.readdirSync(apisPath);\n    if (!this.metadata) {\n        this.loadMetadata();\n    }\n    var metadata = this.metadata;\n\n    // sort paths so latest versions appear first\n    modelPaths = modelPaths.sort(function sort(a, b) {\n        if (a < b) {\n            return 1;\n        } else if (a > b) {\n            return -1;\n        } else {\n            return 0;\n        }\n    });\n\n    // Only get latest version of models\n    var foundModels = Object.create(null);\n    modelPaths.forEach(function(modelFileName) {\n        var match = modelFileName.match(/^(.+)(-[\\d]{4}-[\\d]{2}-[\\d]{2})\\.normal\\.json$/i);\n        if (match) {\n            var model = match[1];\n            if (!foundModels[model]) {\n                foundModels[model] = modelFileName;\n            }\n        }\n    });\n\n    // now update the metadata\n    var keys = Object.keys(metadata);\n    keys.forEach(function(key) {\n        var modelName = metadata[key].prefix || key;\n        metadata[key].api_path = foundModels[modelName];\n        // find waiters file\n        var baseName = foundModels[modelName].split('.')[0];\n        if (modelPaths.indexOf(baseName + '.waiters2.json') >= 0) {\n            metadata[key].waiters_path = baseName + '.waiters2.json';\n        }\n    });\n};\n\n/**\n * Generates the file containing DocumentClient interfaces.\n */\nTSGenerator.prototype.generateDocumentClientInterfaces = function generateDocumentClientInterfaces() {\n    var self = this;\n    // get the dynamodb model\n    var dynamodbModel = this.loadServiceApi('dynamodb');\n    var code = '';\n    // include node reference\n    code += '///<reference types=\"node\" />\\n';\n    // generate shapes\n    var modelShapes = dynamodbModel.shapes;\n    // iterate over each shape\n    var shapeKeys = Object.keys(modelShapes);\n    shapeKeys.forEach(function (shapeKey) {\n        var modelShape = modelShapes[shapeKey];\n        // ignore exceptions\n        if (modelShape.exception) {\n            return;\n        }\n        // overwrite AttributeValue\n        if (shapeKey === 'AttributeValue') {\n            code += self.generateDocString('A JavaScript object or native type.');\n            code += 'export type ' + shapeKey + ' = any;\\n';\n            return;\n        }\n        code += self.generateTypingsFromShape(shapeKey, modelShape);\n    });\n\n    // write file:\n    this.writeTypingsFile('document_client_interfaces', path.join(this._sdkRootDir, 'lib', 'dynamodb'), code);\n};\n\n/**\n * Returns a service model based on the serviceIdentifier.\n */\nTSGenerator.prototype.loadServiceApi = function loadServiceApi(serviceIdentifier) {\n    // first, find the correct identifier\n    var metadata = this.metadata;\n    var serviceFilePath = path.join(this._apiRootDir, metadata[serviceIdentifier].api_path);\n    var serviceModelFile = fs.readFileSync(serviceFilePath);\n    var serviceModel = JSON.parse(serviceModelFile);\n    // load waiters file if it exists\n    var waiterFilePath;\n    if (metadata[serviceIdentifier].waiters_path) {\n        waiterFilePath = path.join(this._apiRootDir, metadata[serviceIdentifier].waiters_path);\n        var waiterModelFile = fs.readFileSync(waiterFilePath);\n        var waiterModel = JSON.parse(waiterModelFile);\n        serviceModel.waiters = waiterModel.waiters;\n    }\n\n    return serviceModel;\n};\n\n/**\n * Determines if a member is required by checking for it in a list.\n */\nTSGenerator.prototype.checkRequired = function checkRequired(list, member) {\n    if (list.indexOf(member)) {\n        return true;\n    }\n    return false;\n};\n\n/**\n * Generates whitespace based on the count.\n */\nTSGenerator.prototype.tabs = function tabs(count) {\n    var code = '';\n    for (var i = 0; i < count; i++) {\n        code += '  ';\n    }\n    return code;\n};\n\n/**\n * Transforms documentation string to a more readable format.\n */\nTSGenerator.prototype.transformDocumentation = function transformDocumentation(documentation) {\n    if (!documentation) {\n        return '';\n    }\n    documentation = documentation.replace(/<(?:.|\\n)*?>/gm, '');\n    documentation = documentation.replace(/\\*\\//g, '*');\n    return documentation;\n};\n\n/**\n * Returns a doc string based on the supplied documentation.\n * Also tabs the doc string if a count is provided.\n */\nTSGenerator.prototype.generateDocString = function generateDocString(documentation, tabCount) {\n    tabCount = tabCount || 0;\n    var code = '';\n    code += this.tabs(tabCount) + '/**\\n';\n    code += this.tabs(tabCount) + ' * ' + this.transformDocumentation(documentation) + '\\n';\n    code += this.tabs(tabCount) + ' */\\n';\n    return code;\n};\n\n/**\n * Returns an array of custom configuration options based on a service identiffier.\n * Custom configuration options are determined by checking the metadata.json file.\n */\nTSGenerator.prototype.generateCustomConfigFromMetadata = function generateCustomConfigFromMetadata(serviceIdentifier) {\n    // some services have additional configuration options that are defined in the metadata.json file\n    // i.e. dualstackAvailable = useDualstack\n    // create reference to custom options\n    var customConfigurations = [];\n    var serviceMetadata = this.metadata[serviceIdentifier];\n    // loop through metadata members\n    for (var memberName in serviceMetadata) {\n        if (!serviceMetadata.hasOwnProperty(memberName)) {\n            continue;\n        }\n        var memberValue = serviceMetadata[memberName];\n        // check configs\n        switch (memberName) {\n            case 'dualstackAvailable':\n                customConfigurations.push(CUSTOM_CONFIG_ENUMS.DUALSTACK);\n                break;\n        }\n    }\n\n    return customConfigurations;\n};\n\n/**\n * Generates a type or interface based on the shape.\n */\nTSGenerator.prototype.generateTypingsFromShape = function generateTypingsFromShape(shapeKey, shape, tabCount) {\n    // some shapes shouldn't be generated if they are javascript primitives\n    if (['string', 'boolean', 'number', 'Date', 'Blob'].indexOf(shapeKey) >= 0) {\n        return '';\n    }\n    var self = this;\n    var code = '';\n    tabCount = tabCount || 0;\n    var tabs = this.tabs;\n    var type = shape.type;\n    if (type === 'structure') {\n        code += tabs(tabCount) + 'export interface ' + shapeKey + ' {\\n';\n        var members = shape.members;\n        // cycle through members\n        var memberKeys = Object.keys(members);\n        memberKeys.forEach(function(memberKey) {\n            // docs\n            var member = members[memberKey];\n            if (member.documentation) {\n                code += self.generateDocString(member.documentation, tabCount + 1);\n            }\n            var required = self.checkRequired(shape.required || [], memberKey) ? '?' : '';",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "85010899",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1189,
        "pr_file": "scripts/lib/ts-generator.js",
        "discussion_id": "85010899",
        "commented_code": "@@ -0,0 +1,437 @@\n+var fs = require('fs');\n+var path = require('path');\n+\n+var CUSTOM_CONFIG_ENUMS = {\n+    DUALSTACK: {\n+        FILE_NAME: 'config_use_dualstack',\n+        INTERFACE: 'UseDualstackConfigOptions'\n+    }\n+};\n+\n+function TSGenerator(options) {\n+    this._sdkRootDir = options.SdkRootDirectory || process.cwd();\n+    this._apiRootDir = path.join(this._sdkRootDir, 'apis');\n+    this._metadataPath = path.join(this._apiRootDir, 'metadata.json');\n+    this._clientsDir = path.join(this._sdkRootDir, 'clients');\n+    this.metadata = null;\n+    this.typings = {};\n+    this.fillApiModelFileNames(this._apiRootDir);\n+}\n+\n+/**\n+ * Loads the AWS SDK metadata.json file.\n+ */\n+TSGenerator.prototype.loadMetadata = function loadMetadata() {\n+    var metadataFile = fs.readFileSync(this._metadataPath);\n+    this.metadata = JSON.parse(metadataFile);\n+    return this.metadata;\n+};\n+\n+/**\n+ * Modifies metadata to include api model filenames.\n+ */\n+TSGenerator.prototype.fillApiModelFileNames = function fillApiModelFileNames(apisPath) {\n+    var modelPaths = fs.readdirSync(apisPath);\n+    if (!this.metadata) {\n+        this.loadMetadata();\n+    }\n+    var metadata = this.metadata;\n+\n+    // sort paths so latest versions appear first\n+    modelPaths = modelPaths.sort(function sort(a, b) {\n+        if (a < b) {\n+            return 1;\n+        } else if (a > b) {\n+            return -1;\n+        } else {\n+            return 0;\n+        }\n+    });\n+\n+    // Only get latest version of models\n+    var foundModels = Object.create(null);\n+    modelPaths.forEach(function(modelFileName) {\n+        var match = modelFileName.match(/^(.+)(-[\\d]{4}-[\\d]{2}-[\\d]{2})\\.normal\\.json$/i);\n+        if (match) {\n+            var model = match[1];\n+            if (!foundModels[model]) {\n+                foundModels[model] = modelFileName;\n+            }\n+        }\n+    });\n+\n+    // now update the metadata\n+    var keys = Object.keys(metadata);\n+    keys.forEach(function(key) {\n+        var modelName = metadata[key].prefix || key;\n+        metadata[key].api_path = foundModels[modelName];\n+        // find waiters file\n+        var baseName = foundModels[modelName].split('.')[0];\n+        if (modelPaths.indexOf(baseName + '.waiters2.json') >= 0) {\n+            metadata[key].waiters_path = baseName + '.waiters2.json';\n+        }\n+    });\n+};\n+\n+/**\n+ * Generates the file containing DocumentClient interfaces.\n+ */\n+TSGenerator.prototype.generateDocumentClientInterfaces = function generateDocumentClientInterfaces() {\n+    var self = this;\n+    // get the dynamodb model\n+    var dynamodbModel = this.loadServiceApi('dynamodb');\n+    var code = '';\n+    // include node reference\n+    code += '///<reference types=\"node\" />\\n';\n+    // generate shapes\n+    var modelShapes = dynamodbModel.shapes;\n+    // iterate over each shape\n+    var shapeKeys = Object.keys(modelShapes);\n+    shapeKeys.forEach(function (shapeKey) {\n+        var modelShape = modelShapes[shapeKey];\n+        // ignore exceptions\n+        if (modelShape.exception) {\n+            return;\n+        }\n+        // overwrite AttributeValue\n+        if (shapeKey === 'AttributeValue') {\n+            code += self.generateDocString('A JavaScript object or native type.');\n+            code += 'export type ' + shapeKey + ' = any;\\n';\n+            return;\n+        }\n+        code += self.generateTypingsFromShape(shapeKey, modelShape);\n+    });\n+\n+    // write file:\n+    this.writeTypingsFile('document_client_interfaces', path.join(this._sdkRootDir, 'lib', 'dynamodb'), code);\n+};\n+\n+/**\n+ * Returns a service model based on the serviceIdentifier.\n+ */\n+TSGenerator.prototype.loadServiceApi = function loadServiceApi(serviceIdentifier) {\n+    // first, find the correct identifier\n+    var metadata = this.metadata;\n+    var serviceFilePath = path.join(this._apiRootDir, metadata[serviceIdentifier].api_path);\n+    var serviceModelFile = fs.readFileSync(serviceFilePath);\n+    var serviceModel = JSON.parse(serviceModelFile);\n+    // load waiters file if it exists\n+    var waiterFilePath;\n+    if (metadata[serviceIdentifier].waiters_path) {\n+        waiterFilePath = path.join(this._apiRootDir, metadata[serviceIdentifier].waiters_path);\n+        var waiterModelFile = fs.readFileSync(waiterFilePath);\n+        var waiterModel = JSON.parse(waiterModelFile);\n+        serviceModel.waiters = waiterModel.waiters;\n+    }\n+\n+    return serviceModel;\n+};\n+\n+/**\n+ * Determines if a member is required by checking for it in a list.\n+ */\n+TSGenerator.prototype.checkRequired = function checkRequired(list, member) {\n+    if (list.indexOf(member)) {\n+        return true;\n+    }\n+    return false;\n+};\n+\n+/**\n+ * Generates whitespace based on the count.\n+ */\n+TSGenerator.prototype.tabs = function tabs(count) {\n+    var code = '';\n+    for (var i = 0; i < count; i++) {\n+        code += '  ';\n+    }\n+    return code;\n+};\n+\n+/**\n+ * Transforms documentation string to a more readable format.\n+ */\n+TSGenerator.prototype.transformDocumentation = function transformDocumentation(documentation) {\n+    if (!documentation) {\n+        return '';\n+    }\n+    documentation = documentation.replace(/<(?:.|\\n)*?>/gm, '');\n+    documentation = documentation.replace(/\\*\\//g, '*');\n+    return documentation;\n+};\n+\n+/**\n+ * Returns a doc string based on the supplied documentation.\n+ * Also tabs the doc string if a count is provided.\n+ */\n+TSGenerator.prototype.generateDocString = function generateDocString(documentation, tabCount) {\n+    tabCount = tabCount || 0;\n+    var code = '';\n+    code += this.tabs(tabCount) + '/**\\n';\n+    code += this.tabs(tabCount) + ' * ' + this.transformDocumentation(documentation) + '\\n';\n+    code += this.tabs(tabCount) + ' */\\n';\n+    return code;\n+};\n+\n+/**\n+ * Returns an array of custom configuration options based on a service identiffier.\n+ * Custom configuration options are determined by checking the metadata.json file.\n+ */\n+TSGenerator.prototype.generateCustomConfigFromMetadata = function generateCustomConfigFromMetadata(serviceIdentifier) {\n+    // some services have additional configuration options that are defined in the metadata.json file\n+    // i.e. dualstackAvailable = useDualstack\n+    // create reference to custom options\n+    var customConfigurations = [];\n+    var serviceMetadata = this.metadata[serviceIdentifier];\n+    // loop through metadata members\n+    for (var memberName in serviceMetadata) {\n+        if (!serviceMetadata.hasOwnProperty(memberName)) {\n+            continue;\n+        }\n+        var memberValue = serviceMetadata[memberName];\n+        // check configs\n+        switch (memberName) {\n+            case 'dualstackAvailable':\n+                customConfigurations.push(CUSTOM_CONFIG_ENUMS.DUALSTACK);\n+                break;\n+        }\n+    }\n+\n+    return customConfigurations;\n+};\n+\n+/**\n+ * Generates a type or interface based on the shape.\n+ */\n+TSGenerator.prototype.generateTypingsFromShape = function generateTypingsFromShape(shapeKey, shape, tabCount) {\n+    // some shapes shouldn't be generated if they are javascript primitives\n+    if (['string', 'boolean', 'number', 'Date', 'Blob'].indexOf(shapeKey) >= 0) {\n+        return '';\n+    }\n+    var self = this;\n+    var code = '';\n+    tabCount = tabCount || 0;\n+    var tabs = this.tabs;\n+    var type = shape.type;\n+    if (type === 'structure') {\n+        code += tabs(tabCount) + 'export interface ' + shapeKey + ' {\\n';\n+        var members = shape.members;\n+        // cycle through members\n+        var memberKeys = Object.keys(members);\n+        memberKeys.forEach(function(memberKey) {\n+            // docs\n+            var member = members[memberKey];\n+            if (member.documentation) {\n+                code += self.generateDocString(member.documentation, tabCount + 1);\n+            }\n+            var required = self.checkRequired(shape.required || [], memberKey) ? '?' : '';",
        "comment_created_at": "2016-10-25T22:00:14+00:00",
        "comment_author": "LiuJoyceC",
        "comment_body": "If `checkRequired` is supposed to return true when the member is required, then this should be switched.\n`self.checkRequired(shape.required || [], memberKey) ? '' : '?'`\n",
        "pr_file_module": null
      },
      {
        "comment_id": "85435739",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1189,
        "pr_file": "scripts/lib/ts-generator.js",
        "discussion_id": "85010899",
        "commented_code": "@@ -0,0 +1,437 @@\n+var fs = require('fs');\n+var path = require('path');\n+\n+var CUSTOM_CONFIG_ENUMS = {\n+    DUALSTACK: {\n+        FILE_NAME: 'config_use_dualstack',\n+        INTERFACE: 'UseDualstackConfigOptions'\n+    }\n+};\n+\n+function TSGenerator(options) {\n+    this._sdkRootDir = options.SdkRootDirectory || process.cwd();\n+    this._apiRootDir = path.join(this._sdkRootDir, 'apis');\n+    this._metadataPath = path.join(this._apiRootDir, 'metadata.json');\n+    this._clientsDir = path.join(this._sdkRootDir, 'clients');\n+    this.metadata = null;\n+    this.typings = {};\n+    this.fillApiModelFileNames(this._apiRootDir);\n+}\n+\n+/**\n+ * Loads the AWS SDK metadata.json file.\n+ */\n+TSGenerator.prototype.loadMetadata = function loadMetadata() {\n+    var metadataFile = fs.readFileSync(this._metadataPath);\n+    this.metadata = JSON.parse(metadataFile);\n+    return this.metadata;\n+};\n+\n+/**\n+ * Modifies metadata to include api model filenames.\n+ */\n+TSGenerator.prototype.fillApiModelFileNames = function fillApiModelFileNames(apisPath) {\n+    var modelPaths = fs.readdirSync(apisPath);\n+    if (!this.metadata) {\n+        this.loadMetadata();\n+    }\n+    var metadata = this.metadata;\n+\n+    // sort paths so latest versions appear first\n+    modelPaths = modelPaths.sort(function sort(a, b) {\n+        if (a < b) {\n+            return 1;\n+        } else if (a > b) {\n+            return -1;\n+        } else {\n+            return 0;\n+        }\n+    });\n+\n+    // Only get latest version of models\n+    var foundModels = Object.create(null);\n+    modelPaths.forEach(function(modelFileName) {\n+        var match = modelFileName.match(/^(.+)(-[\\d]{4}-[\\d]{2}-[\\d]{2})\\.normal\\.json$/i);\n+        if (match) {\n+            var model = match[1];\n+            if (!foundModels[model]) {\n+                foundModels[model] = modelFileName;\n+            }\n+        }\n+    });\n+\n+    // now update the metadata\n+    var keys = Object.keys(metadata);\n+    keys.forEach(function(key) {\n+        var modelName = metadata[key].prefix || key;\n+        metadata[key].api_path = foundModels[modelName];\n+        // find waiters file\n+        var baseName = foundModels[modelName].split('.')[0];\n+        if (modelPaths.indexOf(baseName + '.waiters2.json') >= 0) {\n+            metadata[key].waiters_path = baseName + '.waiters2.json';\n+        }\n+    });\n+};\n+\n+/**\n+ * Generates the file containing DocumentClient interfaces.\n+ */\n+TSGenerator.prototype.generateDocumentClientInterfaces = function generateDocumentClientInterfaces() {\n+    var self = this;\n+    // get the dynamodb model\n+    var dynamodbModel = this.loadServiceApi('dynamodb');\n+    var code = '';\n+    // include node reference\n+    code += '///<reference types=\"node\" />\\n';\n+    // generate shapes\n+    var modelShapes = dynamodbModel.shapes;\n+    // iterate over each shape\n+    var shapeKeys = Object.keys(modelShapes);\n+    shapeKeys.forEach(function (shapeKey) {\n+        var modelShape = modelShapes[shapeKey];\n+        // ignore exceptions\n+        if (modelShape.exception) {\n+            return;\n+        }\n+        // overwrite AttributeValue\n+        if (shapeKey === 'AttributeValue') {\n+            code += self.generateDocString('A JavaScript object or native type.');\n+            code += 'export type ' + shapeKey + ' = any;\\n';\n+            return;\n+        }\n+        code += self.generateTypingsFromShape(shapeKey, modelShape);\n+    });\n+\n+    // write file:\n+    this.writeTypingsFile('document_client_interfaces', path.join(this._sdkRootDir, 'lib', 'dynamodb'), code);\n+};\n+\n+/**\n+ * Returns a service model based on the serviceIdentifier.\n+ */\n+TSGenerator.prototype.loadServiceApi = function loadServiceApi(serviceIdentifier) {\n+    // first, find the correct identifier\n+    var metadata = this.metadata;\n+    var serviceFilePath = path.join(this._apiRootDir, metadata[serviceIdentifier].api_path);\n+    var serviceModelFile = fs.readFileSync(serviceFilePath);\n+    var serviceModel = JSON.parse(serviceModelFile);\n+    // load waiters file if it exists\n+    var waiterFilePath;\n+    if (metadata[serviceIdentifier].waiters_path) {\n+        waiterFilePath = path.join(this._apiRootDir, metadata[serviceIdentifier].waiters_path);\n+        var waiterModelFile = fs.readFileSync(waiterFilePath);\n+        var waiterModel = JSON.parse(waiterModelFile);\n+        serviceModel.waiters = waiterModel.waiters;\n+    }\n+\n+    return serviceModel;\n+};\n+\n+/**\n+ * Determines if a member is required by checking for it in a list.\n+ */\n+TSGenerator.prototype.checkRequired = function checkRequired(list, member) {\n+    if (list.indexOf(member)) {\n+        return true;\n+    }\n+    return false;\n+};\n+\n+/**\n+ * Generates whitespace based on the count.\n+ */\n+TSGenerator.prototype.tabs = function tabs(count) {\n+    var code = '';\n+    for (var i = 0; i < count; i++) {\n+        code += '  ';\n+    }\n+    return code;\n+};\n+\n+/**\n+ * Transforms documentation string to a more readable format.\n+ */\n+TSGenerator.prototype.transformDocumentation = function transformDocumentation(documentation) {\n+    if (!documentation) {\n+        return '';\n+    }\n+    documentation = documentation.replace(/<(?:.|\\n)*?>/gm, '');\n+    documentation = documentation.replace(/\\*\\//g, '*');\n+    return documentation;\n+};\n+\n+/**\n+ * Returns a doc string based on the supplied documentation.\n+ * Also tabs the doc string if a count is provided.\n+ */\n+TSGenerator.prototype.generateDocString = function generateDocString(documentation, tabCount) {\n+    tabCount = tabCount || 0;\n+    var code = '';\n+    code += this.tabs(tabCount) + '/**\\n';\n+    code += this.tabs(tabCount) + ' * ' + this.transformDocumentation(documentation) + '\\n';\n+    code += this.tabs(tabCount) + ' */\\n';\n+    return code;\n+};\n+\n+/**\n+ * Returns an array of custom configuration options based on a service identiffier.\n+ * Custom configuration options are determined by checking the metadata.json file.\n+ */\n+TSGenerator.prototype.generateCustomConfigFromMetadata = function generateCustomConfigFromMetadata(serviceIdentifier) {\n+    // some services have additional configuration options that are defined in the metadata.json file\n+    // i.e. dualstackAvailable = useDualstack\n+    // create reference to custom options\n+    var customConfigurations = [];\n+    var serviceMetadata = this.metadata[serviceIdentifier];\n+    // loop through metadata members\n+    for (var memberName in serviceMetadata) {\n+        if (!serviceMetadata.hasOwnProperty(memberName)) {\n+            continue;\n+        }\n+        var memberValue = serviceMetadata[memberName];\n+        // check configs\n+        switch (memberName) {\n+            case 'dualstackAvailable':\n+                customConfigurations.push(CUSTOM_CONFIG_ENUMS.DUALSTACK);\n+                break;\n+        }\n+    }\n+\n+    return customConfigurations;\n+};\n+\n+/**\n+ * Generates a type or interface based on the shape.\n+ */\n+TSGenerator.prototype.generateTypingsFromShape = function generateTypingsFromShape(shapeKey, shape, tabCount) {\n+    // some shapes shouldn't be generated if they are javascript primitives\n+    if (['string', 'boolean', 'number', 'Date', 'Blob'].indexOf(shapeKey) >= 0) {\n+        return '';\n+    }\n+    var self = this;\n+    var code = '';\n+    tabCount = tabCount || 0;\n+    var tabs = this.tabs;\n+    var type = shape.type;\n+    if (type === 'structure') {\n+        code += tabs(tabCount) + 'export interface ' + shapeKey + ' {\\n';\n+        var members = shape.members;\n+        // cycle through members\n+        var memberKeys = Object.keys(members);\n+        memberKeys.forEach(function(memberKey) {\n+            // docs\n+            var member = members[memberKey];\n+            if (member.documentation) {\n+                code += self.generateDocString(member.documentation, tabCount + 1);\n+            }\n+            var required = self.checkRequired(shape.required || [], memberKey) ? '?' : '';",
        "comment_created_at": "2016-10-27T21:54:33+00:00",
        "comment_author": "chrisradek",
        "comment_body": "Thanks, didn't catch this due to the mistake above.\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "90351124",
    "pr_number": 1245,
    "pr_file": "lib/credentials/cognito_identity_credentials.js",
    "created_at": "2016-11-30T23:15:44+00:00",
    "commented_code": "*/\n  storage: (function() {\n    try {\n      return AWS.util.isBrowser() && window.localStorage !== null && typeof window.localStorage === 'object' ?",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "90351124",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1245,
        "pr_file": "lib/credentials/cognito_identity_credentials.js",
        "discussion_id": "90351124",
        "commented_code": "@@ -331,8 +331,10 @@ AWS.CognitoIdentityCredentials = AWS.util.inherit(AWS.Credentials, {\n    */\n   storage: (function() {\n     try {\n-      return AWS.util.isBrowser() && window.localStorage !== null && typeof window.localStorage === 'object' ?",
        "comment_created_at": "2016-11-30T23:15:44+00:00",
        "comment_author": "chrisradek",
        "comment_body": "Can you keep the `AWS.util.isBrowser() && window.localStorage !== null` checks at the top of the try block? As it is, this will always throw an error in node.js (and possibly some 'browser' environments like electron). I know the catch block should handle this case, but I'd like to avoid throwing an error if we can predict it.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "51147005",
    "pr_number": 888,
    "pr_file": "lib/services/s3.js",
    "created_at": "2016-01-28T16:34:54+00:00",
    "commented_code": "// This chunk of code will set the location constraint param based\n    // on the region (when possible), but it will not override a passed-in\n    // location constraint.\n    if (!params) params = {};\n    if (typeof params === 'function') {\n      callback = params;\n      params = {};\n    }",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "51147005",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 888,
        "pr_file": "lib/services/s3.js",
        "discussion_id": "51147005",
        "commented_code": "@@ -411,7 +409,10 @@ AWS.util.update(AWS.S3.prototype, {\n     // This chunk of code will set the location constraint param based\n     // on the region (when possible), but it will not override a passed-in\n     // location constraint.\n-    if (!params) params = {};\n+    if (typeof params === 'function') {\n+      callback = params;\n+      params = {};\n+    }",
        "comment_created_at": "2016-01-28T16:34:54+00:00",
        "comment_author": "chrisradek",
        "comment_body": "It might be useful to add one more check after the if block to set params equal to itself or an empty object to protect us in the unlikely event someone passes in a value like `null`. Imagine this would be a rare edge case but we do this already for other operations.\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "107256817",
    "pr_number": 1405,
    "pr_file": "lib/resource_waiter.js",
    "created_at": "2017-03-21T19:46:42+00:00",
    "commented_code": "callback = params; params = undefined;\n    }\n\n    if (params && params.$waiter) {\n      if (params.$waiter.delay) {\n        this.config.delay = params.$waiter.delay;",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "107256817",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1405,
        "pr_file": "lib/resource_waiter.js",
        "discussion_id": "107256817",
        "commented_code": "@@ -136,6 +136,16 @@ AWS.ResourceWaiter = inherit({\n       callback = params; params = undefined;\n     }\n \n+    if (params && params.$waiter) {\n+      if (params.$waiter.delay) {\n+        this.config.delay = params.$waiter.delay;",
        "comment_created_at": "2017-03-21T19:46:42+00:00",
        "comment_author": "chrisradek",
        "comment_body": "Just in case someone wants to enter `0`, maybe use a `typeof x === 'number'` check instead.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "147590167",
    "pr_number": 1782,
    "pr_file": "lib/event_listeners.js",
    "created_at": "2017-10-29T18:37:50+00:00",
    "commented_code": "var req = resp.request;\n      var logger = req.service.config.logger;\n      if (!logger) return;\n      function filterSensitiveLog(inputShape, shape) {\n        switch (inputShape.type) {",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "147590167",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1782,
        "pr_file": "lib/event_listeners.js",
        "discussion_id": "147590167",
        "commented_code": "@@ -469,14 +469,52 @@ AWS.EventListeners = {\n       var req = resp.request;\n       var logger = req.service.config.logger;\n       if (!logger) return;\n+      function filterSensitiveLog(inputShape, shape) {\n+        switch (inputShape.type) {",
        "comment_created_at": "2017-10-29T18:37:50+00:00",
        "comment_author": "jeskew",
        "comment_body": "I think you need to return early here if `shape` is undefined. There are recursive shapes defined in some services, and this function will need to check for some stopping condition.",
        "pr_file_module": null
      },
      {
        "comment_id": "147770081",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1782,
        "pr_file": "lib/event_listeners.js",
        "discussion_id": "147590167",
        "commented_code": "@@ -469,14 +469,52 @@ AWS.EventListeners = {\n       var req = resp.request;\n       var logger = req.service.config.logger;\n       if (!logger) return;\n+      function filterSensitiveLog(inputShape, shape) {\n+        switch (inputShape.type) {",
        "comment_created_at": "2017-10-30T17:08:54+00:00",
        "comment_author": "AllanZhengYP",
        "comment_body": "Oh right. Thank you for pointing out.",
        "pr_file_module": null
      }
    ]
  }
]

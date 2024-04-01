# Access Tableau Embedding API v3

Stating with Tableau 2021.4, the Embedding API v3 library is available for use on Tableau Server, Tableau Cloud, Tableau Public, and on the Tableau CDN. To add the Embedding API to your web pages and applications, you simply link to the library.

The Embedding API library contains functions for interacting with the Embedding API. The Embedding API library is available in multiple versions, and each version of the library corresponds to a specific version of Tableau. Additionally, for each version of the Embedding API file, there is also a minified file (.min) that you can use in production environments to reduce the amount of data that browsers need to download.

## Versions of the Tableau Embedding API
The following table lists the Embedding API v3 library files and the corresponding versions of Tableau. For compatibility, you should use the version of the library that matches the version of Tableau you are using.

Tableau Version	Embedding API v3 Files	Availability
2023.3.x	tableau.embedding.3.8.0.min.js	Tableau Cloud (December 2023)
 	tableau.embedding.3.8.0.js
2023.3	tableau.embedding.3.6.0.min.js	Tableau Cloud, Tableau Server
 	tableau.embedding.3.6.0.js
2023.2	tableau.embedding.3.6.0.min.js	Tableau Cloud
 	tableau.embedding.3.6.0.js
2023.1	tableau.embedding.3.5.0.min.js	Tableau Cloud, Tableau Server
 	tableau.embedding.3.5.0.js
2022.4	tableau.embedding.3.4.0.min.js	Tableau Cloud
 	tableau.embedding.3.4.0.js
2022.3	tableau.embedding.3.3.0.min.js	Tableau Cloud, Tableau Server
 	tableau.embedding.3.3.0.js
2022.2	tableau.embedding.3.2.0.min.js	Tableau Cloud
 	tableau.embedding.3.2.0.js
2022.1	tableau.embedding.3.1.0.min.js	Tableau Cloud, Tableau Server
 	tableau.embedding.3.1.0.js
2021.4	tableau.embedding.3.0.0.min.js	Tableau Cloud, Tableau Server
 	tableau.embedding.3.0.0.js

You can access non-minified versions of the library by removing .min from the filename, for example, tableau.embedding.3.6.0.js. Use the non-minified version of the library during development as it can help when you need to debug your embedding code.

## Where to get the Embedding API v3 library
Starting with Tableau 2021.4, you can get the Embedding API v3 library from multiple locations, including Tableau Server, Tableau Cloud, Tableau Public, and the Tableau CDN (https://embedding.tableauusercontent.com/). Starting with Tableau 2024.1, you can get the Embedding API v3 library from npm.

As a general rule, you should always get the Embedding API v3 library from the same Tableau instance that hosts your visualizations. This ensures that you always use a version of the library that is compatible with the version of Tableau you are using.

## Accessing the library on Tableau
For convenience, you can link to latest version of the library (tableau.embedding.3.latest) rather than the specific version for the release (3.0.0, 3.1.0, etc.). The file (tableau.embedding.3.latest.min.js, or tableau.embedding.3.latest.js) will always point to the most recent release of the library on that instance of Tableau. The file (tableau.embedding.3.latest.min.js, or tableau.embedding.3.latest.js) is only available on Tableau Server, Tableau Cloud, and Tableau Public. If you use the Tableau CDN (https://embedding.tableauusercontent.com/), you need to link to the specific version of the file that you want to include.

Note that you cannot link to a local copy of the library (using file://), as it will cause Cross-Origin Resource Sharing (CORS) errors. You must link to the library on Tableau or the Tableau CDN, or on a server over HTTPS.

The Embedding API v3 library is a JavaScript ES6 module. To include the library in the HTML code for your web application, you need to set the type attribute to module in the `<script>` tags. For more information about the use of modules, see JavaScript modules.

Note that you can only use the Embedding API v3 library when you are embedding views from Tableau 2021.4 or later. If you use an incorrect version of the API with Tableau Server, Tableau Cloud, or Tableau Pubic, you will see a version incompatible error.

For Tableau Server 2021.4 and later, add the following code to a web page to link to the latest Embedding API v3 library:
```html
<script type="module" src="https://my-server/javascripts/api/tableau.embedding.3.latest.min.js"></script>
```

Replace my-server with the name of your Tableau Server. For example, if your server is www.example.com, to use the Embedding API v3 library you would include this line in your HTML page:
```html
<script type="module" src="https://www.example.com/javascripts/api/tableau.embedding.3.latest.min.js"></script>
```

For Tableau Cloud, use the following:
```html
<script type="module" src="https://Tableau-Pod.online.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js"></script>
```

Replace Tableau-Pod with the name of your pod. For example, if your Tableau Pod is 10ax, the URL would look like this:
```html
<script type="module" src="https://10ax.online.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js"></script>
```

For Tableau Public, use the following:
```html
<script type="module" src="https://public.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js"></script>
```

## Installing the npm package
Starting with Tableau Cloud (December 2023), the Embedding API v3 libraries are available from Node Package Manager (npm). You should always use a version of the library that it compatible with the version of Tableau that hosts the view. See Versions of the Tableau Embedding API.

The following command installs the Embedding API v3 library in the node_modules folder of the current directory.
```bash
npm i @tableau/embedding-api
```

To install a specific version of the library, append `@<version>` to the command. For example, to install the 3.8.0 library, you would use the following command.
```bash
npm i @tableau/embedding-api@3.8.0
```

You can verify the installation by checking files in the `node_modules` folder. If a `package.json` file exists in the directory where you ran the install command, and specifies the version of the library to use, the latest version of the library that satisfies the semantic versioning is installed. If no `package.json` exists, or no dependency for the library is specified, the latest version of the library is installed.

The following entry in the package.json file specifies the 3.9 library (including patch versions of that release).
```json
"dependencies": {
    "@tableau/embedding-api": "^3.9.0"
  }
```

# Import the npm package
In your JavaScript or TypeScript code, import the TableauViz object and any other classes and objects you need from the Embedding API v3 library. To simplify your code and improve load times, import just the classes you need, for example TableauViz to create the JavaScript object and TableauEventType to set an event listener. To import TableauViz and TableauEventType, use the following statement. Note that the library is specified using the scoped package (@tableau/embedding-api).
```js
import { TableauViz, TableauEventType } from '@tableau/embedding-api';
```

Note also if you import the library, which is an ES module, you need to specify "type": "module" in the package.json file.
```json
 "type": "module",
```

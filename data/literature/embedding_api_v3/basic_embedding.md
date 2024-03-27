# Basic Embedding

The easiest way to embed Tableau views into web applications is to use the embed code that is generated when you click the Share button on a published view. You simply copy the code and place it in your HTML page. Starting with Tableau 2021.4, the Embedding API v3 makes it almost as easy by giving you the option of simply adding a web component to your web page.

Starting in Tableau 2022.3, Tableau Server, Tableau Cloud, and Tableau Public use the Embedding API v3 web component for the Embed Code option (available from Share button on the toolbar). The good news is that embedding views using the Embedding API v3 code is now even easier. You can use the Embedding API v3 in Tableau 2021.4 and later.

For the Embedding API v3, there are two ways to initializing the API and embed the visualization in your web application:

Use the web component (`<tableau-viz>`) in your HTML code.

Use JavaScript to create the `TableauViz` object.

You can also take a hybrid approach and combine these two ways. This topic will show you how you can use these options.

For information about editing embedded views, see Embed Web Authoring.


## Use the `<tableau-viz>` web component for basic embedding
The Tableau Embedding API v3 makes embedding a view in your web page or application easy to do, without a lot of JavaScript coding. You just link to the Embedding API library and then add a web component to your HTML code, much like you would any other HTML element.

### Link to the Embedding API library
Starting with Tableau 2021.4, the Embedding API v3 is available on Tableau Server, Tableau Cloud, and Tableau Public. In most cases, you should use the version of the Embedding API library that is hosted on the Tableau instance that is serving the view you are embedding. If you use the file from one of these locations, you can link to the file tableau.embedding.3.latest.min.js, which will always point to the latest release of the library.

The library is a JavaScript ES6 module. To use the library in your web application, you need to set the type attribute to module in the `<script>` tags.

For example, in the following HTML code, replace my-server with the name of your Tableau Server, or the name of the server for your Tableau developer sandbox, if you are part of the Tableau Developer Program. If you are using Tableau Public, use public.tableau.com. If you are using Tableau Cloud, be sure to include the name of the pod in the name of the server, for example, if your pod is 10ax, you would use 10ax.online.tableau.com.
```html
<script type="module" src="https://my-server/javascripts/api/tableau.embedding.3.latest.min.js"></script>
```

The library is also hosted on the Tableau CDN, https://embedding.tableauusercontent.com/. If you use the library from the CDN, you need to link to a specific release of the file. For example, to use version 3.1.0 of the library, you would include the following in your HTML code:
```html
<script type="module" src="https://embedding.tableauusercontent.com/tableau.embedding.3.1.0.min.js"></script>
```

The file, tableau.embedding.3.latest.min.js, is only available on Tableau Server, Tableau Cloud, and Tableau Public. For more information about the library file, see Access the Embedding API.

## Add the `<tableau-viz>` component to your HTML page
After you link to the library, you can use Tableau Embedding API. Using a `<tableau-viz>` web component is the simplest way to embed a view into a page and to initialize the Embedding API. You can use the component to configure how you want to initialize the display of the view, by adding attributes, see Configure Embedding Objects and Components.

The basic structure of the `<tableau-viz>` web component is as follows:
```html
<tableau-viz id="tableauViz"
  src='https://my-server/views/my-workbook/my-view'>
</tableau-viz>
```

The `src` attribute specifies the URL of the view on Tableau Server. The best way to get the URL is to click the Share button on the Tableau toolbar and then use the Copy Link. The id attribute identifies the instance of the web component. You will need this id if you want to access the view programmatically after the initial loading. For more information, see Interact with the View.

> For security in your embedded application, you should always specify the URL using the Hypertext Transfer Protocol Secure (HTTPS). HTTPS helps protects privacy by encyrypting communication.

>Note: Starting in Tableau 2022.3, Tableau Server, Tableau Cloud, and Tableau Public will use the Embedding API v3 web component for the Embed Code option (available from the Share button on the toolbar). The `<tableau-viz>` component replaces the JavaScript API v1 code previously used. If you have web pages that use Embed Code, you should update them to use the new initialization method. Be sure to include a link to the Embedding API v3 library.

For information about how you can configure the `<tableau-viz>` component, see Configure Embedding Objects and Components.

## Use JavaScript to initialize the API and embed the view
In some instances, you might prefer to configure and initialize the embedded view using JavaScript and the TableauViz object, rather than using the `<tableau-viz>` web component.

The first step is to create an `<div>` to contain the embedded view in your HTML code. In this respect, this is similar to what you do to embed a view using the JavaScript API v2. You also need to give the `<div>` an identifier (say, tableauViz) so that you can specify that element when you append the embedded view. This is important because the view is not rendered until you add it to the DOM.

### HTML code
```html
<div id="tableauViz"></div>
```

Also, if you put your JavaScript code in a separate .js file, you’ll need to import the file in your HTML page with the type set as module.
```html
<script type="module" src="./myEmbeddedCode.js"></script>
```

# JavaScript code for embedding a TableauViz object
In your JavaScript code, you need to import the TableauViz object from the Embedding API v3 library. You can then create a new instance of the object and configure the object with the path to the view and other properties and methods supported by the object (see Configure Embedding Objects and Components. To simplify your code and improve load times, import just the classes you need, for example TableauViz to create the JavaScript object and TableauEventType to set an event listener.
```js
import {
  TableauViz,
  TableauEventType,
} from 'https://my-server/javascripts/api/tableau.embedding.3.latest.min.js';
```

For example, the following code shows how you might embed a view. In this instance, the toolbar is hidden. The example shows how you could add an event listener. In this case, the code adds a MarkSelectionChanged event, which is triggered whenever the marks selected in the view change. Elsewhere in your code, you would need to add a handleMarkSelection() method to handle the event.

It’s important to note that creating the object `new TableauViz()` does not render the view. To do that, you must add it to the DOM (that is, add it to `document` using `appendChild()`, for example).
```js
import {
  TableauViz,
  TableauEventType,
} from 'https://my-server/javascripts/api/tableau.embedding.3.latest.min.js';

const viz = new TableauViz();

viz.src = 'https://my-server/views/my-workbook/my-view';
viz.toolbar = 'hidden';
viz.addEventListener(TableauEventType.MarkSelectionChanged, handleMarkSelection);

document.getElementById('tableauViz').appendChild(viz);

/*  Methods */

function handleMarkSelection() {
  alert('Mark(s) selected!');
  // code to handle the mark selection goes here
}
```

Important: If you put your JavaScript code in a separate .js file, you’ll need to import the file in your HTML page with the type set as module. If you import the file as text, the Embedding API library fails to load.
```html
<script type="module" src="./myEmbeddedCode.js"></script>
```

For information about how you can configure the TableauViz object see Configure Embedding Objects and Components.

## Combine JavaScript and the `<tableau-viz>` web component to embed the view
Some people might prefer a hybrid approach, combining the advantage of using a semantic HTML element with the flexibility and efficiency of JavaScript. In this case, you add a `<tableau-viz>` web component to your HTML page. But instead of specifying all of the attributes, the URL, toolbar options, etc., you just specify the `<tableau-viz>` element and provide it with a unique id.

In your HTML code, include the link to the Embedding API library and then add the web component.
```html
<script type="module" src="https://my-server/javascripts/api/tableau.embedding.3.latest.min.js"></script>

<tableau-viz id="tableauViz"></tableau-viz>
```

In your JavaScript code, create the viz object from the HTML element, and then use the viz object to configure the embedded view.
```js
const viz = document.getElementById("tableauViz");
viz.src = url;
```

This is similar to the process you take when you Interact With the View created using the web component.

Example of basic embedding using the `<tableau-viz>` web component
Here’s the code that shows basic embedding:
```html
<script type="module" src="https://public.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js"></script>

<tableau-viz id="tableauViz"
  src='https://public.tableau.com/views/Superstore_embedded_800x800/Overview'
  toolbar="bottom" hide-tabs>
</tableau-viz>
```

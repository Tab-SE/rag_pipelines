# Embed Tableau Web Authoring

Available in Tableau 2022.2 and later, you can embed Tableau views into your web application and can conveniently edit, explore, and author new content in the workbook, all without leaving your web application. Users no longer have to sign in separately to Tableau to update and publish the viz. Using the Embedding API v3, embedding a viz for authoring is as easy as embedding a viz for viewing. The Embedding API provides a `<tableau-authoring-viz>` web component that you can place in your HTML code. If you want to use JavaScript to initialize the API and embed the authoring viz, you can instantiate a TableauAuthoringViz object and set viz authoring properties.

Just like for embedding views, there are two ways to initialize the API and embed the view in web authoring mode into your web application:

Use the web component (`<tableau-authoring-viz>`) in your HTML code.

Use JavaScript to create the TableauAuthoringViz object.

This topic will show you how you can use these two options.

Note: Web authoring is only available to those Tableau users who have Web Edit capabilities for the view. Embedding the web authoring web component or object in a web application does not grant editing capability to all users.

If you don't need to embed a view that supports web authoring, see Basic Embedding.

## Use the `<tableau-authoring-viz>` web component for embedded web authoring
The Tableau Embedding API v3 makes embedding a view in web authoring mode easy to do, without a lot of JavaScript coding. You link to the Embedding API library and then add the <tableau-authoring-viz> web component to your HTML code, just like you would with the <tableau-viz> web component.

### Link to the Embedding API library
In most cases, you should use the version of the Embedding API library that is hosted on the Tableau instance that is serving the view you are embedding. If you use the file from one of these locations, you can link to the file tableau.embedding.3.latest.min.js, which will always point to the latest release of the library. Support for embedded web authoring was first added to the Embedding API 3.2.0 library and is available in Tableau 2022.2 and later.

For example, in the following HTML code, replace my-server with the name of your Tableau Server, or the name of the server for your Tableau developer sandbox, if you are part of the Tableau Developer Program. If you are using Tableau Public or Tableau Cloud, use public.tableau.comor online.tableau.com as the name of the server.
```html
<script type="module" src="https://my-server/javascripts/api/tableau.embedding.3.latest.min.js"></script>
```

For more information about linking to library file, see Access the Embedding API.

## Add the `<tableau-authoring-viz>` component to your HTML page
After you link to the library, you can use Tableau Embedding API. Using a `<tableau-authoring-viz>` web component is the simplest way to embed a web authoring view into a page and to initialize the Embedding API. You can use the component to configure how you want to initialize the display of the view, by adding attributes, see Configure Embedding Objects and Components.

The basic structure of the `<tableau-authoring-viz>` web component is as follows:
```html
<tableau-authoring-viz id="tableauAuthoringViz"
  src='https://my-server/views/my-workbook/my-view'>
</tableau-authoring-viz>
```

The `src` attribute specifies the URL of the view on Tableau Server. The best way to get the URL is to click the Share button on the Tableau toolbar and then use the Copy Link. The id attribute identifies the instance of the web component. You will need this id if you want to access the view programmatically after the initial loading. For more information, see Interact with the View.

For security in your embedded application, you should always specify the URL using the Hypertext Transfer Protocol Secure (HTTPS). HTTPS helps protects privacy by encyrypting communication.
For information about how you can configure the `<tableau-authoring-viz>` component, see Configure Embedding Objects and Components.

## Use JavaScript to initialize the API and embed the viz
In some instances, you might prefer to configure and initialize the embedded view using JavaScript, rather than using the the `<tableau-authoring-viz>` web component. Using this approach, you create a TableauAuthoringViz object and set viz authoring properties.

The first step is to create a `<div>` to contain the embedded view in your HTML code. In this respect, this is similar to what you do to embed a view using the JavaScript API v2. You also need to give the `<div>` an identifier (say, tableauAuthoringViz) so that you can specify that element when you append the embedded view. This is important because the view is not rendered until you add it to the DOM.

HTML code
```html
<div id="tableauAuthoringViz"></div>
```

In your JavaScript code, you need to import the `TableauWebAuthoringViz` object from the Embedding API v3 library. You can then create a new instance of the object and configure the object with the path to the view and other properties and methods supported by the object (see Configure Embedding Objects and Components). It’s important to note that creating the object (new TableauWebAuthoringViz()) does not render the view. To do that, you must add it to the DOM (that is, add it to document using appendChild(), for example).

The following example, shows how you might embed a web authoring view by creating a `TableauWebAuthoringViz` object. Note that the embedded view and embedded web authoring view have different attributes. See Configure Embedding Objects and Components. In this case, the web authoring view adds an event listener for a publishing event (WorkbookPublished). You would need to add a `handlePublished()` method to handle the event.
```js
import {
  TableauAuthoringViz,
  TableauEventType,
} from 'https://my-server/javascripts/api/tableau.embedding.3.latest.min.js';

const viz = new TableauAuthoringViz();

viz.src = 'https://my-server/authoring/my-workbook/my-view';
viz.hideCloseButton = true;
viz.addEventListener(TableauEventType.WorkbookPublished, handlePublished);

document.getElementById('tableauViz').appendChild(viz);
```

Important! If you put your JavaScript code in a separate .js file, for example myEmbeddedCode.js, you’ll need to import the file in your HTML page with the type set as module. If you import the file as text, the Embedding API library fails to load.
```html
<script type="module" src="./myEmbeddedCode.js"></script>
```

## Combine JavaScript and the `<tableau-authoring-viz>` web component to embed the view
Some people might prefer a hybrid approach, combining the advantage of using a semantic HTML element with the flexibility and efficiency of JavaScript. In this case, you add a `<tableau-authoring-viz>` web component to your HTML page. But instead of specifying all of the attributes, the URL, toolbar options, etc., you just specify the `<tableau-authoring-viz>` element and provide it with a unique id.

In your HTML code, include the link to the Embedding API library and then add the web component.
```html
<script type="module" src="https://my-server/javascripts/api/tableau.embedding.3.latest.min.js"></script>
<tableau-authoring-viz id="tableauAuthoringViz"></tableau-authoring-viz>
```

In your JavaScript code, create the viz object from the HTML element, and then use the viz object to configure the embedded view.

```js
const viz = document.getElementById("tableauAuthoringViz");
viz.src = url;
```

This is similar to the process you take when you Interact With the View created using the web component.

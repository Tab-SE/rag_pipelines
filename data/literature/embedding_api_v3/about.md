# About the Embedding API v3

The Embedding API v3 is a modern JavaScript library that supports Tableau viz web components. You can embed Tableau views in web pages and web applications using the JavaScript library methods directly, or embed views using the Tableau viz web components and attributes in your HTML code without using the API directly.

## Embedding API v3 interfaces
The top-level object is the Viz object. You can create, or instantiate, a Viz object as either a TableauViz object (to embed a view) or a TableauAuthoringViz object (to embed a web authoring view). From the Viz object, you can access all the workbooks, sheets, methods, and properties contained in the Viz object. You can also embed a view or a web authoring view using the Tableau web components (<tableau-viz> and <tableau-authoring-viz>). From these web components you can also access the Viz object for further processing. You configure the Viz objects or web components by setting attributes or properties. For information about creating a Viz object, see Basic Embedding. For information about configuring the Viz object, see Configure Embedding Objects and Components.

The Embedding API v3 provides a rich set of interfaces. The basic interfaces are shown in the following diagram. After you create the Viz object (in either viewing or authoring mode), you can navigate to the individual worksheets and elements in the view through these interfaces.

```js
// create the viz object, assumes an <div> element exists with id="tableauViz"

import {
  TableauViz,
} from 'https://public.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js';

const viz = new TableauViz();

viz.src = 'https://my-server/views/my-workbook/my-view';
viz.toolbar = 'hidden';

// add the viz object to the DOM
document.getElementById('tableauViz').appendChild(viz);

let sheet = viz.workbook.activeSheet;
sheet.applyFilterAsync("Container", ["Boxes"], FilterUpdateType.Replace);
```

For more information about the Embedding API v3 interfaces, see the Embedding API Reference.

## Importing the Embedding API v3 library
The Embedding API v3 library is available as a JavaScript ES6 module, and as such, requires some special considerations. To include the library in the HTML code for your web application, you need to set the type attribute to module in the `<script>` tags.

```js
<script type="module" src="https://YOUR-SERVER/javascripts/api/tableau.embedding.3.latest.min.js"></script>
```

If you are creating a JavaScript file(s) as part of your embedded web application, to improve load times, import just the features you need from the Embedding API v3 library. For example, you might import TableauViz to create the JavaScript object and TableauEventType to set an event listener. When you include your JavaScript file in your web application, be sure to set the type to module in the `<script>` tags in your HTML code.

```js
import {
  TableauViz,
  TableauEventType,
} from 'https://public.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js';
```

For more information about the use of modules, see JavaScript modules. For information about accessing the library and library compatibility, see Access Tableau Embedding API v3.

## Use Async/Await for methods that return promises
The Embedding API v3 provides a number of asynchronous methods, methods such as, applyFilterAsync(),displayDialogAsync(), or getMarksAsync(). These are methods that return promises. The Embedding API v3 supports the standard JavaScript ES6 Promises, including the async/await syntax of the ES2017. In the past, you might have used promise chaining (.then methods, sometimes combined with arrow function expressions => ) to link the results from the asynchronous methods. Introduced in ECMAScript 2017, async/await operators provide an easier way to work with promises.

For example, the follow code snippet shows an event handler for a MarkSelectionChanged event. The .then() method handles the promise (the selected marks). If you wanted to further process the results with other asynchronous calls, you could add additional .then() methods.

```js
function getSelectedMarks(event) {
    event.detail.getMarksAsync().then( (marksSelected) => {
      const numMarks = marksSelected.data[0].data.length;
      alert(`${numMarks} marks Selected`);
      // add additional asynchronous methods ...
    });  // add .then() methods for additional promises
}
```

To use the async/await statement for the same event handler, you declare the function to be an asynchronous function (async). And then use the await keyword for the call to the getMarksAsync() method, an asynchronous method that returns a promise. You can only use await in functions declared as an async function.

```js
async function getSelectedMarks(event) {
    const marksSelected = await event.detail.getMarksAsync();
    const numMarks = marksSelected.data[0].data.length;
    alert(`${numMarks} marks Selected`);
    // call additional asynchronous methods with the await keyword
}
```


For more information, see async function in the MDN docs.

## Understanding when Embedding API promises resolve
Some Embedding API methods that return promises, such as selectMarksByValueAsync, might resolve when the action they perform was initiated, and not necessarily when the action was completed. This means the viz could still be rendering when the promise resolves. Similarly, if you are using event listeners, events such as MarksSelectionChanged might be triggered when the action is initiated and not necessarily when the action is completed. This is done so that the Embedding API performance is not affected by large vizzes that might take longer to render.

If you are trying to perform a task, such as taking a screenshot of a viz after marks are selected, we recommend that you add a reasonable delay to the task after the promise resolves or after the event is triggered.

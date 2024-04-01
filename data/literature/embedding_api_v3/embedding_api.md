# Tableau Embedding API v3

Use the Tableau Embedding API v3 to integrate Tableau visualizations into your own web applications. Harness the power of the Embedding API to add custom controls, and take advantage of modern, secure methods of authentication that allow users to interact with the visualization from your web application.

## Introducing the Embedding API v3
The Tableau Embedding API v3 provides you an easy way to embed and integrate Tableau views in your web apps and web pages. The Tableau Embedding API v3 provides for the next-level of enhancements over the Tableau JavaScript API v2. The Tableau Embedding API v3 features a redesigned process for embedding to make your life easier, to modernize the experience, and to enable new functionality.

Some parts of using the Embedding API v3 are the same as the JavaScript API v2, and others have just slightly different syntax. But the biggest difference is the initialization of the API, where you can now use web components.

Web components are a standard available in all modern browsers, that allow you to add custom, and 3rd party, functionality to your web page using HTML syntax as easily as adding an image, link, or div. Using the web component technology, we have created a <tableau-viz> component that you can use to add visualizations to your web pages.

For more information about the differences between the Embedding API v3 and the JavaScript API v2, see Upgrade from Tableau JavaScript v1 and v2.

For an overview and demonstration of the Embedding API v3 in action, see the TC 21 talk, A New Era in Tableau Embedding.

The Embedding API v3 is under active development, join the Tableau Developer Program and keep up-to-date with the coming features.

## Getting started with embedding
Embedding a Tableau visualization on a web page is straight-forward and only involves a few steps.

1. ### Link to the Embedding API library
Starting with Tableau 2021.4, the Embedding API v3 library is hosted on Tableau Server, Tableau Cloud, Tableau Public, and on the Tableau CDN (https://embedding.tableauusercontent.com/). The library (tableau.embedding.3.n.n.min.js) is a JavaScript ES6 module. To use the library in your web application, you need to set the type attribute to module in the <script> tags.

For example, to use the latest Embedding API v3 library on Tableau Public, you would use the following line of code on your web page:

```html
<script type="module" src="https://public.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js"></script>
```

For more information about the Embedding API v3 library file, see Access the Embedding API.

2. ### Add the Tableau viz web component
For the Embedding API v3, the initialization step is now easier than it was for the Tableau JavaScript API v2. You can initialize the API as part of your HTML code when you use to the <tableau-viz> web component. For example, the following code is all you need to embed a Tableau view into your HTML pages.

```html
<tableau-viz id="tableauViz"
  src='https://my-server/views/my-workbook/my-view'>
</tableau-viz>
```

You can also use the Embedding API and JavaScript code to create and configure the Tableau Viz object if you need programmatic control over the embedded view. For more information, see Use JavaScript to initialize the API and embed the view.

3. ### Customize the Tableau viz web component
To specify options on how to initialize the viz, you can add those as attributes of the <tableau-viz> element. For example, you can use attributes to show or hide the toolbar, or tabs, set the height and width of the viz, and set the device layout. For more information about the attributes you can use, see Configure TableauViz objects and components.

```html
<tableau-viz id="tableauViz"
  src="https://my-server/views/my-workbook/my-view"
  device="phone" toolbar="bottom" hide-tabs>
</tableau-viz>
```

Example of basic embedding
Here’s the code:

```html
<script type="module" src="https://public.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js"></script>


<tableau-viz id="tableauViz"
  src='https://public.tableau.com/views/Superstore_embedded_800x800/Overview'
  toolbar="bottom" hide-tabs>
</tableau-viz>
```

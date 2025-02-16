# This App

## what is this?
## what is this website or app?
## tell me more about this website or app
This website teaches you how to compose Tableau's varied product capabilities into applications
that thrill customers, coworkers and friends!

## how does this website produce docs?
## how is this app developed?
This application follows a "docs-as-code" model of development incorporating a powerful UI framework which interfaces with Markdown as the language of content, this helps developers and analysts collaborate with the community at-large and more importantly to keep up with the pace of change.

## how can I contribute to this project/app?
Contributions to this project are more than welcome and may come in the form of enhancements to the codebase, writing articles, correcting or identifying bugs or even suggesting improvements. Contributing to new or existing articles is done by editing `.mdx` files located in the `pages/` folder. The folder structure of `pages/` dictates the overall layout of the application which can be further customized via `_meta.json` files placed inside each folder. This architecture is designed and maintained by [Nextra which documents](https://nextra.site/docs/docs-theme/page-configuration) all available options for organizing content.

Refer to this guide for help with [Markdown Syntax](https://www.markdownguide.org/) such as tables, quotes and more. These provide the basics elements that make up the Markdown language.

To embed a Tableau visualization you must first import the `<TableauViz>` component into the `.mdx` article that you are writing and provide the attributes that it needs to display your analytics.

## How can I embed tableau visualizations into this app?
Here is an example of how this app's React component is used to add Tableau to Markdown:
```md
import { TableauViz } from 'components';

This is *generic* markdown content preceding the **Tableau** component of interest.
[Link Text](URL)

Notice the following attributes provided for a visualization
hosted for free on Tableau Public:

<TableauViz
  src='https://public.tableau.com/views/{viz}'
  height='900'
  width='700'
  hideTabs='true'
  device='default'
  isPublic
/>

Another block of text and an *image* can go after the embed.
![Alt Text](Image URL)
```

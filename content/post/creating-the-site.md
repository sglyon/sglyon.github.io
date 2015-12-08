---
title: "Hugo and GitHub Pages"
description: "This post explains everything I did to get this site up and running."
date: "2014-03-15"
tags:
    - "hugo"
---

Welcome to my first post! In this article I will explain the steps I took to get this site set up and running. This post will not be a comprehensive overview of everything Hugo can do. Instead, I will share some tips and tricks I found along the way for how to get a site up and running using Hugo and getting github pages to host the it.

For a more exhaustive coverage of what Hugo can do I recommend consulting the [Hugo documentation](http://hugo.spf13.com/overview/introduction). I consistently referenced the examples contained in the [Hugo showcase](http://hugo.spf13.com/showcase) when I was putting this site together.

# Hugo

## Defining the Layout

On this site I knew I wanted a `Section` for general blog posts and another `Section` to hold the course notes I while working on my PhD. I decided to name these `Section`s (in the Hugo sense of the word) `blog` and `notes`, respectively.

I then needed to create a few files:

```
/layouts
  /blog
    li.html
    summary.html
  /notes
    li.html
    summary.html
```

The `summary.html` file specifies how each file in the `Section` should be displayed in a list when first landing on the main page for the `Section`.

I am not really sure what the `li.html` files are for, but the documentation says that these files should be defined. I ended up copying and pasting the files from an example.

## Indexes

In my opinion, one of Hugo's most powerful features is the `Index`. I think of an `Index` as an arbitrary, yet structured way of organizing and displaying content. The main principle is that you can define ways to group content, then give an html template for how these groups should be shown.

To define a new index group you add them to a list in your `config.yaml` (or `config.json` or `config.toml` if you are using another format). Because I want this site to be home to my blog posts and notes I take in classes, I wanted to use indexes as a natural way to organize my content. At this point I have three indexes: (1) by category, (2) by course, and (3) by teacher. These are represented as follows in my config file (note that the values are all the plural version of the singular key):

```yaml
indexes:
  category: "categories"
  course: 'courses'
  teacher: 'teachers'
```

After telling Hugo what the indexes are, I gave them each templates in `layouts/indexes/<INDEX_NAME>.html`, where `INDEX_NAME` is the singular version of each index as defined in the config file.

The final step in getting Hugo to generate indexes is to add the index information in the metadata section of each post. This metadata section is a yaml block set off by a line containing only `---` on either side. Below I have included an example of one of these blocks from a file containing notes from one of Tom Sargent's lectures (notice the key is the plural version of the index and the value is a list of strings):

```yaml
---
title: "Ramsey Taxation I"
description: "We show how to solve the optimal taxation problem from the perspective of a Ramsey planner."
date: "2014-03-03"
tags:
  - "Ramsey Taxation"
courses:
  - "macroQ3"
teachers:
  - "Sargent"
---
```

## Mathjax

Another thing that was very important for my site was the ability to render latex math and equations. To do this I am using the [MathJax](http://www.mathjax.org/) javascript library. In order to get this to work, I needed to add a `<script>` to each page that loads MathJax and gets it set up to my liking. The easiest way to do this was to add the needed code to the file `layouts/chrome/footer.html`, because I include the footer on every page.

Before showing the portion of that file dedicated to MathJax, I first want to discuss an issue I had getting it set up. I am used to using MathJax in markdown either within an IPython notebook, or when using Pandoc as the markdown processor. Both of these systems have very good MathJax integration and work very well. However, the markdown processor used by Hugo does not have built in MathJax support. One feature of markdown is that an underscore (`_`) can be used to denote emphasis. This means that `_this_` is rendered as _this_ in markdown. The problem is that the underscore is very common in LaTeX fragments to denote a subscript. So, when first building this site I noticed that any snippet of math that had underscores in it would not render as math, but would instead cause a large portion of the content to be presented in italics.

I googled for a while to find a solution to this problem. One solution was to escape each underscore by writing `\_` instead of `_`. This required me to make far too many changes. Another solution I found was that if I wrapped the math in `<div>MATH</div>` it would be unaffected. However, the `<div>` inserts a line break, so for inline math this wasn't an issue. The final solution I came up with was from [this blog post](http://doswa.com/2011/07/20/mathjax-in-markdown.html). The solution consists of adding some MathJax settings to `footer.html` as well as a function that allows verbatim text (text in between two backticks) to be untouched by markdown, but processed by MathJax. The final result was the following snippet of html in my `footer.html` template

```html
<!-- Loading MathJax -->
<script type="text/javascript"
  src="https://c328740.ssl.cf1.rackcdn.com/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>

<script type="text/x-mathjax-config">
MathJax.Hub.Config({
  tex2jax: {
    inlineMath: [['$','$'], ['\\(','\\)']],
    displayMath: [['$$','$$'], ['\[','\]']],
    processEscapes: true,
    processEnvironments: true,
    skipTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
    TeX: { equationNumbers: { autoNumber: "AMS" },
         extensions: ["AMSmath.js", "AMSsymbols.js"] }
  }
});
</script>

<script type="text/x-mathjax-config">
  MathJax.Hub.Queue(function() {
    // Fix <code> tags after MathJax finishes running. This is a
    // hack to overcome a shortcoming of Markdown. Discussion at
    // https://github.com/mojombo/jekyll/issues/199
    var all = MathJax.Hub.getAllJax(), i;
    for(i = 0; i < all.length; i += 1) {
        all[i].SourceElement().parentNode.className += ' has-jax';
    }
});
</script>
```

## Other

The rest of my Hugo setup was created by following the example from [Kieran Healy's website](http://kieranhealy.org/) and consulting the documentation.

When defining the html templates and drafting content I used Sublime Text 3 with the [Markdown Editing](https://github.com/SublimeText-Markdown/MarkdownEditing) package. the [Live Reload](https://github.com/dz0ny/LiveReload-sublimetext2) package [Live Reload google Chrome extension](https://chrome.google.com/webstore/detail/livereload/jnihajbhpnppcggbcgedagnkighmdlei?hl=en). I used Live Reload because it allowed me to update content, and upon saving a file in Sublime text, it would get automatically processed by Hugo, and reloaded by Chrome without me having to do anything. In order to get this set up I needed to do the following:

* Follow the manual installation instructions for the Live reload plugin for sublime text 3. The plugin is installable via package control for sublime text 2, but it didn't work for sublime text 3.
* Install and enable the chrome live reload extension.
* Enable the `Simple reload with delay(400ms)` live reload plugin within sublime. To do this you open the command Palette, select  `LiveReload: Enable/disable plug-ins` and then select the option mentioned in the previous sentence. I chose the short delay option because it gave Hugo a change to re-process all the material before telling Chrome to refresh the page.
* Run hugo in server and watch mode using the command `hugo server --watch`. This is a very cool feature of Hugo that not only serves up the site, but watches all the source files for changes. If it detects a change it re-processes the site and serves up the new version automatically. Because Hugo is so fast, this setup works very well and feels somewhat magical!

# GitHub Pages

After getting Hugo set up, I needed to find somewhere to host my site. I have used the free github pages service for a few websites in the past, so I was already comfortable with using it as a platform for hosting a static website. To integrate github pages within my Hugo workflow I followed the example of Dana Woodman and set up one repository to hold the structure and un-rendered content of the site, and another to hold the content generated by Hugo.

In the repository [sglsitecontent](https://github.com/spencerlyon2/sglsitecontent) I have all the content for the site, and the repository [spencerlyon2.github.io](https://github.com/spencerlyon2/spencerlyon2.github.io) hosts the content generated by Hugo. To make this dual repository setup easier, I defined the directory `/public` within the sglsitecontent repo to be both where Hugo should put the generated output, *and* a git subtree that points to the root of the master branch of the spencerlyon2.github.io repo.

To do this I removed completely the public folder from the content repo using `rm -rf public`. Then I added the subtree under the prefix (directory) public using the command

```
git subtree add --prefix public git@github.com:spencerlyon2/spencerlyon2.github.io.git master --squash
git subtree pull --prefix=public
```

Now, when I run the `hugo` command again, the output is placed in the public directory, which the content repo thinks is a mirror of the github.io repo. The final step in this process was to define a simple script `deploy.sh` that builds the site, adds everything, commits the changes, then pushes to both repositories. This script is

```sh
#!/bin/bash

echo -e "\033[0;32mDeploying updates to Github...\033[0m"

# Build the project.
hugo -s ./

# Add changes to git.
git add .

# Commit changes.
msg="rebuilding site `date`"
if [ $# -eq 1 ]
  then msg="$1"
fi
git commit -m "$msg"

# Push source and build repos.
git push origin master
git subtree push --prefix=public git@github.com:spencerlyon2/spencerlyon2.github.io.git master
```

Now when I run `./deploy.sh` hugo is run, all the changes are added and committed into git then pushed to both repositories.

# Conclusion

I hope that this post is helpful to someone else trying to set up a blog using Hugo and github pages. I will probably add another post in the future as I learn more about Hugo and make changes to my setup.

---
title: "Custom URL with GitHub Pages and DynDns"
description: "Details how I got my custom domain purchased from dyndns.org to redirect to my GitHub pages site."
date: "2014-03-21"
tags:
    - "web"
---

## Buying a Domain

I think that the domain name [spencerlyon2.github.io](http://spencerlyon2.github.io) is alright, but I really want my GitHub Pages website to point to a custom domain that I own. So, I went to [dyndns.org](http://dyndns.org) and purchased the domain [sglyon.com](sglyon.com). It cost me $50.00 for two years. (<font size=2>I since learned of another website called [namecheap.com](http://namecheap.com) that only costs about $10.00 a year, depending on the extension of the domain. If I were to do it again, I would register my domain name through them.</font> )

## Getting GitHub Pages Pointed to the Right Place

This is the easiest step. I simply created a file named `CNAME` that has only the content

```
sglyon.com
```

That's all on the GitHub end: pretty easy!

## Setting up DNS on DynDns website

This was the most confusing part for a web programming newb like me. After searching through the [setting up a custom domain](https://help.github.com/articles/setting-up-a-custom-domain-with-pages) and [troubleshooting](https://help.github.com/articles/my-custom-domain-isn-t-working) pages from the GitHub pages help site, I finally found a solution.

I ended up creating (modifying) 3 records:

* An `A` record that points to `192.30.252.153` with TTL set to `1800`
* An `A` record that points to `192.30.252.154` with TTL set to `1800`
* A `CNAME` record that points to `spencerlyon2.github.io` with TTL set to `1800`

In the end the configuration page on my Dns management page looked like the image below.

<!-- ![Hostname setup for DynDns and GitHub Pages](/images/DynHostnames.png) -->
<div class="container-fluid">
<img src="/images/DynHostnames.png" alt="Hostname setup for DynDns and GitHub Pages" class="img-responsive center-block"/>
</div>

## Verifying and Testing

I then verified that my domain name pointed to the GitHub servers using the command `dig sglyon.com  +nostats +nocomments +nocmd` and was pleased it returned the following:

```
; <<>> DiG 9.8.3-P1 <<>> sglyon.com +nostats +nocomments +nocmd
;; global options: +cmd
;sglyon.com.      IN  A
sglyon.com.   1405  IN  A 192.30.252.154
sglyon.com.   1405  IN  A 192.30.252.153
```

After waiting for about ten minutes I could successfully point my browser to `sglyon.com` and it would open up this website!

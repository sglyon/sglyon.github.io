---
title: "Parallel data movement in Julia"
description: "How to move data across processes in a parallel Julia environment"
date: "2014-12-29"
draft: true
tags:
    - "julia"
    - "parallel"
---

This post contains the notes I took when trying to understand how data movement works across processes in Julia. The content of this post is broken into two sections:

1. An introduction to parallel computing in Julia. This section mainly pulls content from the [parallel computing section](http://julia.readthedocs.org/en/latest/manual/parallel-computing/) of the Julia documentation
2. A section of how-to's providing explanations and examples for performing common data movement tasks

## Intro: Key building blocks

Parallel programming in Julia is built around a few key concepts. Below is a rough sketch of how these pieces fit together:

* A single process (which I will call the **root** process or root for short) drives computation, which is done by secondary processes called **workers**
* One process (typically the root process) issues a **remote call** on another (possibly the same) process. The remote call is an instruction to execute certain code on a particular process
* The remote call *immediately* returns a **remote reference**. The remote reference can be thought of as an IOU that holds a [thunk](http://en.wikipedia.org/wiki/Thunk) (or placeholder) for the actual value that was computed by the working process that executed the call. Note it *does not* hold the value itself, but a reference to it
* This remote call can be **fetch**ed from another process, which will retrieve the actual *value* computed by the call

## How to pass data...

### ... from worker to worker

Imagine that we have three processes: 1 main

### ... from main to worker

### ... from worker to main

---
layout: post
title:  "Rosie v1.0.0-alpha-2 released"
date:   2017-10-22
categories: release
---

Rosie version 1.0.0-alpha-2 has been released, and the Python module is back!

There is a fresh implementation of `librosie.so`, making Rosie available (again)
from a variety of programming languages.  A module for one language, Python, is
part of the 1.0.0-alpha-2 release.

I am very interested in feedback and contributions to make `rosie.py` better.
In particular, more arguments can be made into keywords or given default values.

Also, the current api provided by `rosie.py` returns the match data in a buffer
created by the cffi package.  This buffer does not have all the features of
"standard" Python buffers or memory views.  The api returns this buffer in order
to avoid making a decision for the user about how the match data will be used.
In other words, converting it to a string would require making a copy of the
data, whereas often the buffer can be used directly instead.

Rosie can return match data in many forms, though probably the most useful for a
Python programmer is the JSON format, which can be processed by `json.loads` to
produce a Python structure.

My experience with JSON libraries leads me to think that many inefficiencies
lurk there, however.  This is why Rosie has its own JSON generator, tailored to
implement only the needed features, and written in C

If Python's `json.loads` is too slow, there is an attractive alternative.  Rosie
can produce a byte-encoded output that has a simple format.  Match data in this
compact encoding can be returned to Python, where it could be decoded in
`rosie.py`.  If anyone is interested in coding this up, let me know!

## Roadmap

Another alpha release, coming soon, will include rich support for creating
character classes based on Unicode properties.

Rosie modules for other languages, like Go, C, node.js, and Ruby, are also
forthcoming.  We had these for Rosie v0.99, and they are on the roadmap to
reproduce for the new librosie in v1.0.0.

And `rosie.py` will be revised, ideally with some help from Python programmers,
to be more Pythonic.

The Rosie macro facility has been "dark launched" in the sense that the
following macros are already part of Rosie v1.0.0:
    * find
    * findall
    * ci

Although macro documentation is lacking, some examples are lurking about.
Here's a teaser: The `find` macro skips ahead until its pattern argument is
matched, and captures the pattern argument.  Macros are invoked using the macro
name followed by a colon.  Here's an example where we want to search for the
word "nameserver" at the start of a line that also contains "201":

``` 
$ rosie -o line match '"nameserver" find:"201"' test/resolv.conf 
nameserver 192.9.201.1
nameserver 192.9.201.2
$
``` 

Finally, a number of customization capabilities are being designed, along the
lines of a `~/.rosierc` file, for users of the Rosie CLI and REPL.

Whether you code in Python or any other language that has [libffi](https://sourceware.org/libffi/) support,
you have access to #[modernpatternmatching](https://twitter.com/search?q=%23modernpatternmatching).

<hr>

Follow us on [Twitter](https://twitter.com/jamietheriveter) for announcements.
We expect v1.0.0-beta to be released before the end of 2017.



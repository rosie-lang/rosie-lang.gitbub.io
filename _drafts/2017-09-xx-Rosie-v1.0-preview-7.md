---
layout: post
title:  "Rosie v1.0 Preview #7: ..."
date:   2017-09-03
categories: preview
---

Intro...


## Enhancements over regex

RPL has many enhancements over regex.  Here, we briefly describe some of them.

### Identifiers and composability
One of the reasons that RPL expressions are easier to read and maintain than
regex (in our opinion) is that patterns can be named using identifiers.  And we
have taken great pains to ensure that RPL expressions compose, making it
possible to construct bigger patterns out of smaller ones.

This approach allows whitespace and comments to be used within a pattern
definition as desired, to make it clear what the pattern does.

And, Rosie will execute
[built-in pattern tests]({{ site.baseurl }}{% post_url 2017-07-30-Rosie-v1.0-preview-4 %}),
if you write them, which also
help document what the pattern does. 

### Captures
<a id="captures" />
By default, any pattern with a name is captured.  And all patterns in RPL have
names (not numbers).  So you can easily find a capture in the Rosie output by
looking for its identifier.

### Parse tree output
RPL enables not just named captures, but full parses.  That is, a match to
pattern `p` can have sub-matches named `x` and `y` if `p` is defined in terms of
`x` and `y`.  The result is a full parse tree, making Rosie an excellent tool
for parsing domain specific languages, configuration files, and the like.

In fact, RPL code itself is parsed by Rosie!  It's RPL all the way down!

See [an earlier post on output formats]({{ site.baseurl }}{% post_url 2017-07-04-Rosie-v1.0-preview-3 %})
for examples of parse tree output in the JSON format.


### Tokenization
<a id="tokenization" />

|  `(...)`         | _Cooked group_, the default mode, in which Rosie automatically looks for token boundaries between pattern elements |
|  `{...}`         | _Raw group_, which tells Rosie to match the pattern exactly as written, without looking for token boundaries |


### Grammars
RPL patterns can be recursive, so RPL can be used to match
recursively defined structures --- something that regex cannot do.  For example,
below is an example pattern that parses JSON-encoded data.  It uses the RPL
`grammar` declaration to define a set of mutually recursive patterns.

``` 
package json

import word, num

local key = word.dq
local string = word.dq
local number = num.signed_number

local true = "true"
local false = "false"
local null = "null"

grammar
   value = ~ string / number / object / array / true / false / null
   member = key ":" value
   object = "{" (member ("," member)*)? "}"
   array = "[" (value ("," value)*)? "]"
end
``` 

### Packages
In the JSON parsing example above, the definitions form a package.  A Rosie
package can import other packages, as shown.  This makes it easy to collect
related patterns together, and to share patterns by sharing packages.

### More

macros? functions?






## Rosie was created for scalable pattern matching

Scalability goals for Rosie include big data, large (complex) patterns, and many
developers.  The ability to trace a match, at varying levels of detail, is a key
debugging feature.  Much like reading a stack trace, you find a lot of
information.  But again, like reading a stack trace, you quickly get used to
understanding them.

Tracing, without having to paste your patterns and data into some random
website, is how 
#[modernpatternmatching](https://twitter.com/search?q=%23modernpatternmatching)
is done.

<hr>

Follow us on [Twitter](https://twitter.com/jamietheriveter) for
announcements.  We expect v1.0.0 to be released around the celestial end of
summer, i.e. the autumnal equinox.


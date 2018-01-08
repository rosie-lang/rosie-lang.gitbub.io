---
layout: post
title:  "Near-term Roadmap"
#date:   2017-12-18
categories: preview
---

Rosie v1.0.0 is in alpha release now.  Our intention is to release a beta
version in early 2018, with a frozen feature set, API, CLI, and REPL interfaces.
The beta will be a release candidate for the proper version 1.0.0.

Over the course of the alpha releases, we have been adding features and
making minor changes.  Three important features will be added before the
beta: thread safety; unicode predicates; and enhanced customization.

## Thread safety

_Edit: [2018-01-08] Thread safety arrived in `librosie` in v1.0.0-alpha-7.  See
`src/librosie/C/mt.c` for an example of a multi-threaded Rosie program._

The `librosie` in v1.0.0-alpha-6 (and earlier) is not thread-safe.  Some changes
to the API and to the compilation of the library will make it safe for
multi-threading.  An enforced limitation is that a matching engine may be used
by only one thread at a time.  In other words, for parallel execution, you must
create a matching engine for each thread.  Fortunately, matching engines are
fairly lightweight.


## Unicode predicates

Rosie v1.0.0 has a powerful feature for defining character sets, but the alpha
releases (thus far) lack support for Unicode predicates like "characters in
the Hebrew script"; or "one of the nearly 1000 characters labeled as _Numeric_" in
[Unicode 10.0.0](http://www.unicode.org/versions/Unicode10.0.0/); or the
intersection, union, or difference of these.

An upcoming alpha release will add predicates for Unicode scripts and
properties.  

Rosie supports only the UTF-8 character encoding today. No requests for other
encodings have been received, but we are
[interested to know](https://www.reddit.com/r/RosiePatternLanguage/) if the need
exists. 

_Edit: [2018-01-08] We [posted today]({{ site.baseurl }}{% post_url
2018-01-08-RPL-Character-Sets %}) on the design of character sets in RPL._ 

## Customization, and the *Rosie Prelude*

Rosie is often used from the command line, and a common request is for Rosie
to load an initialization file (e.g. `~/.rosierc`) so that frequently used
options can be specified there.

Another command-line customization is the ability to assign colors (for printing
matches in colorized text) to patterns.  This feature is also forthcoming.

And, in some installations, a user of the CLI, REPL, or API may want to have
some patterns pre-loaded automatically.  This customization is likely to take the form
of `import` statements listed in an initialization file.

Finally, some users may wish to customize the *Rosie Prelude*<sup>1</sup>,
i.e. the set of patterns and functions/macros that form the base set on top of
which other patterns are built.  Rosie patterns like `.` (dot, matching any
character), `$` (dollar, matching end of input), and `^` (caret, matching start
of input) are among the identifiers present in the Prelude.

The Rosie `.` matches any UTF-8 encoded character.  Some users may wish to
redefine `.` to match any ASCII character instead, as part of an ASCII-only
configuration. 

Similarly, the Rosie boundary pattern (bound to the tilde symbol, `~`) is
defined to match a variety of word and other boundaries.  To customize the
boundary for all imported packages and all loaded RPL files, the definition must
be modified in the Prelude.

Note: A redefinition of `~` in an ordinary (non-Prelude) RPL file will affect
all of the patterns defined in that file, but not any outside of that file.

Since pattern libraries are compiled in the environment of the Prelude,
modifications to the Prelude will affect all patterns subsequently loaded
(imported, compiled), and this can break RPL packages which depend in some way
on the standard Rosie Prelude.  The ability to use a custom Prelude is intended
for specialized use cases, and also to allow the Rosie user community to evolve
Rosie independently of official releases.

\[1\] The name *prelude* was borrowed from the Haskell language, where (to my
understanding) the [Haskell Prelude](https://wiki.haskell.org/Prelude) serves a
similar function: 
<blockquote> <strong>Prelude</strong> is a module that contains a small set
of standard definitions and is included automatically into all Haskell modules.
</blockquote>

## Rosie was created for scalable pattern matching

Rosie was created to address pattern matching _in the large_: big data; great
variety of data formats; many patterns; and many developers.  

Thread safety is a therefore requirement.  Also, the world of data and
programmers and projects is much larger than the United States, and includes so
many languages beyond English.  Thus, Unicode character predicates are a requirement.
Finally, the CLI and REPL are not only an easy way to get started with Rosie --
they are, for many users, the primary way of running Rosie.  So, the ability to
customize the user experience is also a requirement.  These requirements will be
addressed in the near-term roadmap.

Pattern matching _in the large_ is 
#[modernpatternmatching](https://twitter.com/search?q=%23modernpatternmatching).


<hr>

Please contribute discussion and questions to the
[Rosie subreddit](https://www.reddit.com/r/RosiePatternLanguage/). 

Follow us on [Twitter](https://twitter.com/jamietheriveter) for
announcements.  We expect v1.0.0-beta to be released in the first months of 2018.


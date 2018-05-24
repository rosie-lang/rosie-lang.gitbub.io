---
layout: post
title:  "Version 1.0 Coming Soon"
date:   2018-05-23
categories: 
---

<style type="text/css">
    <!--
      p.nogap {
        margin: 0em;
      }
    -->
</style>

We are about to release version 1.0.0-beta-11 of Rosie Pattern Language, and
this may be the last beta release before _Rosie version 1.0_.  Our
expectation is that version 1.0 will be released before the end of next month
(**June, 2018**).  In this post, we will review the project goals, some of Rosie's
current capabilities, and what we have planned for the coming year.

## Project goals

The Rosie Pattern Language (RPL) is a replacement for regular expressions
(regex) in situations where regex do not scale.  The Rosie project implements a
compiler for RPL and a run-time text matching engine.

Our goal is to provide a solid text-matching foundation for applications such
as:
* Data mining of unstructured and semi-structured text input
* Domain-specific text parsing, for example:
    * Systems management scripts, where pre-defined patterns that match many
      kinds of network addresses, timestamps, etc. save time and increase
      reliability.
    * Source code analysis, where a full parser may be unavailable or unwieldy,
      RPL patterns can be used to extract features like import statements,
      comments, class/method/function signatures, etc.
    * Health data management, or any domain in which Natural Language Processing
      would benefit from RPL grammars that can parse industry-specific notations
      as found in drug prescriptions, treatment instructions, and patient
      genetic information, to name just a few.
	* Cyber security and especially information security, where inputs in many
      formats must be scanned for certain textual patterns or content, whether
      to detect intrusion, prevent information leaks, or monitor compliance.

For these application domains and many others, regex are a poor foundation on
which to build.  Regex are difficult to maintain; they do not reliably compose;
they are not portable; and modern regex implementations perform erratically,
sometimes requiring exponential time on malformed input.

Additionally, Unicode support varies across regex implementations from
non-existent to fully featured, and it interacts with regex "modes" that control
case sensitivity and the meaning of "." (dot).  A goal of RPL is to approach
Unicode with a fresh perspective, hoping to avoid the compromises needed to
graft support onto decades old regex technology.

### Design strengths of the RPL language

* RPL is readable and maintainable, with syntax more like a programming language
  than the terse, cryptic syntax of regex.  This allows RPL to scale better to
  teams of developers, who must understand, maintain, and extend text-matching
  patterns. 
* RPL is based on Parsing Expression Grammars (PEGs), which can do everything
  that regex can do, and more.  In particular, RPL (and any PEG-based solution)
  can match recursively-defined text representations, such as JSON, HTML, XML,
  s-expressions, and many configuration file formats.
* RPL patterns are named, and collections of patterns form modules (libraries)
  which can be easily shared.  Organizations (and application domains) can build
  reusable libraries of common patterns, saving significant developer time and
  reducing the risk inherent in writing patterns from scratch or finding them on
  Stack Overflow.
* RPL was designed for the crucial pre-deployment steps of pre-compilation and
  testing.  (Most regex patterns are written as literal strings in a larger
  program, and those patterns are not compiled or tested until run-time, when
  code is deployed.)

### Design strengths of the Rosie implementation

* RPL files can contain unit tests that serve as regression tests (when patterns
  are modified), demonstrations (on how patterns are meant to be used), and
  documentation (about which inputs are designed to be accepted and rejected).
* Unicode support was designed to be integral, with good support today (for
  UTF-8) and additional capabilities planned.
* The Rosie implementation defines 3 stages of processing:
    * Compilation of RPL expressions into a program for a "matching virtual
      machine" (based on Roberto Ierusalimschy's `lpeg`);
    * Matching a pattern against input text, producing a match result in the
      form of a parse tree; and
    * Output encoding, in which the match result is transformed into a format
      selected by the Rosie user.  

  <p class="nogap">The explicit separation of stages yields opportunities for
  improvements and extensions to one stage that are independent of the other
  stages, e.g. (1) compiler optimizations to produce more efficient patterns;
  (2) improvements to the matching vm (e.g. to use vector instructions); (3)
  user-written output encoders for integration with other systems.</p>


## Current capabilities

Automation
* Tokenization.  The matcher looks for a (configurable) token boundary between
  pattern elements, unless the pattern is contained in curly braces `{}`.  No
  more inserting `\b` everywhere, as with regex.
* Captures.  Every named pattern is captured (unless it is an `alias`).  No more
  playing with parentheses and numbered captures, as with regex.
* Library imports. On the command line, you can use patterns like `net.ip` and
  Rosie will automatically find and use the `net` library.  While RPL patterns
  are less concise than regex generally, the ability to refer to pre-defined
  patterns by name may actually save typing (and increase reliability of your
  shell commands and scripts).

Macros
* **`find`** <br> RPL, like other PEG solutions, is greedy and
  possessive, so a pattern like 
  
  <center><code>.* X</code></center>

  will never succeed because the `.*` will
  consume all of the input.  The same idiom in RPL would be written 
  
  <center><code>&lbrace;{!X .}*  X}</code></center>

  which is cumbersome and repetitive.  The expression `find:X` applies the
  `find` macro to the pattern `X` and expands to an expression like the one
  above.  
* **`findall`** (grep) <br> The functionality of Unix grep, in which the input is
  searched for all occurrences of a pattern, is simply a repeated version of
  `find`.  The expression `findall:X` searches the input for all occurrences of
  the pattern `X`.
* **`ci`** <br> In RPL, `ci:...` transforms `...` into a case-insensitive pattern.
  All literal strings and character sets in `...` are transformed.
* **`error` <br>** Sometimes, in a complex pattern, there is a point in the pattern
  where matching will fail, but you want to return what has already been
  matched, along with an indication of where the failure occurred.  The RPL
  pattern `error:...` does this.  The argument, `...`, must be a tag
  (e.g. `#missing_close_paren`) or a string (e.g. `#"Missing delimeter"`).

Unicode 
* The dot `.` matches a single UTF-8-encoded Unicode character, or, failing
  that, a single byte.  The fall back to a single byte allows Rosie to process
  invalid UTF-8, which is a common occurrence.  The dot expression can be
  redefined within an RPL package, e.g. to enforce valid UTF-8 or match only
  ASCII. 
* Unicode blocks, scripts, categories (e.g. lower case letters), and more
  character attributes are provided as named RPL patterns, e.g. `Script.Greek`,
  a pattern in the RPL Unicode `Script` package which matches Greek letters.
* A general RPL feature, not limited to Unicode input text but very useful for
  it, is the ability to construct character set unions, intersections, and
  differences. 

Output formats
* **Color** for humans: assignable colors, e.g. dates in blue, email addresses in green.
* **JSON** for programs: nested matches (e.g. `date.month` is a sub-match of
  both `date.us` and `date.eur`) and flat lists capture the full structure of a
  match.
* **Text** of various types for scripts: text of the matching input (like grep), or
  just the matching part (like grep -o), or the first level of sub-matches.
* **Boolean** for efficiency: avoid spending cycles encoding a match when all that
  matters is whether the pattern matched or not.
* **Binary** for API: you can use Rosie from Python, Go, and other languages, and
  match structures are encoded in a compact binary format to flow over the
  `librosie` API.

Standard library
* Dates, times, timestamps
* Network addresses, including ipv4, ipv6, domain names, email and URL
* Numbers of varying kinds
* JSON, csv, and other file formats

## Planned enhancements (or, current limitations)

* Compiled patterns will be stored to disk. <br> The design of RPL's module
  (package) system is meant to support compilation of individual modules, which
  are collections of patterns.  Today, all patterns are compiled on the fly.
  There is no file format defined for saving and loading compiled RPL.  This is
  a planned enhancement.
* The RPL compiler could be faster. <br> The compiler is implemented in Lua,
  which is fast for an interpreted language.  But the compiler includes many
  assertions (which are slow in Lua) and it retains lots of debugging
  information (which consumes a lot of memory).  With the RPL language stability
  that is the essence of the forthcoming Rosie version 1.0, we can focus on
  refactoring the compiler to save time and space.
* The RPL compiler will include various optimizations.  <br> For example, when
  patterns `A` and `B` share a common prefix `X`, and could be rewritten as `{X
  AA}` and `{X BB}`, the expression `A / B` can be transformed by the compiler
  into `{X AA / BB}`, which is more efficient.
* The support for Unicode could grow, depending on enhancement requests, to
  include normalization and support for encodings other than UTF-8.
* Case insensitive Unicode searching is planned.  <br> The implementation will
  likely case fold the input as needed during matching, thus allowing a
  lexically scoped case fold RPL function, e.g. `cf:X` to match `X` without
  regard to case.  The current `ci` macro, while useful, is not an equally
  powerful solution.
* The Rosie libraries for Python and Go will be significantly enhanced, and
  libraries for other languages will be added.  

## Release schedule

In the coming weeks, a version beta-11 and possibly beta-12 will be released,
including very minor features and of course bug fixes.

The proper version 1.0 release is planned for the end of June, 2018.

Libraries for Python and Go, which allow programs in those languages to use
Rosie, are a high priority.  We are hopeful that a Python interface to
`librosie` of reasonable quality can be released with Rosie version 1.0.

In the months that follow, other libraries will be released, with a bump of the
Rosie minor version number to indicate the added functionality.  Interleaved
with library development will be work on the other planned enhancements as
outlined above.

We are always looking for contributors to the Rosie project, whether they work
on implementing enhancements, writing patterns to be shared with other users, or
authoring examples of Rosie's utility.  Open an issue on GitHub or email <a
href="mailto:info@rosie-lang.org">info@rosie-lang.org</a>. 


## Discussion on reddit

Please post comments to the
[Rosie subreddit](https://www.reddit.com/r/RosiePatternLanguage/).

<hr>

Follow us on [Twitter](https://twitter.com/jamietheriveter) for announcements
about the RPL approach to #[modernpatternmatching](https://twitter.com/search?q=%23modernpatternmatching).




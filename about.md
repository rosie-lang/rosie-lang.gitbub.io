---
layout: default
title: About Rosie Pattern Language (RPL)
permalink: /about/
---

## Rosie is like regex, but better

[Rosie](http://github.com/jamiejennings/rosie-pattern-language) is a
supercharged alternative to Regular Expressions (regex), matching patterns
against any input text.  Rosie ships with a standard library of patterns for
matching timestamps, network addresses, email addresses, CSV files, JSON, and
many more common syntactic forms.


## Rosie/RPL scales in ways that regex do not

### _Scale to many patterns_

RPL is *readable and maintainable.*  It is structured
like a programming language, so you can:
   - Build complex patterns out of simple ones 
   - Write patterns that others can read and understand, using whitespace,
     comments, and built-in test expressions
   - Create libraries of reusable patterns
   - Import pattern libraries built by other people

### _Scale to big data_

The Rosie Pattern Engine is *small and fast.*

   - The entire run-time takes less than 400KB (yes, *kilobytes*) of disk
	 space, and around 20MB of resident memory
   - Non-recursive patterns (which have the power of regex) take *linear time*
	 to match, whereas most modern regex engines can exponentially backtrack
   - Current speed (prior to v1.0.0 release) is about *5x faster* than the
	 regex-based [grok](https://www.elastic.co/guide/en/logstash/5.4/plugins-filters-grok.html)

### _Scale for productivity_

Rosie is *flexible and extensible.*
   - Unlike most regex tools, Rosie can generate structured (JSON) output,
     making its output easy to store or to consume by downstream processes
   - An alternate compressed output format can be selected to reduce data
	 transfer volume
   - The CLI uses different colors for dates, times, network addresses, etc., so
     that you don't have to read JSON when working interactively
   - Plain text (not JSON) output can be selected when using rosie to replace
     grep
   - Rosie is extensible with new patterns, libraries, color assignments, output
     formats, and macros
   - Rosie has an interactive pattern development mode to help write and debug
	 patterns
   - Rosie supports UTF-8 natively, but input text can be in any encoding; Rosie
     can even handle invalid codepoints gracefully


Rosie is released under the [MIT license](https://opensource.org/licenses/mit-license.html)

You can download Rosie from [github](http://github.com/jamiejennings/rosie-pattern-language)


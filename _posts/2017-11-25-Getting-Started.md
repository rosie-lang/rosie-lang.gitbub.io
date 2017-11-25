---
layout: post
title:  "Getting Started with RPL in 15 minutes"
date:   2017-11-25
categories: howto
---

In 5 minutes, you'll have Rosie installed in a local directory like `/tmp` or
`/home/whomever`.  In 10 minutes, you'll be using the standard pattern library
to extract _from your own data_ a variety of common patterns like network
addresses, dates, times, and more.


In 15 minutes, you'll be writing your own RPL patterns on the command line or at
the REPL.


## Install Rosie

(1) **Download** by visiting the
 [Rosie repository](https://github.com/jamiejennings/rosie-pattern-language) and
 click _Clone or download_.  Or: 
 
``` 
git clone http://github.com/jamiejennings/rosie-pattern-language
``` 


(2) **Build** Rosie by running `make` in the directory containing Rosie:

```
cd rosie-pattern-language
make
```

You can use Rosie now, by running the executable `bin/rosie`:

<pre>
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">rosie-pattern-language$ </span></span><span class="comint-highlight-input">bin/rosie --version</span>
1.0.0-alpha-6
<span class="comint-highlight-prompt">rosie-pattern-language$ </span></pre>
	
(3) Optionally, **install** Rosie by running `make install`.  The default
installation directory is `/usr/local`, and the installation will consist of:

```
/usr/local/bin/rosie           executable
/usr/local/lib/rosie           directory with additional rosie files
/usr/local/lib/librosie.so     shared library, e.g. for Python and other languages
```

If you want to call Rosie from Python at some point, you'll need to copy
`src/librosie/python/rosie.py` to wherever you keep your Python libraries.  More
on this in a future post, but meanwhile there's a 
[test program](https://github.com/jamiejennings/rosie-pattern-language/blob/master/src/librosie/python/test.py)
that illustrates the basics.


## Getting help

The Rosie CLI takes a command (like `match`) and optional switches.  One of the
commands is `help`:

<pre>
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">rosie-pattern-language$ </span></span><span class="comint-highlight-input">bin/rosie help</span>
Usage: rosie [--version] [--verbose] [--rpl &lt;rpl&gt;] [-f &lt;file&gt;]
       [--libpath &lt;libpath&gt;] [-o &lt;output&gt;] [&lt;command&gt;] ...

Rosie 1.0.0-alpha-6

Options:
   <span class="comment">--version</span>             Print rosie version
   <span class="comment">--verbose</span>             Output additional messages
   <span class="comment">--rpl</span> &lt;rpl&gt;           Inline RPL statements
   <span class="comment">-f</span> &lt;file&gt;, <span class="comment">--file</span> &lt;file&gt;
                         Load an RPL file
   <span class="comment">--libpath</span> &lt;libpath&gt;   Directories to search for rpl modules
   <span class="comment">-o</span> &lt;output&gt;, <span class="comment">--output</span> &lt;output&gt;
                         Output style, one of: nocolor, color, none, line, text, subs, default, json, byte

Commands:
   help                  Print this help message
   config                Print rosie configuration information
   list                  List patterns, packages, and macros
   grep                  In the style of Unix grep, match the pattern anywhere in each input line
   match                 Match the given RPL pattern against the input
   repl                  Start the read-eval-print loop for interactive pattern development and debugging
   test                  Execute pattern tests written within the target rpl file(s)
   expand                Expand an rpl expression to see the input to the rpl compiler
   trace                 Match while tracing all steps (generates MUCH output)

The RPL 'import' statement will search these directories in order (this is the libpath):
        /Users/jennings/Projects/rosie-pattern-language/rpl
<span class="comint-highlight-prompt">rosie-pattern-language$ </span></pre>

The RPL language reference is in the code repository at
[doc/rpl.md](https://github.com/jamiejennings/rosie-pattern-language/blob/master/doc/rpl.md).

## Match all the things!

There's a useful pattern in
[the 'all' package](https://github.com/jamiejennings/rosie-pattern-language/blob/master/rpl/all.rpl)
called 'things' that matches a few dozen common items.  Try it out with some
sample data from the rosie test directory...

<style type="text/css">
<!--
      body {
        color: #000000;
        background-color: #ffffff;
      }
      .bold {
        /* bold */
        font-weight: bold;
      }
      .comint-highlight-input {
        /* comint-highlight-input */
        font-weight: bold;
      }
      .comint-highlight-prompt {
        /* comint-highlight-prompt */
        color: #0000cd;
      }
      .comint-highlight-prompt {
        /* comint-highlight-prompt */
        color: #0000cd;
      }
      .comment {
        /* font-lock-comment-face */
        color: #888088;
      }
      .custom {
        /* (foreground-color . "green3") */
        color: #00cd00;
      }
      .custom-1 {
        /* (foreground-color . "red3") */
        color: #cd0000;
      }
      .custom-2 {
        /* (foreground-color . "blue2") */
        color: #0000ee;
      }
      .custom-3 {
        /* (foreground-color . "cyan3") */
        color: #00cdcd;
      }
      .custom-4 {
        /* (foreground-color . "yellow3") */
        color: #cdcd00;
      }
      .custom-5 {
        /* (foreground-color . "black") */
        color: #000000;
      }
      .underline {
        /* underline */
        text-decoration: underline;
      }

-->
</style>
<pre>
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">rosie-pattern-language$ </span></span><span class="comint-highlight-input">bin/rosie match all.things test/logfile </span>
<span class="custom-2">Apr</span> <span class="custom-2">8</span> <span class="bold"><span class="custom-2">09</span></span> <span class="bold"><span class="custom-2">42</span></span> <span class="bold"><span class="custom-2">24</span></span> <span class="custom-3">Js-MacBook-Pro</span> <span class="custom-1">com.apple.xpc.launchd</span> <span class="custom-5">[</span> <span class="underline">1</span> <span class="custom-5">]</span> <span class="custom-5">(</span> <span class="custom-1">homebrew.mxcl.kafka</span> <span class="custom-5">[</span> <span class="underline">68878</span> <span class="custom-5">]</span> <span class="custom-5">)</span> <span class="custom-5">:</span> <span class="custom-4">Service</span> <span class="custom-4">exited</span> <span class="custom-4">with</span> <span class="custom-4">abnormal</span> <span class="custom-4">code</span> <span class="custom-5">:</span> <span class="underline">1</span>
<span class="custom-2">Apr</span> <span class="custom-2">8</span> <span class="bold"><span class="custom-2">09</span></span> <span class="bold"><span class="custom-2">42</span></span> <span class="bold"><span class="custom-2">24</span></span> <span class="custom-3">Js-MacBook-Pro</span> <span class="custom-1">com.apple.xpc.launchd</span> <span class="custom-5">[</span> <span class="underline">1</span> <span class="custom-5">]</span> <span class="custom-5">(</span> <span class="custom-1">homebrew.mxcl.kafka</span> <span class="custom-5">)</span> <span class="custom-5">:</span> <span class="custom-4">Service</span> <span class="custom-4">only</span> <span class="custom-4">ran</span> <span class="custom-4">for</span> <span class="underline">8</span> <span class="custom-4">seconds</span> <span class="custom-5">.</span> <span class="custom-4">Pushing</span> <span class="custom-4">respawn</span> <span class="custom-4">out</span> <span class="custom-4">by</span> <span class="underline">2</span> <span class="custom-4">seconds</span> <span class="custom-5">.</span>
<span class="custom-2">Apr</span> <span class="custom-2">8</span> <span class="bold"><span class="custom-2">10</span></span> <span class="bold"><span class="custom-2">10</span></span> <span class="bold"><span class="custom-2">18</span></span> <span class="custom-1">Js-MacBook-Pro.local</span> <span class="custom-3">MUpdate</span> <span class="custom-5">[</span> <span class="underline">69707</span> <span class="custom-5">]</span> <span class="custom-5">:</span> <span class="custom-4">Endpoint</span> <span class="custom-4">at</span> <span class="custom">'/Applications/Meeting.app'</span> <span class="custom-4">is</span> <span class="custom-4">latest</span> <span class="custom-4">version</span> <span class="custom-5">(</span> <span class="underline">4732</span> <span class="custom-5">)</span> <span class="custom-5">,</span> <span class="custom-4">skipping</span> <span class="custom-5">.</span>
<span class="custom-2">Apr</span> <span class="custom-2">8</span> <span class="bold"><span class="custom-2">10</span></span> <span class="bold"><span class="custom-2">10</span></span> <span class="bold"><span class="custom-2">18</span></span> <span class="custom-1">Js-MacBook-Pro.local</span> <span class="custom-3">MUpdate</span> <span class="custom-5">[</span> <span class="underline">69707</span> <span class="custom-5">]</span> <span class="custom-5">:</span> <span class="custom-4">Next</span> <span class="custom-4">Update</span> <span class="custom-4">Check</span> <span class="custom-4">at</span> <span class="custom-2">2016</span> <span class="custom-2">04</span> <span class="custom-2">09</span> <span class="bold"><span class="custom-2">02</span></span> <span class="bold"><span class="custom-2">22</span></span> <span class="bold"><span class="custom-2">03</span></span> <span class="bold"><span class="custom-2">+0000</span></span>
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">rosie-pattern-language$ </span></span>
</pre>

A few things to notice:
- The CLI automatically executes `import all` upon seeing use of the pattern
  `all.things`.  Files of RPL code must explicitly include the `import X`
  statement to use patterns from package `X`.
- The output style is `color`, which is the default for the `match` command.
  The default output style for the `grep` command is to output every line that
  matches, like the Unix `grep` does.
- Pattern names from the standard library are assigned default color and font 
  styles.  Soon these will be customizable.
  
The `rosie list` command will show the patterns loaded, and what color, if any,
has been assigned.  To see patterns in the `network` packages, you have to tell
rosie to import that package:

<pre>
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">rosie-pattern-language$ </span></span><span class="comint-highlight-input">bin/rosie --rpl 'import net' list net.*</span>
Rosie 1.0.0-alpha-6(candidate)

Name                           Cap? Type       Color           Source
------------------------------ <span class="comment">----</span> <span class="comment">----------</span> <span class="comment">---------------</span> <span class="comment">------------------------------</span>
$                                   pattern    red (default)   
.                                   pattern    red (default)   
MAC                            Yes  pattern    underline;green ...attern-language/rpl/net.rpl
MAC_cisco                      Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
MAC_common                     Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
MAC_windows                    Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
^                                   pattern    red (default)   
any                            Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
authority                      Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
authpath                       Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
ci                                  macro                      
email                          Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
error                               function                   
find                                macro                      
findall                             macro                      
first                               macro                      
fqdn                           Yes  pattern    red             ...attern-language/rpl/net.rpl
fqdn_strict                    Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
fqdn_strict_alias                   pattern    red (default)   ...attern-language/rpl/net.rpl
halt                                pattern    red (default)   
host                           Yes  pattern    red             ...attern-language/rpl/net.rpl
http_command                   Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
http_command_name              Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
http_version                   Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
ip                             Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
ip_literal                     Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
ipv4                           Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
ipv6                           Yes  pattern    red;underline   ...attern-language/rpl/net.rpl
ipv6_mixed                          pattern    red (default)   ...attern-language/rpl/net.rpl
keepto                              macro                      
last                                macro                      
message                             function                   
name                           Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
path                           Yes  pattern    green           ...attern-language/rpl/net.rpl
port                           Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
registered_name                Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
scheme                         Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
uri                            Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
url                            Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
userinfo                       Yes  pattern    red (default)   ...attern-language/rpl/net.rpl
~                                   pattern    red (default)   

41/41 names shown
<span class="comint-highlight-prompt">rosie-pattern-language$ </span></pre>


Another way to explore the RPL standard library is to examine the files in the
`rpl` directory.  In each file, you'll find comments and test cases that show
what kinds of input each pattern is expected to accept and reject.


## Remember to start at the beginning!

There are a small number of important differences between Rosie expressions
([PEGs](https://en.wikipedia.org/wiki/Parsing_expression_grammar), generally)
and regex.  The one that trips up people who are most familiar with regex is
that PEGs start matching at the _first character of the input_.

<pre>
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">rosie-pattern-language$ </span></span><span class="comint-highlight-input">bin/rosie -o line match '"brown"' test/quick.txt </span>
brown fox in field wants to sleep
brown fox in brush wants to sleep
<span class="comint-highlight-prompt">rosie-pattern-language$ </span>
</pre>

To find all the lines in `test/quick.txt` that contain the word "brown" anywhere
in the line, Rosie has a `grep` command:

<pre>
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">rosie-pattern-language$ </span></span><span class="comint-highlight-input">bin/rosie grep '"brown"' test/quick.txt </span>
the quick brown
the quick brown fox
the quick brown fox jumped over the lazy (but adorable) dog
brown fox in field wants to sleep
brown fox in brush wants to sleep
<span class="comint-highlight-prompt">rosie-pattern-language$ </span></pre>

<blockquote>
<h3>Aside</h3>

In case you are curious about how Rosie's `grep` command is implemented, it is
equivalent to applying the `findall` macro to the pattern argument and using the
`match` command.  (And specifying the `line` output format, which is the default
for `grep`.)

<pre>
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">rosie-pattern-language$ </span></span><span class="comint-highlight-input">bin/rosie -o line match 'findall:"brown"' test/quick.txt </span>
the quick brown
the quick brown fox
the quick brown fox jumped over the lazy (but adorable) dog
brown fox in field wants to sleep
brown fox in brush wants to sleep
<span class="comint-highlight-prompt">rosie-pattern-language$ </span></pre>

Peeling away one more layer, the `findall` macro is a repetitive form of the
`find` macro, which takes a pattern argument and does essentially this:
<em>While not looking at the target pattern, consume a character and repeat.
Finally, match the target pattern.</em>

<pre>
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">rosie-pattern-language$ </span></span><span class="comint-highlight-input">bin/rosie -o line match '{!"brown" .}* "brown"' test/quick.txt </span>
the quick brown
the quick brown fox
the quick brown fox jumped over the lazy (but adorable) dog
brown fox in field wants to sleep
brown fox in brush wants to sleep
<span class="comint-highlight-prompt">rosie-pattern-language$ </span></pre>

</blockquote>

## Experiment at the CLI or the REPL

### The Rosie CLI

Here are some suggestions for experimenting on your own data using the Rosie CLI.

- Use `match all.things` to see which items within your data are already
  recognized by Rosie.
- Switch to `grep <pat>` to find specific items, e.g. use `date.any` or
  `net.any` for `<pat>`.
- Add `-o color` to your command to make the output easier to read.  (The
  default for Rosie `grep` is to simply echo the matching lines, like Unix
  `grep` does.)
- Compose a pattern on the command line.  Don't forget to enclose the pattern in
  single quotes to shield it from interpretation by the shell!
- Change the output option to `-o json` to see the structure in the matches.
  Pipe the output into a json pretty-printer to increase readability.
  
<style type="text/css">
    <!--
      body {
        color: #000000;
        background-color: #ffffff;
      }
      .bold {
        /* bold */
        font-weight: bold;
      }
      .comint-highlight-input {
        /* comint-highlight-input */
        font-weight: bold;
      }
      .comint-highlight-prompt {
        /* comint-highlight-prompt */
        color: #0000cd;
      }
      .comint-highlight-prompt {
        /* comint-highlight-prompt */
        color: #0000cd;
      }
      .comment {
        /* font-lock-comment-face */
        color: #888088;
      }
      .custom {
        /* (foreground-color . "cyan3") */
        color: #00cdcd;
      }
      .custom-1 {
        /* (foreground-color . "blue2") */
        color: #0000ee;
      }
      .custom-2 {
        /* (foreground-color . "black") */
        color: #000000;
      }

    -->
    </style>
<pre>
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">rosie-pattern-language$ </span></span><span class="comint-highlight-input">bin/rosie grep ts.any test/logfile </span>
Apr  8 09:42:24 Js-MacBook-Pro com.apple.xpc.launchd[1] (homebrew.mxcl.kafka[68878]): Service exited with abnormal code: 1
Apr  8 09:42:24 Js-MacBook-Pro com.apple.xpc.launchd[1] (homebrew.mxcl.kafka): Service only ran for 8 seconds. Pushing respawn out by 2 seconds.
Apr  8 10:10:18 Js-MacBook-Pro.local MUpdate[69707]: Endpoint at '/Applications/Meeting.app' is latest version (4732), skipping.
Apr  8 10:10:18 Js-MacBook-Pro.local MUpdate[69707]: Next Update Check at 2016-04-09 02:22:03 <span class="comment">+0000</span>
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">rosie-pattern-language$ </span></span><span class="comint-highlight-input">bin/rosie -o color grep 'ts.any id.any' test/logfile </span>
<span class="custom-1">Apr</span> <span class="custom-1">8</span> <span class="bold"><span class="custom-1">09</span></span> <span class="bold"><span class="custom-1">42</span></span> <span class="bold"><span class="custom-1">24</span></span> <span class="bold"><span class="custom">Js-MacBook-Pro</span></span>
<span class="custom-1">Apr</span> <span class="custom-1">8</span> <span class="bold"><span class="custom-1">09</span></span> <span class="bold"><span class="custom-1">42</span></span> <span class="bold"><span class="custom-1">24</span></span> <span class="bold"><span class="custom">Js-MacBook-Pro</span></span>
<span class="custom-1">Apr</span> <span class="custom-1">8</span> <span class="bold"><span class="custom-1">10</span></span> <span class="bold"><span class="custom-1">10</span></span> <span class="bold"><span class="custom-1">18</span></span> <span class="bold"><span class="custom">Js-MacBook-Pro</span></span> <span class="bold"><span class="custom">local</span></span>
<span class="custom-1">Apr</span> <span class="custom-1">8</span> <span class="bold"><span class="custom-1">10</span></span> <span class="bold"><span class="custom-1">10</span></span> <span class="bold"><span class="custom-1">18</span></span> <span class="bold"><span class="custom">Js-MacBook-Pro</span></span> <span class="bold"><span class="custom">local</span></span>
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">rosie-pattern-language$ </span></span><span class="comint-highlight-input">bin/rosie -o color grep 'ts.any id.any find:ts.any' test/logfile </span>
<span class="custom-1">Apr</span> <span class="custom-1">8</span> <span class="bold"><span class="custom-1">10</span></span> <span class="bold"><span class="custom-1">10</span></span> <span class="bold"><span class="custom-1">18</span></span> <span class="bold"><span class="custom">Js-MacBook-Pro</span></span> <span class="bold"><span class="custom">local</span></span> <span class="custom-1">2016</span> <span class="custom-1">04</span> <span class="custom-1">09</span> <span class="bold"><span class="custom-1">02</span></span> <span class="bold"><span class="custom-1">22</span></span> <span class="bold"><span class="custom-1">03</span></span> <span class="bold"><span class="custom-1">+0000</span></span>
<span class="comint-highlight-prompt">rosie-pattern-language$ </span></pre>

### The Read-Eval-Print Loop (REPL)

If you have developed in Lisp or Scheme, you have seen the power of the REPL as
a development tool.  Even Python supports a REPL these days to enable
incremental code development.  And so does Rosie.

There are three things you can enter at the `Rosie>` REPL prompt:

- Commands, like `.match`, `.trace`, and `.load`;
- RPL statements, e.g. definitions like `d = [:digit:]`; and
- RPL identifiers (to see their definitions).

<pre>
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">rosie-pattern-language$ </span></span><span class="comint-highlight-input">bin/rosie repl</span>
Rosie 1.0.0-alpha-6
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">Rosie&gt; </span></span><span class="comint-highlight-input">d</span>
Repl: undefined identifier d
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">Rosie&gt; </span></span><span class="comint-highlight-input">d = [:digit:]</span>
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">Rosie&gt; </span></span><span class="comint-highlight-input">d</span>
[:digit:]
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">Rosie&gt; </span></span><span class="comint-highlight-input">.match d "4"</span>
{"data": "4", 
 "e": 2, 
 "s": 1, 
 "type": "d"}
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">Rosie&gt; </span></span><span class="comint-highlight-input">.match d+ "4321"</span>
{"data": "4321", 
 "e": 5, 
 "s": 1, 
 "subs": 
   [{"data": "4", 
     "e": 2, 
     "s": 1, 
     "type": "d"}, 
    {"data": "3", 
     "e": 3, 
     "s": 2, 
     "type": "d"}, 
    {"data": "2", 
     "e": 4, 
     "s": 3, 
     "type": "d"}, 
    {"data": "1", 
     "e": 5, 
     "s": 4, 
     "type": "d"}], 
 "type": "&#857;"}
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">Rosie&gt; </span></span><span class="comint-highlight-input">import net</span>
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">Rosie&gt; </span></span><span class="comint-highlight-input">net</span>
&lt;environment: 0x7fa00a7b54c0&gt;
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">Rosie&gt; </span></span><span class="comint-highlight-input">net.ipv4</span>
{ipv4&lowbar;component &lbrace;{"." ipv4&lowbar;component} {"." ipv4&lowbar;component} {"." ipv4&lowbar;component}}}
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">Rosie&gt; </span></span><span class="comint-highlight-input">.match net.ipv4 "192.67.1.100"</span>
{"data": "192.67.1.100", 
 "e": 13, 
 "s": 1, 
 "type": "net.ipv4"}
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">Rosie&gt; </span></span><span class="comint-highlight-input">.match findall:net.ipv4 "Hello 192.67.1.100"</span>
{"data": "Hello 192.67.1.100", 
 "e": 19, 
 "s": 1, 
 "subs": 
   [{"data": "192.67.1.100", 
     "e": 19, 
     "s": 7, 
     "type": "net.ipv4"}], 
 "type": "*"}
<span class="comint-highlight-prompt"><span class="comint-highlight-prompt">Rosie&gt; </span></span>
Exiting
<span class="comint-highlight-prompt">rosie-pattern-language$ </span></pre>


Note that sample data for the `match` and `trace` commands must be enclosed in
double quotes.

Using the REPL is a good way to develop RPL patterns.  Because Rosie is happy to
match just a portion of the input data (starting at the first character), you
can begin with a pattern that matches just the first item in the data, and then
extend the pattern incrementally to match more and more of the sample input.


## Coming up: Rosie and Python

In a forthcoming post, I'll show how to call Rosie from Python using `rosie.py`,
which uses `librosie.so`.

## Discussion on reddit

A [Rosie subreddit](https://www.reddit.com/r/RosiePatternLanguage/) has been
created for discussion of these posts and for questions about Rosie and RPL.
See you there!

<hr>

Follow us on [Twitter](https://twitter.com/jamietheriveter) for announcements
about the RPL approach to #[modernpatternmatching](https://twitter.com/search?q=%23modernpatternmatching).




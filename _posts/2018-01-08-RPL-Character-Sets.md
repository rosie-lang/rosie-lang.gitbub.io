---
layout: post
title:  "RPL Character Sets: <br>Going beyond (around, through) regex"
date:   2018-01-08
categories: 
---

The character set syntax in Rosie Pattern Language fixes some of the usability
issues with regex character sets, and then goes beyond what some (but not all)
regex solutions offer today.  In this post, we cover RPL character sets as
implemented in
[Rosie v1.0.0-alpha-8](https://github.com/jamiejennings/rosie-pattern-language/releases/tag/v1.0.0-alpha-8).

Note: At the time of this writing (2018-01-07), the RPL documentation does not
include discussion of the new features described here.  That will be remedied
shortly. 

## Character sets in regex

Regex solutions have a concise way of specifying a set of characters, any one of
which will be matched.  This is the _character set syntax_ (sometimes called
_bracket expressions_) and is familiar in expressions like `[0-9]` and `[+-=*/]`
and `[:space:]`.

The first example, `[0-9]`, is a _character range_; `[+-=*/]` is a _character
list_, and `[:space:]` is a _named character set_.

Perhaps you have already spotted the error in `[+-=*/]`?  It is a valid Posix
regular expression, but it is not simply a list of characters to match.  The
dash (or minus sign) is special in a character set: it indicates a range. So,
there's a flaw in our example of a character _list_.  A correct example of a
list of 5 characters is `[-+=*/]`, in which the dash does not indicate a range.

Our broken example shows another aspect of regex character sets: they may
include ranges and individual characters mixed together.  Indeed, `[+-=*/]` is
parsed as the range `[+-=]` and the list `[*/]`.

The ability to combine ranges and lists gives a very compact notation, but in our
opinion, it too easily permits mistakes.  When we see an expression like
`[+-=*/]`, we don't know whether the author intended to write a combined range
and list, or whether they forgot that `-` was a magic character in this context.

Suppose the author intended to write a list of 5 characters.  It is awkward that
their mistake (which accidentally includes a range) is valid in regex.  Even
worse is that, at first glance, it appears to work as intended!

```shell 
$ echo 'ABCD -+*/ !@#' | egrep -o '[+-=*/]'
-
+
*
/
$ echo 'y = mx + b' | egrep -o '[+-=*/]'
=
+
$ echo 'y/z = (m*x + b)/z' | egrep -o '[+-=*/]'
/
=
*
+
/
$ 
``` 

But, of course, the accidental range `[+-=]` accepts many other characters:

```shell 
$ echo 'y < mx + b' | egrep -o '[+-=*/]'
<
+
$ echo 'y = (-b +- sqrt(b^2)-4ac)/2a' | egrep -o '[+-=*/]'
=
-
+
-
2
-
4
/
2
$ 
```

If the author did not intend this character set to accept `<` and numbers like
`2` and `4`, the tests above would be very surprising.

In the next section, we will look at how RPL avoids this pitfall, making it
harder to accidentally write something you did not intend, while making it
easier to read and understand RPL character sets without consulting a manual.

Note: We will return to the topic of _named character sets_ in a later section.

## Character sets in RPL

### Design point: Always escape the magic characters

In an RPL character set, there are five "magic" characters: `\ [ ] ^ -`

- `\` (backslash) is the universal escape character in RPL;
- `[`, `]` (open and close brackets) start and end a character set, respectively;
- `^` (caret) changes the meaning to the complement of the set being defined;
- `-` (dash) sits between the first character and the last character of a range.

You cannot write `[+-=*/]` in RPL because the dash is magic in a character
set.  When Rosie sees an unescaped dash, it expects that you are constructing a
range.  Escaping the dash (writing `\-`) tells Rosie that you are using the dash
as an ordinary character.

```shell
$ echo 'y = mx + b' | rosie -o subs grep '[+-=*/]'
Syntax error
	[parser]: invalid character range edge (not a single character): =*/
	in user input :1:2: [+-=*/]
$ echo 'y = mx + b' | rosie -o subs grep '[+\-=*/]'
=
+
$ echo 'y < mx + b' | rosie -o subs grep '[+\-=*/]'
+
$ 
```

A different design choice, instead of requiring escaping, would be to allow
magic characters in non-magic positions.  This is the regex solution, and it
requires memorizing many rules, e.g.

> To include a literal <strong>]</strong> in the list, make it the first character (following
> a possible <strong>^</strong>).  To include a literal <strong>-</strong>, make it the first or last
> character, or the second endpoint of a range.  To use a literal <strong>-</strong> as the
> first endpoint of a range, enclose it in <strong>[.</strong> and <strong>.]</strong> to make it a
> collating element (see below).  With the exception of these and some
> combinations using <strong>[</strong> (see next paragraphs), all other special characters, <!-- ] -->
> including <strong>\\</strong>, lose their special significance within a bracket expression.  
> <em>(From the OS X man page, in section 7, of re_format, POSIX 1003.2 regular expressions.)</em>

I don't have the patience to quote the rest of that man page, about which
characters can go where, and how their position changes the meaning of the
expression.  There are too many rules to keep in mind all of the time.  We think
the RPL rule is simpler: _Always escape the magic characters._

Note: A complete description of character escape syntax in RPL is included in an
[appendix](#appendix) to this post.

### Design point: Combine character sets explicitly

In RPL, a character set can be a range, a list, or a named character set, or an
_explicit combination_ of character sets.  (Regex combine ranges and lists
implicitly by putting them adjacent to one another.)  Character sets are
combined explicitly in RPL by including them in an outer pair of brackets:

- `[[0-9][A-F]]` is an explicit combination of two ranges, `[0-9]` and `[A-F]`,
  and matches a single character in either range;
- `[[0-9] [A-F]]` is the same combination, because the outer square brackets
  function as an RPL grouping construct, inside of which are other valid RPL
  expressions (and whitespace is ignored between expressions);
- `[ [0-9] [+\-\[\]] ]` combines the range `[0-9]` and the list of `+`, `-`,
  `[`, and `]`; note that the magic characters are escaped, and that whitespace
  can be used to make this expression a little easier to read.

There is more power in these RPL _bracket expressions_ than is shown in the
examples above.  We will return to this topic in the section on
[Bracket Expressions](#brackets) below.  For now, we point out that the extra
typing required by this design choice is offset by the resulting clarity.  We
expect it to be much easier for a human to read and understand character sets
when they are made of simple ranges, lists, and named sets which are then
explicitly combined.

### Design point: Don't repeat characters

Regex allows a character to appear multiple times in a list, e.g. `[+-=*/*/*/]`.
RPL does not allow this, because it facilitates mistakes such as using
`[:alpha:]` in regex instead of `[[:alpha:]]`.  The former is a list of 5
characters (:, a, l, p, and h).  The latter is a named posix character set that
matches alphabetic characters in the current locale.

RPL allows named character sets without the double brackets.  `[:alpha:]` is
valid RPL and is the expected posix character set, not a character list.  By
prohibiting repeated characters, RPL can:

- assume that when the user writes `[:X:]`, they intend to refer to a named
  character set, with name `X`;
- extend the collection of named character sets beyond the posix ones, by
  allowing new names beyond the posix ones to replace `X` in `[:X:]`; see
  [one proposed idea](#DesignQuestion) below;
- catch some copy/paste, typographical and other errors that would go
  unnoticed if duplicate characters were allowed.

It is easy to dismiss the value of catching some inadvertent mistakes, like
typos and copy/paste.  But programming languages have a long history of design
decisions that were later regretted because such mistakes produced valid code
which did not do what the author intended.  (More in [the end note](#EndNote) below.)

### Design point: Write ranges in order

Related in spirit to not repeating characters in lists is to write character
ranges in order of increasing codepoint value.  When specifying a range,
particularly in a Unicode context, with over a million possible characters, the
RPL compiler can catch some mistakes by ensuring the start of the range is left
of the dash, and the end of the range on the right.  So `[A-Z]` and `[+-=]` are
valid, but `[Z-A]` and `[=-+]` will cause compiler errors.

In addition, RPL ranges must contain at least two characters.  There is no
important reason to allow `[A-A]` in RPL when the `[A]` could be used instead,
and is more clear.

### Summary

The syntax of RPL exists in a tension between embracing the familiar syntax of
regular expressions and, with decades of hindsight, creating something more,
well, _regular_.  That is, we want RPL to be a language based on a few concepts,
with a clear syntax for each one, and a few ways for combining them.

We want to reduce the developer's
[cognitive load](https://en.wikipedia.org/wiki/Cognitive_load).  A technology
that comes with many rules, and, worse, many exceptions to the rules, imposes a
high cognitive load and facilitates mistakes.

The RPL design points discussed above for character sets, or _bracket
expressions_, are meant to keep things simple for the programmer while allowing
the compiler to help find errors.


## <a id="brackets" />RPL Bracket Expressions

Now that we have covered the ways in which RPL simplifies character set syntax,
we can show how the resulting simple forms of _range_, _list_, and _named set_
can be combined in powerful ways. 

First, an observation: Character sets are disjunctions.  A character list like
`[abc]` matches `a` or `b` or `c`.  A compound set like `[[0-9][A-F]]` matches a
character in either range `[0-9]` or `[A-F]`.  This presents an opportunity.

We already have two grouping constructs in RPL: parentheses group expressions to
be matched with a boundary in between them, and curly braces group expressions
to be matched with no boundary.  (I like to imagine the curly braces like the
jaws of [pliers](https://en.wikipedia.org/wiki/Pliers), squeezing the
expressions tightly together.)  The fact that brackets suggest disjunction is an
opportunity to make them a third grouping construct:

- `{e1 e2 ... en}` === `e1 e2 ... en`, i.e. a sequence of expressions
- `(e1 e2 ... en)` === `e1 ~ e2 ~ ... ~ en`, where `~` matches a token boundary
- `[e1 e2 ... en]` === `e1 / e2 / ... / en`, where `/` is the ordered choice operator

As language designers, we ask _What does it mean to say that brackets are a
grouping construct in RPL?_ It means that brackets behave very much like
parentheses and braces.  It means that the expressions `e1` ... `en` can be any
RPL expressions.  It means that extra layers of brackets around an expression do
not change its meaning.

Can we make these intentions true?

The answer is _yes_, provided we can resolve a syntactic ambiguity.  We choose
to regard `[abc]` as a list of 3 characters and not a bracket expression
containing the identifier `abc`.  Similarly, `[a b]` is a list of 3 characters,
and not the disjunction of the patterns named `a` and `b`.

As much as we loathe inconsistencies and exceptions to rules, we remember that
sometimes "the perfect is the enemy of the good", and we continue on.  If we
accept the simple forms of character sets as being, in some sense, atomic, then
we can have brackets as a grouping construct.  The following are valid RPL (as
of version 1.0.0-alpha-8):

- `[1234]` is a character list containing 4 characters
- `[[1234]]` is the same list of 4 characters
- `[[[[[1234]]]]]` is the same list of 4 characters
- `[:alpha:]` is the posix named character set "alpha"
- `[[:alpha:]]` is the same named character set
- `[[[[[:alpha:]]]]]` is the same named character set
- `[]` is an empty character set that will not match any character
- `[[1234] foo]` === `[1234] / foo`, where `foo` is an RPL identifier bound to a pattern
- `[[] foo bar]` === `[] / foo / bar` === `foo / bar`, for identifiers `foo` and `bar`
- `[[] "hi" "bye"]` === `[] / "hi" / "bye"` === `"hi" / "bye"`

Interestingly, the RPL expressions `foo`, `bar`, `"hi"`, and `"bye"` are
(clearly) not restricted matching exactly one character.  While the simple
character sets match exactly one character in a _range_, a (non-empty) _list_,
or a _named set_, the RPL _bracket expressions_ are more general.

In a section below, we will preview the forthcoming
[Unicode character classes](#UnicodeClasses), which present a use case for
expressions like `[[abcd] foo]`.  That is, provided we can bind `foo` to a set
of Unicode characters that have a particular property.  It remains to be seen if
there are use cases where `foo` is an expression that matches more than one
character.  It's even possible that creating such general _bracket expressions_
will be a decision later regretted.


## Bracket expressions and the & operator

In a recent alpha release, we quietly introduced the RPL `&` operator (called
"and").  This operator may be defined in terms of existing RPL functionality, so
it adds no new capability.  It does, however, provide a mellifluous syntax for
combining character sets.

When we think of character sets (as opposed to the more general _bracket
expressions_), we do indeed think of sets in the classical sense.  To construct
a particular set, we might apply the operations of union, intersection, and
difference to other sets.  Or we might take the complement of a set.

How do these operations look in RPL?

### Intersection

We have already seen set union.  It is the "or" that defines the meaning of a
_bracket expression_.  So let's turn to the title of this section, the `&`
operator, which implements set intersection.

- `[[:xdigit:] & [A-Z]]` denotes the set intersection of the posix set `xdigit`
  and the uppercase letters `A` through `Z`.  This expression is the equivalent
  of `[A-F]`.
- `[[p] [:xdigit:] & [A-Z]]` means either `p` or the set intersection as described
  above.  As with the rest of RPL, expressions are right associative, and binary
  operators have equal precedence.
- `[[:xdigit:] & [A-Z] [p]]` denotes the intersection of `xdigit` with the union
  of `[A-Z]` and `[p]`.
- `[ [[:xdigit:] & [A-Z]] [p] ]` denotes the union of the intersection of
  `xdigit` with `[A-Z]`, and `[p]`.  It will match `A-F` or `p`.
- `[[:xdigit:] & [A-Z] & [p]]` is the intersection of 3 sets which, in this
  case, happens to be empty, and thus equivalent to `[]`, which will not match
  any input.

Outside of a bracket expression, `&` works just the same.  With any RPL pattern,
even those that match multi-character sequences, `&` works just the same.  You
may have guessed a definition of the `&` operator that can yield this behavior.
It is:

    e & f === >e f

In other words, the intersection of two patterns, `e` and `f`, is the same as
`>e` (look ahead at pattern `e`) followed by `f` (match pattern `f`).

For expressions that match a single character, i.e. character sets, `>e f`
succeeds when the next input character is in `e` (so the look ahead succeeds)
and also in `f`.  

For generic expressions `e` and `f`, the meaning depends, of course, on the
nature of those two patterns.  But the definition of `&` is clear.  It is
defined in terms of the RPL operators look-ahead (`>`) and sequence (denoted by
adjacency).  

### Complement

As in regex, character set complement is denoted using the caret, `^`, inside the
brackets.  So `[^0-9]` matches a single character that is not one of the digits
`0` through `9`.  Adopting the Perl syntax for the complement of named character
sets yields a good notation (surprisingly) .  So `[:^digit:]` matches a
single character which is not in the posix `digit` set.

Clearly, we can use `^` to denote the complement of a simple character set, like
a _range_, _list_, or _named set_.  But can we specify the complement of a
generic bracket expression?

Yes.  `[^ [[:xdigit:] & [A-Z]] [p]]` matches a character that is not `[A-F]` and
not `p`.  

What does `[^ ...]` mean when there are expressions inside the brackets that
match multi-character strings?  For example, what does `[^ [A-Z] "Hi" ]` mean?

First, let's examine what the expression means if we omit the complement:

> `[[A-Z] "Hi"]` === `[A-Z] / "Hi"`, meaning that it matches either a single
>  character in the range `A-Z` or the literal string `Hi`.  
  
The RPL expression `[^e]` matches a single character that is not in the set
denoted by `e`, when `e` is a set.  Extending this definition to generic bracket
expressions is straightforward: if the input would match `e`, then `[^e]` fails,
else consume a character and continue.

> `[^e]` === `{!e .}`

Recall that `!e` in RPL is read as "not e", and that

> `!e` === `!>e`, which means "not looking ahead at `e`".

Therefore,

> `[^e]` === `{!e .}`
> <br>`[^ e1 e2 ... en]` === `{ !{e1 / e2 / ... / en} . }`
> <br>`[^ e1 & e2]` === `{ !{e1 & e2} . }` === `{ !{>e1 e2} . }`

It is significant that the RPL compiler uses the definition of `.` when compiling a
complemented bracket expression.  The default definition of "dot" matches a
single Unicode character or, failing that, a single byte.  But you can change
the definition of dot within an RPL file.  This capability proves useful in
certain circumstances, such as when defining an ASCII-only package of RPL
patterns, or a package of patterns for parsing binary data (where dot must match
only a single byte of any value 0-255).


### Difference

Within bracket expressions, we have seen set union (denoted by adjacency),
intersection (denoted by `&`), and complement (`^`).  We resisted the temptation
to include a "minus sign" operator in RPL for set difference.  Instead, when you
want the set difference between `X` and `Y`, you write:

> `[X & [^Y]]`, meaning "in set X and not in set Y" when X, Y are character sets

This has the expected generic definition in RPL:

> `[X & [^Y]]` === `{>X [^Y]}` === `{>X {!Y .}}`

In other words, the "set difference of X and Y" means "a character in X that is not
in Y", and is written in RPL as "matches X and the complement of Y".  If we read
this again with arbitrary patterns `e` and `f` in mind, then we have:

> `[e & [^f]] === { >e {!f .} }`

which means:

>  "look ahead at `e`, and then:
> <br> fail if we look ahead seeing `f`, but otherwise we consume a character and continue on.
  
This is, admittedly, an odd expression.  Perhaps it will not have much use
generically, and will prove useful only when the expressions are character
sets. So be it.  What is important is that the concept of set difference is (1)
expressible in RPL with reasonable concision, and (2) generalizes to combine
arbitrary RPL expressions, for consistency across the language.

Next, we will take a moment to preview a forthcoming feature, before wrapping up
this long post.



## <a id="UnicodeClasses" />Unicode character classes (forthcoming)

Full Unicode support in Rosie (for UTF-8 encoded input) is almost complete.
This is the current state of affairs:

- The dot (`.`) matches a single Unicode character (or, failing that, a single
  byte).
- UTF-8 encoded Unicode characters may appear in string literals and character
  sets.
- A Unicode character may be written, in a string or character set, using one of
  two escape sequences, \u and \U (see [the appendix](#appendix) below).
  
What is missing, but coming soon, is the ability to specify a character set that
contains exactly the Unicode characters which have a given property.  For
example, each of these is a character set based on the Unicode specification:

- characters in the `Greek` script;
- characters in the category `uppercase`;
- characters in the category `punctuation`; and
- characters designated as `White_Space`.

The [Unicode standard](http://unicode.org) defines these properties.  We merely
wish to reference them in order to construct useful characters sets for
matching.  

Some regex implementations, like the ones in Java and Perl, provide a notation
for the set of characters in Unicode category `L` that looks like:

> `\pL` or `\p{L}`, or sometimes `\p{IsL}` or `\p{InB}` if `B` is
> the name of a Unicode "block"

> and an uppercase `\PL` (or sometimes `\p{^L}`) for the complement set.

Across different regex implementations, various forms of this syntax are
supported or not, and for various Unicode properties or not.  Naturally, we see
an opportunity to have a more regular, less _ad hoc_ approach in RPL.  We are
working on the following approach.

### Unicode character classes in RPL libraries

We will extend the set of standard libraries that ship with RPL to include
packages defining sets of characters that possess each Unicode property that we
wish to support.  As with any RPL library, these can be imported, giving a set
of named patterns.

One possible arrangement of the libraries and pattern names is:

- `Unicode/Script.rpl` defines 140 patterns, each named after a Unicode script,
  e.g. `Latin`, `Thai`, and `Cyrillic`.
- `Unicode/Block.rpl` defines 280 patterns, one for each Unicode block.
- `Unicode/Property.rpl` defines over 30 patterns, one for each Unicode property,
  e.g. `Lu` (uppercase letter), `M` (combining mark), and `N` (number).
- And so on, for all supported properties.

If we follow through with this arrangement, then the resulting character sets
might be used as follows:


```
import Unicode/Script, Unicode/Category
 
thai_or_lao = Script.Thai / Script.Lao
thai_word = Script.Thai+
thai_upper = Script.Thai & Category.Upper
```

As you can see, bracket expressions are not needed in order to use these
patterns.  Of course, they could be used, whether for convenience or to signal
intent to the reader.

The implementation of the Unicode libraries is well underway as of this writing
(2018-01-07), but we are very interested in feedback on the approach.  Please
post comments and suggestions in the
[Rosie subreddit](https://www.reddit.com/r/RosiePatternLanguage/).


### <a id="DesignQuestion" />A design question

We end this section with a design question.  Given the previous section, where
we describe libraries of Unicode patterns, do we need to go further?  Should RPL
support named character sets which correspond to the patterns for Unicode properties?

We currently support the posix sets, which are written `[:alpha:]`, for
example.  Should we also support `[:Thai:]` or `[:Script=Thai:]` as an
alternative syntax for `Script.Thai` from the example above?

One benefit of such a syntax is that it unifies posix sets with Unicode sets,
giving a uniform look (and thus, recognizability) to both.  However, there are
costs.

RPL does not have a concept of "automatic" imports.  (The CLI does this, when
possible, as a convenience for command-line use only.  But the CLI is a tool
that should be considered part of the Rosie project, independent of RPL as a
language specification.)  A design principle in RPL is to make dependencies
visible, which suggests that to use `[:Script=Thai:]` in an RPL file, that file
must `import` something.  But, what?  The package `Unicode/Script` seems
logical, but it requires the programmer to remember to include `Unicode` in the
import path, which is a bit awkward.  Or, should we consider Unicode character
sets to be built in, the way the posix sets are today (with no import needed)?

What do you think?  Anyone who has read this far probably
has an opinion, and we'd like to hear it.  Please post comments and suggestions
in the [Rosie subreddit](https://www.reddit.com/r/RosiePatternLanguage/).


## Conclusion

This post described a number of new features in RPL, for which documentation is
still being written.  We described the design points behind these features, and
our hopes for a definition of RPL that ultimately imposes a lower cognitive load
than other pattern matching technologies.  (We understand that when RPL and
[PEGs](https://en.wikipedia.org/wiki/Parsing_expression_grammar) are new to a
user, there is a learning curve.)

Features like the RPL grouping constructs are orthogonal and idempotent.  Set
operations are supported clearly and directly (except that set difference does
not have its own operator).  Requirements for escape sequences are uniform, and
violations are explained in compiler error messages.  (See the
[appendix on escape sequences](#appendix) below for more on that.)

Finally, we presented a piece of work that is not yet finished (Unicode
character sets), and a possible extension of that work (merging the Unicode
character sets with the posix ones into a uniform syntax).


## <a id="reddit" />Discussion on reddit

A [Rosie subreddit](https://www.reddit.com/r/RosiePatternLanguage/) has been
created for discussion of these posts and for questions about Rosie and RPL.
See you there!

<hr>
## <a id="EndNote" />End note on programming language design flaws

Detecting mistakes, including typographical errors and copy/paste errors, is a
great aid to programmers.  To allow an RPL expression
that looks like one thing but is really another is to introduce a flaw.  Every
design has flaws, but why would we add one knowingly?

An analogous design flaw to allowing duplicate characters in lists, or
out-of-order ranges, is found in programming languages that allow implicit
variable declaration.  They will silently create a new variable when
encountering a misspelling.  Examples include Perl (without `use strict`) and
Lua (though many programmers write a `strict` equivalent).

Search for
[programming language design errors](https://www.google.com/search?q=programming+language+design+errors)
or
[worst software bugs](https://www.google.com/search?client=safari&rls=en&q=worst+software+bugs)
and you'll find cases in which valid code looked (to developers) like one thing,
when it was actually a different thing.  This type of claim is common in
post-mortem analyses:

> "A more structured programming language with stricter compilers would have made
> this particular defect much more obvious."
> <br>
> [All Circuits are Busy Now: The 1990 AT&T Long Distance Network Collapse](http://users.csc.calpoly.edu/~jdalbey/SWE/Papers/att_collapse.html)


<hr>
## <a id="appendix" />Appendix: RPL Escape Sequences

With any language, there are two things you need to know about escape
sequences.  What _can_ I escape, and what _must_ I escape?

### What escape sequences are universal in RPL?

In RPL (as of version 1.0.0-alpha-8), you can use the following "universal"
escape sequences when writing string or character literals:

| RPL syntax | Name | Meaning |
| -----------| -----| --------|
| `\xHH`       | Hex escape | A single byte; where HH is in 00-FF |
| `\uHHHH`     | Unicode escape | The UTF-8 encoding of a Unicode codepoint; HHHH in 0000-FFFF |
| `\UHHHHHHHH` | Long Unicode escape | The UTF-8 encoding of a Unicode codepoint; HHHHHHHH in 00000000-10FFFFFF |
| `\a`, `\b`, `\t`, `\n`, `\f`, `\r` | Subset of [ANSI C escape sequences](https://en.wikipedia.org/wiki/Escape_sequences_in_C) | Codepoints 07 (bell), 08 (backspace), 09 (tab), 0A (newline), 0C (formfeed), 0D (return) |

Rationale: 
1. The RPL hex escape is a variant of the same in ANSI C, except that the RPL
syntax requires exactly two hex digits.  We expect the hex escape to be used
for parsing binary data and for specifying non-characters, such as single bytes
in the range 80-FF.
2. Both Unicode escapes, `\u` and `\U`, are also part of ANSI C, and have been
adopted by other languages as well.  The long form is expected to be needed
rarely, because of the paucity of defined codepoints above FFFF.
3. Several of the ANSI C escape sequences are used much too often to ignore,
particularly tab, newline, and carriage return.  We dropped the vertical tab,
which has fallen into disuse, but kept the bell, backspace, and formfeed
sequences.

### What escape sequences are mandatory in RPL?

In RPL (as of version 1.0.0-alpha-8), the "universal" escape sequences described
above are always available when writing string or character literals.  There are
only a handful of cases in which an escape sequence _must be used_ in order to
refer to the character itself.

**Rule:** | _Always escape the magic characters_
          | The escape character, backslash, is always magic; to get a literal backslash, write `\\`
		  | In a string, the double quote is magic (signaling the end of the string); to put a double quote in a string, write `\"`
		  | In a character set, the magic characters are `[`, `]`, `^`, and `-`; to put any of these into a character range or list, write `\[`, `\]`, `\^`, and `\-`

Rationale:
1. To reduce cognitive load, we try to reduce the number of rules.  Here, there
is essentially one rule, with sub-parts applying to strings, character sets, and
both.
2. Importantly, there are no exceptions to the rule.  The position of a
character in a character set or string is irrelevant to the rule.  Only the
context of being within a string or character set matters.


<hr>

Follow us on [Twitter](https://twitter.com/jamietheriveter) for announcements
about the RPL approach to #[modernpatternmatching](https://twitter.com/search?q=%23modernpatternmatching).



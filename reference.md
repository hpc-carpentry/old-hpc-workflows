---
layout: reference
---

## Glossary

{:auto_ids}
Zipf's Law
: In the field of quantitative linguistics, Zipf's Law states that the
frequency of any word is inversely proportional to its rank in the frequency
table. Thus the most frequent word will occur approximately twice as often as
the second most frequent word, three times as often as the third most
frequent word, etc.: the rank-frequency distribution is an inverse relation
(source: [Wikipedia][zipf]).

Build File
: A build file describes all the steps required to execute or build your code or data.
The format of the build file depends on the build system being used. Snakemake build files are called Snakefiles, and use Python 3 as the definition language.

Dependency
: A file that is needed to build a target. In Snakemake, dependencies are
specified as inputs to a rule.

Target
: A file to be created or built. In Snakemake targets are also called outputs.

Rule
: Describes how to create outputs from inputs. Dependencies between rules are handled
implicitly by matching filenames of inputs to outputs. A rule can also contain no inputs or outputs, in which case it simply specifies a command that can be run manually.
Snakemake rules are composed of inputs, outputs, and an action.

Default Target
: The first rule in a Snakefile defines the *default target*. This is the target
that will be built if you do not specify any targets when running snakemake.

Action
: The part of a rule that specifies the commands to run.

Incremental Builds
: Incremental builds are builds that are optimized so that targets that have
up-to-date output files with respect to their corresponding input files are
not executed.

Directed Acyclic Graph
: A directed acyclic graph (DAG) is a finite graph with no directed cycles.
In the context of Snakemake, it means that you cannot define any circular
dependencies between rules. A rule cannot, directly or indirectly, depend on
itself.

Pattern Rule
: A Snakemake rule that uses wildcard patterns to describe a general rule to
make any output that matches the pattern.

Wildcard
: Wildcards are used in an input or output to indicate a pattern (e.g.: `{file}`).
Snakemake matches each wildcard to the regular expression `.+`, although additional
constraints can be specified. See [the documentation][docs-wildcard] for details.

{% include links.md %}

[zipf]: https://en.wikipedia.org/wiki/Zipf%27s_law
[docs-wildcard]: https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#wildcards
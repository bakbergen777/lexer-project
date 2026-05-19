# Compiler Principles — Lexer Project

**Topic:** Usage of Automatic Construction Tools for Lexical Analysis Programs
**Tool used:** **Flex** (Fast Lexical Analyzer Generator)
**Course:** Compiler Principles, Spring 2026

## Group members

| Name                  | Student ID    |
|-----------------------|---------------|
| Bakbergen Amir        | 202469990559  |
| Bakbergen Alen        | 202469990562  |
| Huang Liu Diego David | 202469990549  |
| Liu Bryan             | 202469990275  |

## What this project does

We use **Flex**, an automatic lexical-analyzer generator, to build a scanner for a small C-like language. The scanner reads a source file and produces a stream of typed tokens (keyword, identifier, integer constant, float constant, string, character, operator, punctuation, comment) with line/column positions. Lexical errors are reported with location.

The Flex specification (`lexer.l`) declares regular expressions for every token category and lets Flex generate a deterministic finite automaton (DFA) that drives a fast C scanner. We never hand-code the DFA.

## File layout

| File                | Purpose                                                       |
|---------------------|---------------------------------------------------------------|
| `lexer.l`           | **Primary deliverable** — Flex specification of the scanner   |
| `test.c`            | Sample input that exercises every token category              |
| `Makefile`          | One-command build / run / clean                               |
| `lexer_demo.py`     | Portable Python verification runner (same regexes, same output) |
| `output.txt`        | Captured token stream for `test.c`                            |
| `screenshots/`      | Demo screenshots referenced from the slides                   |
| `summary.md`        | Test-case summaries and observations                          |
| `slides.pptx`       | Project presentation                                          |

## How to build and run

### Option A — Flex + GCC (the actual deliverable)

```bash
flex   lexer.l                   # produces lex.yy.c
gcc    lex.yy.c -o lexer -lfl    # macOS: replace -lfl with -ll
./lexer test.c                   # or: ./lexer < test.c
```

Or simply:

```bash
make          # build
make run      # build + run on test.c
make clean    # remove generated files
```

### Option B — Portable Python runner (no toolchain needed)

```bash
python3 lexer_demo.py test.c
```

This script encodes the **same regular expressions** used in `lexer.l`, so the token stream is identical. We provide it so the scanner can be demonstrated on any machine without installing Flex / a C compiler.

## Token categories recognised

```
KEYWORD     if else while for do return break continue
            int float double char void const struct typedef
            sizeof switch case default
IDENT       [A-Za-z_][A-Za-z0-9_]*
INT_CONST   [0-9]+
FLT_CONST   [0-9]+.[0-9]+([eE][+-]?[0-9]+)?
STR_CONST   "..."  (with escapes)
CHR_CONST   '.'    (with escapes)
OPERATOR    + - * / % = < > ! & | ^ ~
            == != <= >= && || ++ -- += -= *= /= ->
PUNCT       ( ) { } [ ] ; , . : ? #
COMMENT     // ...   and   /* ... */
```

Whitespace and newlines are consumed silently; line / column counters are updated so error messages can point to the exact location.

## Result on `test.c`

```
Summary: total=155  keywords=22  identifiers=35  numbers=13  operators=20  errors=1
```

The single reported error corresponds to the deliberate stray `@` character we inserted at the end of `test.c` to demonstrate the scanner's error-reporting feature.

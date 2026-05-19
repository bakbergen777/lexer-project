# Test Program & Results — Summary

## 1. Tool choice

We selected **Flex** (the open-source successor to AT&T's `lex`) because it is the de-facto standard automatic lexical-analyzer generator, is supported on every major platform, and integrates cleanly with `bison` / `yacc` for the parser stage that follows in this course. Flex consumes a regex-based specification and emits a C source file containing a table-driven DFA scanner.

## 2. Specification design (`lexer.l`)

The specification is split into the three classic Flex sections:

1. **Definitions** — `%option`s and reusable regex macros (`DIGIT`, `LETTER`, `ID`, `INT`, `FLOAT`, `STRING`, `CHARCONST`, comments).
2. **Rules** — one rule per token category. Multi-character operators (`==`, `!=`, `<=`, `>=`, `&&`, `||`, `++`, `--`, `+=`, …) appear *before* the single-character operator rule so Flex's longest-match policy picks the right token.
3. **User code** — a `main()` that opens the input file, calls `yylex()`, and prints a final summary (totals per category and number of errors).

Each rule's action calls a small `emit()` helper that prints one row of `line:col  category  lexeme`, advances the column counter, and increments per-category counters.

## 3. Test program (`test.c`)

We wrote a self-contained C-like sample that touches every category at least once:

| Construct in `test.c`                       | Tokens exercised                     |
|---------------------------------------------|--------------------------------------|
| `#include <stdio.h>`                        | `#`, identifiers, `<`/`>`            |
| `// single-line comment`                    | line comment rule                    |
| `/* multi-line comment */`                  | block comment rule                   |
| `int factorial(int n)`                      | keywords, identifiers, punctuation   |
| `if (n <= 1) return 1;`                     | `if`, `<=`, `return`, integer        |
| `float pi = 3.14159;`                       | float literal                        |
| `char letter = 'A';`                        | character literal                    |
| `const char *msg = "Hello, Compiler!";`     | string literal, `*`, `=`             |
| `for (int i = 0; i < 5; i++)`               | `for`, `++`                          |
| `if (x >= 100 && pi != 0.0)`                | `>=`, `&&`, `!=`                     |
| `int bad@token = 0;`                        | **deliberate `@` error** to test error reporting |

## 4. Observed result

Running on `test.c`:

```
Summary: total=155  keywords=22  identifiers=35  numbers=13  operators=20  errors=1
```

Screenshots:

* `screenshots/01-lexer-output-part1.png` — first half of the token stream (header + first 70 tokens).
* `screenshots/02-lexer-output-part2.png` — second half of the token stream including the final `Summary` line and the `[error]` for the stray `@`.
* `screenshots/03-build-and-run.png` — terminal session showing `flex lexer.l` → `gcc` → `./lexer test.c`.

### What the screenshots confirm

1. **Every keyword** in our keyword list is correctly classified as `KEYWORD`, never as `IDENT`. Flex's longest-match rule combined with rule ordering guarantees this.
2. **Multi-character operators** (`<=`, `>=`, `==`, `!=`, `&&`, `++`) are recognised as one token, not two adjacent single-character operators.
3. **Floats vs integers** — `3.14159` and `2.0` are tagged `FLT_CONST`, while `42`, `5`, `0`, `100`, `7` are `INT_CONST`.
4. **String and character literals** are kept intact (with their quotes and escapes) and tagged `STR_CONST` / `CHR_CONST`.
5. **Comments** are matched as whole tokens; their internal characters never leak into the token stream.
6. **Line/column tracking** stays accurate across multi-line comments — the next token after a `/* ... */` reports the correct line.
7. **Error reporting** locates the stray `@` precisely (`line 38 col 8`) and the scanner recovers, continuing to tokenise the rest of the line.

## 5. Verification with the Python runner

To make the demo reproducible on any machine, `lexer_demo.py` re-implements the same regex master list (with the same precedence rules) and prints output in the same format. Running it on the same `test.c` produces an identical token stream and identical summary numbers, which we treat as a regression check on the Flex specification.

## 6. Build instructions (recap)

```bash
flex lexer.l
gcc  lex.yy.c -o lexer -lfl    # macOS: -ll
./lexer test.c
# or:
make run
# or, no toolchain required:
python3 lexer_demo.py test.c
```

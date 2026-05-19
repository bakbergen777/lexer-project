#!/usr/bin/env python3
"""
lexer_demo.py - portable verification runner

Mirrors the regex specification in lexer.l so the same input file
produces the same token stream whether the user runs Flex (lexer.l)
or this script. This is convenient when graders want to see the
output without installing Flex / a C toolchain.

Usage:
    python3 lexer_demo.py test.c
"""
import re
import sys
from pathlib import Path

# ----- Token spec (order matters - longer/more-specific first) ----
KEYWORDS = {
    "if", "else", "while", "for", "do", "return", "break", "continue",
    "int", "float", "double", "char", "void", "const", "struct",
    "typedef", "sizeof", "switch", "case", "default",
}

TOKEN_SPEC = [
    ("BCOMMENT", r"/\*[\s\S]*?\*/"),
    ("LCOMMENT", r"//[^\n]*"),
    ("FLOAT",    r"\d+\.\d+([eE][+-]?\d+)?"),
    ("INT",      r"\d+"),
    ("STRING",   r"\"([^\"\\\n]|\\.)*\""),
    ("CHAR",     r"'([^'\\\n]|\\.)'"),
    ("OP2",      r"==|!=|<=|>=|&&|\|\||\+\+|--|\+=|-=|\*=|/=|->"),
    ("OP1",      r"[+\-*/%=<>!&|^~]"),
    ("PUNCT",    r"[(){}\[\];,.:?#]"),
    ("ID",       r"[A-Za-z_][A-Za-z0-9_]*"),
    ("NL",       r"\r?\n"),
    ("WS",       r"[ \t]+"),
    ("MISMATCH", r"."),
]

LABEL = {
    "BCOMMENT": "COMMENT   ",
    "LCOMMENT": "COMMENT   ",
    "FLOAT":    "FLT_CONST ",
    "INT":      "INT_CONST ",
    "STRING":   "STR_CONST ",
    "CHAR":     "CHR_CONST ",
    "OP2":      "OPERATOR  ",
    "OP1":      "OPERATOR  ",
    "PUNCT":    "PUNCT     ",
    "ID":       "IDENT     ",
    "KEYWORD":  "KEYWORD   ",
}

MASTER = re.compile("|".join(f"(?P<{n}>{p})" for n, p in TOKEN_SPEC))


def lex(source: str):
    line, col = 1, 1
    counts = dict(total=0, kw=0, id=0, num=0, op=0, err=0)

    print("=" * 60)
    print(" Lexical analyzer (Python verification runner)")
    print(" Compiler Principles - Group Project")
    print("=" * 60)
    print("  line:col  category   lexeme")
    print("  --------  ---------  ----------------------")

    for m in MASTER.finditer(source):
        kind = m.lastgroup
        text = m.group()

        if kind == "NL":
            line += 1
            col = 1
            continue
        if kind == "WS":
            col += len(text)
            continue
        if kind == "MISMATCH":
            print(f"  [error] line {line} col {col}: "
                  f"unexpected character {text!r}", file=sys.stderr)
            counts["err"] += 1
            col += 1
            continue

        # multi-line comments may contain newlines - track them
        nl_count = text.count("\n")
        display = text if "\n" not in text else text.splitlines()[0] + " ..."

        if kind == "ID" and text in KEYWORDS:
            label = LABEL["KEYWORD"]
            counts["kw"] += 1
        else:
            label = LABEL[kind]
            if kind == "ID":      counts["id"]  += 1
            if kind in ("INT", "FLOAT"): counts["num"] += 1
            if kind in ("OP1", "OP2"):   counts["op"]  += 1

        print(f"  {line:4d}:{col:<3d}  {label}  {display}")
        counts["total"] += 1

        if nl_count:
            line += nl_count
            col = len(text) - text.rfind("\n")
        else:
            col += len(text)

    print("-" * 60)
    print(f"  Summary: total={counts['total']}  keywords={counts['kw']}  "
          f"identifiers={counts['id']}  numbers={counts['num']}  "
          f"operators={counts['op']}  errors={counts['err']}")
    print("=" * 60)
    return counts


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("test.c")
    if not path.exists():
        sys.exit(f"input file not found: {path}")
    src = path.read_text(encoding="utf-8", errors="replace")
    rc  = lex(src)
    sys.exit(0 if rc["err"] == 0 else 2)


if __name__ == "__main__":
    main()

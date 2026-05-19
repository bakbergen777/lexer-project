# Build / run / clean the Flex-based lexer
#
#   make          -> build ./lexer
#   make run      -> build and run on test.c
#   make py       -> run the portable Python verification runner
#   make clean    -> remove generated files
#
# Requires: flex, gcc (or clang).  On macOS link against -ll instead of -lfl.

CC      := gcc
CFLAGS  := -O2 -Wall
LIBS    := -lfl                # macOS: change to -ll

lexer: lex.yy.c
	$(CC) $(CFLAGS) lex.yy.c -o lexer $(LIBS)

lex.yy.c: lexer.l
	flex lexer.l

run: lexer
	./lexer test.c

py:
	python3 lexer_demo.py test.c

clean:
	rm -f lex.yy.c lexer lexer.exe output.txt

.PHONY: run py clean

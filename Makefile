all: test

test: test.c
	clang $< -o $@

clean:
	rm -f test

.PHONY: clean

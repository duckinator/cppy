all: test

test: test.o
	clang $< -o $@

%.o: %.c
	./preprocessor.py $< | clang -std=c11 -x c -c -o $@ -

clean:
	rm test
	rm -f *.o
	rm -f *.cppy

.PHONY: clean

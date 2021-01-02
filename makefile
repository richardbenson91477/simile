all: test1.s

test1.s: test1.simile
	./simile < $^ > $@

test:

clean:
	rm -f test1.s

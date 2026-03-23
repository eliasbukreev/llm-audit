workflows:
	rm -rf /home/elias/.kilocode/workflows/
	mkdir -p /home/elias/.kilocode/workflows/
	cp -r workflows/* /home/elias/.kilocode/workflows/

docs:
	rm -rf /home/elias/docs/
	mkdir -p /home/elias/docs/
	cp -r docs/* /home/elias/docs/

.PHONY: workflows docs

workflows:
	rm -rf /home/elias/.kilocode/workflows/
	mkdir -p /home/elias/.kilocode/workflows/
	cp -r workflows/* /home/elias/.kilocode/workflows/

.PHONY: workflows

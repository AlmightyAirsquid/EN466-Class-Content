PYTHON := python3

.PHONY: carbon golf

carbon:
	$(PYTHON) carbon.py --plot=$(WIDTH)

golf:
	$(PYTHON) golf.py --theta=$(THETA)

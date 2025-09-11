PYTHON := python3
SCRIPT := trigonometry.py

.PHONY: plot write read

plot:
	$(PYTHON) $(SCRIPT) --function $(FXN) --print $(FMT)

write:
	$(PYTHON) $(SCRIPT) --write $(TXT) --function $(FXN)

read:
	$(PYTHON) $(SCRIPT) --print $(FMT) --read_from_file $(TXT)

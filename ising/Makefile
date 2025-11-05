PYTHON := python3
SCRIPT := ising.py

ITER := 2500
TEMP := 1.0
FPS := 1000
DIM := 50

ising:
	$(PYTHON) $(SCRIPT) -I $(ITER) -T $(TEMP) -F $(FPS) -D $(DIM)

clean:
	rm -f *.png

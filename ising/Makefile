PYTHON := python3
SCRIPT := ising.py

ITER := 2500
TEMP := 1.0
FPS := 1000
DIM := 50
SEED := 67

ising:
	$(PYTHON) $(SCRIPT) -I $(ITER) -T $(TEMP) -F $(FPS) -D $(DIM) --seed $(SEED)

clean:
	rm -f *.png

PYTHON := python3
RUN := 1

.PHONY: diffusion gases oscillator poisson rnumbers rwalk

diffusion:
	$(PYTHON) diffusion.py --RUN=$(RUN)
gases:
	$(PYTHON) gases.py --RUN=$(RUN)
oscillator:
	$(PYTHON) oscillator.py --RUN=$(RUN)
poisson:
	$(PYTHON) poisson.py --RUN=$(RUN)
rnumbers:
	$(PYTHON) rnumbers.py --RUN=$(RUN)
rwalk:
	$(PYTHON) rwalk.py --RUN=$(RUN)

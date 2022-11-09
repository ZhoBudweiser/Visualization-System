import richdem as rd
import numpy as np

# Create some NumPy data
npa = np.random.random(size=(100, 100))

# Wrap the NumPy data in an rdarray. I want to treat all of the cells as data
# cells, so I use `no_data=-9999` since I know none of my cells will have
# this value.
rda = rd.rdarray(npa, no_data=-9999)

# Fill depressions, modifying in place. At this point, the calculation I
# wanted to do is done and I can throw away the `rda` object.
rd.FillDepressions(rda, in_place=True)

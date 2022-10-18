import numpy as np
from scipy.stats import norm

from Option import Option

opt=Option("C",100,"20221215",1)

print(opt.calcPrice(110,0.5,0.3,0))
print(opt.calcPayoff(139))
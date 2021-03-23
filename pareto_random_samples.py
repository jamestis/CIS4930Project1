from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
def pareto_random_samples(shape,num_samples):
    #shape * scale / (shape -1) = 1MB
    scale_i = (shape - 1) / shape
    samples = np.linspace(start = scale_i, stop = 10, num=num_samples)
    pdf = np.array([stats.pareto.pdf(x=samples, b=shape,loc=0,scale=scale_i)])
    normalized_pdf = pdf[0]/np.sum(pdf[0])
    return np.random.choice(a = samples, size =num_samples,replace = True,p=normalized_pdf)

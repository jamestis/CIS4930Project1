from scipy import stats
import numpy as np
def generate_files(shape,num_samples):
    #shape * scale / (shape -1) = 1MB
    scale_i = (shape - 1) / shape
    #possibly FIXME : where to stop?
    samples = np.linspace(start = scale_i, stop = 6, num=num_samples)
    print("Smallest possible file = ", scale_i)
    pdf = np.array([stats.pareto.pdf(x=samples, b=shape,loc=0,scale=scale_i)])
    normalized_pdf = pdf[0]/np.sum(pdf[0])
    return np.random.choice(a = samples, size =num_samples,replace = True,p=normalized_pdf)


import numpy as np
import os
import joblib
import subprocess
from partition import step_function, equispaced
from matrix_io import *

from bzmodel import *
from noise_gpu_settings import *

prec = 256
D = BZModel(prec)
RI = D.field

#graphplot = plot(lambda x: D.orig_f(RI(x)).center(),
#     D._start.center(),
#     (D._start + D._scale).center(), color="#000")
#
#graphplot.show()

data = [[RR(x.strip()) for x in qln.split("\t")] for qln in open('lyap_results.txt', 'r')]
data = []
myplot = plot([])

for noise,_,lower,upper in data:
    print noise,' -> [',lower,',',upper,']'

    myplot += line([(noise*0.97, upper+0.012), (noise, upper),
                    (noise/0.97, upper+0.012)],
                   color="#f80")
    myplot += line([(noise*0.97, lower-0.012), (noise, lower),
                    (noise/0.97, lower-0.012)],
                   color="#0f8")
#myplot.show(scale = "semilogx", xmin = 0.00005, xmax = 0.12, ymin = -1.2, ymax = 0.5)
#myplot = line([(x[0],x[2]) for x in data], color="#f00")
#myplot += line([(x[0],x[3]) for x in data], color="#000")
#myplot.show(scale = "semilogx")

params = [
    (D, 2**25, 2**16, 60, 690, 2**14), #0.01052
     (D, 2**25, 2**16, 60, 630, 2**14),
     (D, 2**25, 2**16, 60, 578, 2**14),
    (D, 2**25, 2**16, 60, 530, 2**14), #0.008087
     (D, 2**25, 2**16, 60, 486, 2**14),
     (D, 2**25, 2**16, 60, 446, 2**14),
    (D, 2**25, 2**16, 60, 408, 2**14), #0.006225
     (D, 2**25, 2**16, 60, 374, 2**14),
     (D, 2**25, 2**16, 60, 342, 2**14),
    (D, 2**25, 2**16, 60, 314, 2**14), #0.004791
     (D, 2**25, 2**16, 60, 288, 2**14),
     (D, 2**25, 2**16, 60, 264, 2**14),
    (D, 2**25, 2**16, 60, 242, 2**14), #0.003692
     (D, 2**25, 2**16, 60, 222, 2**14),
     (D, 2**25, 2**16, 60, 202, 2**14),
    (D, 2**25, 2**16, 60, 186, 2**14), #0.002838
     (D, 2**25, 2**16, 60, 170, 2**14),
     (D, 2**25, 2**16, 60, 154, 2**14),
    (D, 2**25, 2**16, 60, 142, 2**14), #0.002166
     (D, 2**25, 2**16, 60, 130, 2**14),
     (D, 2**25, 2**16, 60, 120, 2**14),
    (D, 2**25, 2**16, 60, 110, 2**14), #0.001678
     (D, 2**25, 2**17, 60, 200, 2**14),
     (D, 2**25, 2**17, 60, 184, 2**14),
    (D, 2**25, 2**17, 60, 168, 2**14), #0.001281
     (D, 2**25, 2**17, 60, 154, 2**14),
     (D, 2**25, 2**17, 60, 142, 2**14),
    (D, 2**25, 2**17, 60, 130, 2**14), #0.0009918
     (D, 2**26, 2**17, 60, 120, 2**14),
     (D, 2**26, 2**17, 60, 110, 2**14),
    (D, 2**26, 2**17, 60, 100, 2**14), #0.0007629
     (D, 2**26, 2**18, 60, 184, 2**15),
     (D, 2**26, 2**18, 60, 168, 2**15),
    (D, 2**26, 2**18, 60, 154, 2**15), #0.0005874
     (D, 2**26, 2**18, 60, 140, 2**15),
     (D, 2**26, 2**18, 60, 128, 2**15),
    (D, 2**26, 2**18, 60, 118, 2**15), #0.0004501
     (D, 2**26, 2**19, 65, 220,  2**16),
     (D, 2**26, 2**19, 65, 200,  2**16),
    (D, 2**26, 2**19, 65, 184,  2**16),  #0.0003509
     (D, 2**26, 2**19, 65, 166,  2**16),
     (D, 2**26, 2**19, 65, 152,  2**16),
    (D, 2**26, 2**19, 65, 140,  2**16),  #0.0002670
     (D, 2**26, 2**19, 65, 128,  2**16),
     (D, 2**26, 2**19, 65, 118,  2**16),
    (D, 2**26, 2**19, 65, 108,  2**16),  #0.0002060
     (D, 2**26, 2**20, 70, 198,  2**17),
     (D, 2**26, 2**20, 70, 182,  2**17),
    (D, 2**26, 2**20, 70, 166,  2**17),  #0.0001583
    #(D, 2**26, 2**20, 70, 136,  2**17),  #0.0001296
    #(D, 2**26, 2**20, 70, 112,  2**17),  #0.0001068
]
params = [
    (D, 2**25, 2**16, 60, 690, 2**14, 'orange'), #0.01052
    (D, 2**25, 2**16, 60, 242, 2**14, 'red'), #0.003692
    (D, 2**25, 2**17, 60, 168, 2**14, 'fuchsia'), #0.001281
    (D, 2**26, 2**18, 60, 118, 2**15, 'lightblue'), #0.0004501
    (D, 2**26, 2**20, 70, 166,  2**17, 'darkblue'),  #0.0001583
]

red_size = 2000
plot_data = []

for D, K, Kcoarse, num_iter, coarse_noise_abs, Kest, col in params:
    #fingerprint = 'P%d_K%d_C%d_N%d_I%d_E%d' % (D.field.prec(), K, Kcoarse,
    #                                       coarse_noise_abs, num_iter, Kest)
    meas_fingerprint = 'P%d_K%d_N%d' % (D.field.prec(), K,
                                   coarse_noise_abs*K/Kcoarse)
    measure_file = 'bzmodel_results/measure_' + meas_fingerprint
    measure_sample_file = 'bzmodel_results/measure_' + \
                          meas_fingerprint + ('_red%d'%red_size)

    if os.access(measure_file, os.R_OK):
        if not os.access(measure_sample_file, os.R_OK):
            args = ['./ComputeReduction',
                    str(K),
                    os.path.abspath(measure_file),
                    str(red_size),
                    os.path.abspath(measure_sample_file)
            ]
            print ' '.join(args)
            subprocess.call(args, cwd = COMPINVMEAS_OPENCL_PATH)
            if not os.access(measure_sample_file, os.R_OK):
                raise ValueError, 'Creation of file %s failed!'%measure_sample_file

        noise = RR(coarse_noise_abs)/Kcoarse*RR(D._scale.center())
        plot_data.append( (noise, measure_sample_file, col) )

#plot_data.sort()


plots = []
for i in range(len(plot_data)):
    noise, sample, col = plot_data[i]
    vec = mmap_binary_vector(red_size, sample)
    func = step_function(vec/red_size, equispaced(red_size))
    plots.append(plot_step_function(func, legend_label = str(noise),
                              #scale='semilogy', ymax=1000, ymin = 0.01)
                                    ymax=50, ymin = 0, color = col))

plot = sum(plots)
plot.save_image('images/measure_plot.png')

#myplot.show(scale = "semilogx", xmin = 0.00005, xmax = 0.12, ymin = -1.2, ymax = 0.5)

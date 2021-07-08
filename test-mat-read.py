import scipy.io
mat = scipy.io.loadmat('fud_points.mat')

# Like this?
print(mat['Fud_points']['Pon'][0][0][0])
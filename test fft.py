# test fft czemu to nie działa
import numpy as np
import matplotlib.pyplot as plt

N = 1000
A = 5
fx = 10
fp = 1000

# okres próbkowania
dt = 1/fp

xx = 0
t = []
for i in range(N):
    t.append(xx*dt)
    xx = xx+1

#print(t)

y = A * np.sin(2*3*fx*t)
print(len(y))

# y fft
X = np.fft.fft(y)

print(type(N))
print(type(dt))


df = 1/(N*dt)

print('df to ', df)

xxx = 0
y_fft = []
for i in range(N):
    y_fft.append(xxx*df)
    xxx = xxx+1

plt.plot(y)
plt.show()
#plt.plot(X)




"""
z = np.corrcoef(y)
#print(len(z))
print(z)
"""



plt.show()






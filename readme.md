## About program
* [Reasons](#reasons)
* [Algorithms of F0](#algorithms-of-F0)
* [Conclusions](#conclusions)
* [Setup and run](#setup-and-run)

## Reasons

In processing digital audio, vocal voice or instruments, 
information about the fundamental frequency - F0 - is extremely important. 

However, a wrongly determined f0 often results in errors in further processes of the program.

A review of algorithms is used to test which one gives the best f0 results. 

## Algorithms of F0
The methods are divided into those working in the time and frequency domain.
```
* Zero crossing analysis
* Autocorrelation function analysis
* YIN (based on autocorrelation)
* Algorithm based on spectral analysis
* PSD
```

## Conclusions
The best method is the autocorrelation function and the method based on spectral analysis. 

However, they require further updating, e.g. for octave errors or noisy recordings.

In the folder you will find examples of recordings which you can rehearse yourself.

## Setup and run
You should have an updated python and libros library version.
Then you run "main_gui".

After you run "main_gui", 
an interface appears where we choose the detection method and the file of our sound (.wav). 

Depending on the method we get information about the F0 value and sometimes a graph (if necessary).

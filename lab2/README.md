# Lab 2: Graph algorithms
This lab consists of Graph class and 3 main scripts:
* generate.py N [-d D] -- generates graph with N nodes and density of D (0 &le; d &le; 1), outputs pickle dump to stdout

* cycle.py [e / h] FILE -- finds Eulerian / Hamiltonian cycle

* show.py FILE -- visualises graph with NetworkX + MatPlotLib

It is also possible to import Graph class (from graphs.py) into any other script or in Python console: the class has
basic methods for creating, examining and editing graphs.
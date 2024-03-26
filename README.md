# sugiyama_layout
Sugiyama layout is used for better hierarchical Graph Visualization.
A graph(V,E) has V = vertices and E(n,m) = Edges
Edges have 2 vertices.
n - parent node, m - child node.

The Visualization consists of 5 steps:

Step 1:
Cycle Breaking. Using networkx library, detect where cycles exist and switches the direction of the last edge

Step 2:
Leveling. Every Node(Vertex) is given a level, where it should take part in the hierarchy, based on the input, which is a list of every edge in the graph.
The width of a single row can be modified and can be given a certain maximum, so the graph will be longer, with more levels but more narrow, preventing visual clutter.

Step 3:
Crossing Minimization. Calculating the relative positions of every node, so the number of crossings, that form from the edges is maximally lowered. There are more than one way to calculate this.
In this repository, I'm using barycenter of the parents in the main 'sugiyama_layout' file.
In 'sugiyama with 2 layers.py' I'm using interconnection matrix of G(graph), calculating the number of crossings in every iteration, while rotating the positions of the nodes in the list for the current level.
(the matrix does not include dummies)

Step 4:
Vertex Positioning. Positions are assigned based on the nodes' ordering in the list of every level.

Step 5:
Drawing Edges. Using the positions of every node from the previous step and matplotlib.pyplot the graph is visualized. 


'barycenter with 2 layers' may be remade to be used for more than 2 layers, therefore could be installed in the main 'sugiyama_layout' file.

USER GUIDE
**********

To launch the WERW-Kpath algorithm type:

java -jar werw-kpath.jar input-filename output-filename k-path-length delimiter(default: tab-separated-value)

input-filename: the name of the file containing the edgelist representing the network

output-filename: the output filename

k-path-length: the length of the k-path random walk (reasonable values range in the interval [5, 20])

delimiter: this parameter is optional, default "\t" (tab-separated values); example of other options: "," (csv) or " " (space-separated values)

Example line commands:

java -jar werw-kpath.jar facebook-links.txt weighted-facebook-links.txt 10


This call will invoke WERW-Kpath passing the input network file called facebook-links.txt, prepared as an edgelist of tab-separated values, exploiting k-path random walks up to length 10.


java -Xmx4G -jar werw-kpath.jar facebook-links.txt weighted-facebook-links.txt 10


This call will invoke WERW-Kpath asking the Java Virtual Machine to allocate 4G of memory to this process. 
This parameter is possibly required when managing large networks (millions of edges).


java -Xmx4G -jar werw-kpath.jar facebook-links.txt weighted-facebook-links.txt " " 10


This invokation is required for passing a "space-separated" edgelist.

REFERENCE
*********

If you use this algorithm please cite the following work:

P. De Meo, E. Ferrara, G. Fiumara, A. Ricciardello. A novel measure of edge centrality in social networks. Knowledge-based Systems (to appear)

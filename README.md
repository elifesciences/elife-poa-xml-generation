# Background

This is a small script to create an XML file that conforms to the output we expect for delivery to HighWire for the publish on accept project. 

A sample output file is provided in `sample-expected-result.xml`.

We are creating a set of lightweight python scripts to do this job. 


## Project outline / inital TODO list

- write a script to output XML from a dict
- tidy up the dict using named tuples
- convert the named tuples to a class
- update the XML outputter to accept a class object as input
- write a test to validate against the DTD that we need to provide to highwire 
- provide utility functions to allow us to modify the structure of the python object, so that we can quicly modify the output XML
- create something using these utility functions that consumes the CSV file that nathan is working on

# Version history 

2013-11-26 first proof of concept. 

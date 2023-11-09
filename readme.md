# Subjective logic used in VANet

## Introduction

In this project, we've applied the subjective logic as a trust model in a VANet. We've used Mininet-wifi to simulate the subjective logic method we've created.

## Context

This project is created as part of a bachelor’s degree thesis at the University of Geneva in information system!

## Contents Table

* [How to get started?](#get-started)
* [Subjective logic](#subjective-logic)
  * [What is subjective logic?](#what-is-it)
  * [How does it work?](#how-it-works)
  * [How to use the librairy](#subjective-logic-library-classes-and-functions)
    * [Graph](#graph)
    * [SubLog](#sublog)
    * [Functions](#functions)
  * [How to do simulations](#simulations)

## Get started

* [ ] **Download** Mininet-wifi : https://github.com/intrig-unicamp/mininet-wifi
* [ ] Go into Mininet-wifi directory ```cd Mininet-wifi```
* [ ] Clone this repository ``` git clone https://gitlab.unige.ch/Ismet.Turhan/research_project```
* [ ] Go into the folder ```cd research_project```
* [ ] Launch the topology ``` sudo python3 mytopo.py ```
* [ ] Start your simulations !

## Subjective logic
### What is it
The subjective logic is a trust model based on the Bayesian probabilities to ensure data accuracy through a network. It is based on a
human interactions comparison and uses opinions as the main trust relation values. An opinion is based on four values the belief, disbelief, 
uncertainty and base rate. It is also possible to consider an opinion based on 3 
values the count of good interaction, bad interaction and the base rate. 
From opinions, it is possible to derive a trust value which will be between 0 and 1, 0 being total distrust and 1 total trust.

### How it works

![Diagram](doc/diagram.png)

To add new opinion simply use the library as following :
 
#### add opinion with 3 values 
    trust = sub_logic.SubLog(False, {'a':0.5, 'r':0, 's':1})
#### add opinion with 4 values
    trust = sub_logic.SubLog(True, {'a':0.5, 'b':0.1, 'd':0.5, 'u': 0.4})

### Subjective logic library Classes and Functions
#### Graph
The Graph class represents a node's opinion storage. It provides methods for adding direct and indirect opinions, retrieving opinions, computing trust, and printing opinions.

##### Constructor:

**Graph(my_node_id)**: Initializes a graph with the specified node ID.
##### Methods:

**add_direct_nodes(node_id, opinion)**: Adds direct opinions to the graph for the specified node ID.<br>
**add_indirect_nodes(opinion_of, opinion_on, opinion)**: Adds indirect opinions to the graph.<br>
**get_my_opinion(node_id)**: Retrieves the opinion of the current node about a specified node.<br>
**get_opinion_of(node_id, on_node)**: Retrieves the opinion about a node from another node.<br>
**compute_trust(node_id)**: Computes trustworthiness towards a specified node.<br>
**print_graph()**: Prints the stored opinions in the graph.<br>
**get_my_nodes()**: Retrieves a list of nodes for which the current node has opinions.<br>

#### SubLog
The SubLog class represents an opinion and provides methods for calculating trust, transitivity, and printing opinions.

##### Constructor:

**SubLog(is_opinion, data)**: Initializes an opinion. If is_opinion is True, provide data for a, b, d, and u. If is_opinion is False, provide data for r, s, and a.<br>
##### Methods:

**trust()**: Calculates and returns the trust value based on the opinion.<br>
**transitivity(opinion1)**: Computes the transitivity of two opinions.<br>
**opinion_print_sr()**: Returns a dictionary with opinion values in terms of good and bad interactions.<br>
**opinion_print_bdu()**: Returns a dictionary with opinion values in terms of belief, disbelief, and uncertainty.<br>

#### Functions
**cumulative_fusion(opinion_1, opinion_2)** The cumulative_fusion function combines two opinions using the cumulative fusion method.<br>

### Simulations

To simulate the subjective logic, we provided 2 scripts with the same topology with 4 static nodes. 
One topology is constituted with 4 good nodes <br>
``` sudo python3 sim4n4g.py ``` <br>
The second topology contains 3 good nodes and 1 bad node <br>
``` sudo python3 sim4n3g.py ``` <br>

By using the ``` -s ``` flag you can save the simulations result

Feel free to modify or create new topology by referring to the Mininet documentation : https://github.com/intrig-unicamp/mininet-wifi


#Author : Ismet Turhan
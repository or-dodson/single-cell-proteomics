import networkx as nx
import pandas as pd
import numpy as np
from itertools import product

class BayesianNetwork(nx.DiGraph):
    def __init__(self, *args, **kwargs):
        super(BayesianNetwork, self).__init__(*args, **kwargs)
    
    def fit(self, data: pd.DataFrame) -> None:
        """
        This method will take a dataframe and create the probability tables for each node in the network.
        Each column of the dataframe should have the same name as one of the nodes of the network."""
        
        # Find all unique values in each column of the data
        for col in data.columns:
            uniques = data[col].unique()
            if col not in self.nodes:
                continue

            self.nodes[col]["possible_values"] = uniques
        
        # Loop through each node and build the conditional probability table
        for node in self.nodes:
            parents = self.predecessors(node)
            possible_values_of_parents = [parent["possible_values"] for parent in parents]
            possible_values_of_node = node["possible_values"]

            for conditioned_on in product(*possible_values_of_parents):
                conditioned_on = np.array(conditioned_on)
                filter = data[parents] == conditioned_on[None,:]
                subset = data.loc[filter, :]
                for possibility in possible_values_of_node:
                    

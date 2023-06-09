# -*- coding: utf-8 -*-
from pysummarization.similarity_filter import SimilarityFilter


class Dice(SimilarityFilter):
    '''
    Concrete class for filtering mutually similar sentences.
    '''

    def calculate(self, token_list_x, token_list_y):
        '''
        Calculate similarity with the Dice coefficient.
        
        Concrete method.
        
        Args:
            token_list_x:    [token, token, token, ...]
            token_list_y:    [token, token, token, ...]
        
        Returns:
            Similarity.
        '''

        x, y = self.unique(token_list_x, token_list_y)
        try:
            result = 2 * len(x & y) / float(sum(map(len, (x, y))))
        except ZeroDivisionError:
            result = 0.0
        return result

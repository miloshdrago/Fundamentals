#!/usr/bin/env python3

# dependencies
from time import time

class Timer(object):
    """
    Decorator for timing a function execution.

    @example        ```
                    @Timer
                    def myfunction():
                        return somecalculation()

                    # this prints function name (i.e. 'myfunction' 
                    # and time to execute to stdout
                    myfunction()
                    ```

    @dependencies   time
    @author         Tycho Atsma <tycho.atsma@student.uva.nl>
    @file           Timer.py
    @documentation  public
    @copyright      University of Amsterdam
    """

    def __init__(self, fn):
        """
        Constructor.
        @param  function    Function to decorate.
        """
        self._fn = fn

    def __call__(self, *args, **kwargs):
        """
        Method to call the decorator and function.
        @param  variadic    Arguments for the function.
        @param  variadic    Arguments for the function.
        @return mixed
        """
        # we need to start a timer so we can calculate
        # the difference after the function execution
        start_time = time()
        
        # call the function and save the output
        out = self._fn(*args, **kwargs)

        # print function name and time to stdout
        print("Execution of '{}' took {}.".format(self._fn.__name__, time() - start_time))

        # expose the output of the decorated function
        return out

# run as main for testing
if __name__ == "__main__":

    @Timer
    def myfunction():
        count = 0
        for n in range(1000):
            count += n
        return count

    # output
    myfunction()

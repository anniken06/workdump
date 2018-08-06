#! python

# The first line is a shebang, it tells the system how to run the script


class DocDemo:
    """String literals that immediately following a scope declaration becomes a docstring.
    This demo will show you how docstrings should look like.

    Usage:
        python my_documentation.py
    """

    def mulMaster(x, y):
        """Multiply two numbers.

        Args:
            x: The first factor.
            y: The second factor.

        Returns:
            The product of x and y
        """
        return x * y


help(DocDemo)
print(DocDemo.mulMaster(3, 4))

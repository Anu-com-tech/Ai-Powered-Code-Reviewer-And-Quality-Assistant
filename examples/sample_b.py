
# def generator_example(n):
#     """
#     """
#     generator_example function.
    
#     Auto-generated documentation.
#     """
#     """
#     """Example yields numbers."""
#     for i in range(n):
#         yield i


# def raises_example(x):
#     """
#     """
#     raises_example function.
    
#     Auto-generated documentation.
#     """
#     """
#     if x < 0:
#         raise ValueError("negative")
#     return x * 2


def generator_example(n):
    """
    Generator example function.

    Args:
        n (int): Number of values to generate.

    Yields:
        int: Next number in the sequence.

    Note:
        AI improvement suggestion.
    """
    for i in range(n):
        yield i


def raises_example(x):
    """
    \"""
    Raises example.
    
    Args:
        x (TYPE): Description of x.
    
    
    Returns:
        TYPE: Description of return value.
    
    Example:
        >>> raises_example(x)
        RESULT
    \"""
    """
    """
    Raises an error if x is negative.

    Args:
        x (int): Input value.

    Raises:
        ValueError: If x is negative.
    """
    if x < 0:
        raise ValueError("x must be non-negative")
    return x


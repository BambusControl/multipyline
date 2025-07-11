import textwrap


def multipyline(s: str) -> str:
    """
    Format a multiline string by removing common leading whitespace and trailing/leading newlines.

    Args:
        s: The input string to format. Can contain multiple lines with varying indentation.

    Returns:
        A cleaned string with common leading whitespace removed and stripped of leading/trailing whitespace.
        Returns empty string for whitespace-only inputs.

    Examples:
        Basic usage - multiline strings using `multipyline`:
        >>> text = '''
        ...     First line:
        ...         Indented second line
        ...     Third line
        ... '''
        >>> result = multipyline(text)
        >>> print(result)
        First line:
            Indented second line
        Third line

        Working with multiline f-strings using `multipyline_inner`:
        >>> result = multipyline(f'''
        ...     Text below is indented:
        ...         {multipyline_inner(text, " " * 12)}
        ... ''')
        >>> print(result)
        Text below is indented:
            First line:
                Indented second line
            Third line

        Handling empty or whitespace-only strings:
        >>> multipyline("   ") == ""
        True
        >>> multipyline("\\n\\n\\n") == ""
        True
    """
    s = textwrap.dedent(s)
    return s.strip()


def multipyline_inner(s: str, prefix: str) -> str:
    """
    Use inside a `multipyline` f-string to format the inner multiline content.

    Here the inner content template is offset 8 spaces from the left
    >>> text = multipyline(f'''
    ...     Text below is indented:
    ...         {multipyline_inner(inner_text, '        ')}''')
    ... #       ^ until here is the prefix;     ^^^^^^^^ equals 8 spaces

    See more examples below.

    Args:
        s: The input string to format.
        prefix: The entire prefix to this template

    Returns:
        A formatted string with the specified prefix applied to each line.

    Examples:
        Intended usage:
        >>> first_text = '''
        ...     First line:
        ...         Indented second line
        ...     Third line
        ... '''
        >>> second_text = 'Oneline text'
        >>> result = multipyline(f'''
        ...     Text below is indented:
        ...         {multipyline_inner(first_text, " " * 8)}
        ...
        ...     This text doesn't need to use inner because there isn't whitespace before it: {second_text}
        ... ''')
        >>> print(result)
        Text below is indented:
            First line:
                Indented second line
            Third line
        This text doesn't need to use inner because there isn't whitespace before it: Oneline text

        Handling empty or whitespace-only strings:
        >>> multipyline("   ") == ""
        True
        >>> multipyline("\\n\\n\\n") == ""
        True
    """
    s = multipyline(s)
    s = textwrap.indent(s, prefix, lambda _: True)
    return s.strip()


def multipylinef(s: str, *args: str) -> str:
    """
    Format a multiline string with placeholders which are also multiline strings.
    Handles proper indentation for each placeholder.

    Args:
        s: The input string containing placeholders `{}`.
        *args: The arguments to fill in the placeholders.

    Returns:
        A formatted string with the placeholders replaced by the provided arguments.
    Raises:
        ValueError: If any single line contains multiple `{}` placeholders.
    Examples:
        Basic usage with a single placeholder:
        >>> func_impl = '''
        ...     # Inner part
        ...     if (x > 0):
        ...         print('Another line')
        ... '''
        >>> result = multipylinef(
        ...     '''
        ...     def fun(x: int):
        ...         print('Outer part')
        ...         {}
        ...     ''',
        ...     func_impl,
        ... )
        >>> print(result)
        def fun(x: int):
            print('Outer part')
            # Inner part
            if (x > 0):
                print('Another line')
    """

    TEMPLATE = "{}"

    formatted_args = [""] * len(args)
    arg_counter = 0

    for line in s.splitlines():
        if TEMPLATE not in line:
            continue

        if line.count(TEMPLATE) > 1:
            raise ValueError(
                f"Multiple '{TEMPLATE}' placeholders found in a single line of the string."
            )

        argument = args[arg_counter]
        formatted_argument = argument

        if len(argument.splitlines()) > 1 and textwrap.dedent(line).startswith(
            TEMPLATE
        ):
            prefix = line[: line.find(TEMPLATE)]
            formatted_argument = multipyline_inner(argument, prefix)

        formatted_args[arg_counter] = formatted_argument
        arg_counter += 1

    print(formatted_args)

    formatted = s.format(*formatted_args)
    return multipyline(formatted)

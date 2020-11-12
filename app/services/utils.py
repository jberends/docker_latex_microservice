import re


def calculate_table_width(
    property_models, first_column_width, column_width=4, extra_width_margin=0
):
    """
    Calculate the table width based on the amount of properties, and thus columns, the table will have

    :param extra_width_margin: [cm] Extra margin to take into consideration
    :param column_width: [cm] Specified column width
    :param first_column_width: [cm] Specified first column width
    :param property_models: part model
    :return:
    """
    return (
        extra_width_margin + (len(property_models)) * column_width + first_column_width
    )


def filter_escape_tex(value):
    """
    Create a filter to be used in jinja2 environments which excapes text based on regexes

    :param value: The text which needs to be escaped
    :return: The filter
    """
    LATEX_SUBS = (
        (re.compile(r"\\"), r"\\textbackslash"),
        (re.compile(r"([{}_#%&$])"), r"\\\1"),
        (re.compile(r"~"), r"\~{}"),
        (re.compile(r"\^"), r"\^{}"),
        (re.compile(r'"'), r"''"),
        #   (re.compile(r'\.\.\.+'), r'\\ldots'),
    )

    new_value = value
    for pattern, replacement in LATEX_SUBS:
        new_value = pattern.sub(replacement, new_value)
    return new_value


def filter_ellipsis_on_longtext(value, max_chars=60, footnote=False):
    """
    A jinja 2 filter that injects a ellipses (...) at the end of very long text.
    :param value: The text which needs to be escaped
    :param max_chars: add ellipsis behind numer of chars.
    :param footnote: add a footnote with the full text
    :return: The filter
    """
    new_value = value
    if len(str(value)) > max_chars:
        new_value = "{}...".format(str(value)[:max_chars])
        if footnote:
            new_value = new_value + r"\footnote{%s}" % value
    return new_value


def filter_no_newline(value):
    """
    A jinja 2 filter that ensures that the newline character is removed (for nicely flowing text)
    :param value: string value
    :return: string value without newline character
    """
    NEWLINE_REGEX = r"\\|\n"

    escape_regex = re.compile(NEWLINE_REGEX)
    r = escape_regex.sub(r" ", value)
    r = filter_squash_whitespace(r)
    return r


def filter_squash_whitespace(value):
    WHITESPACE_REGEX = r"\s+"
    regex = re.compile(WHITESPACE_REGEX)
    r = regex.sub(r" ", value)
    return r


def pixels_to_mm(pixels: int, dpi=200):
    """
    A filter that returns the mm from the number of pixels based on dpi for use in latex

    :param pixels: integer number of pixels
    :param dpi: integer dotsperinch
    :return: string with <nn>mm (size in milimeters)
    """
    return "{}mm".format(pixels / (dpi / 25.4))


def check_string_length(value):
    """

    :param value: string to be written in the cell
    :return: whether or not /seqsplit can be used
    """
    words = value.split(" ")
    if len(words) == 0:
        return False
    if len(words) == 1:
        return True
    return False

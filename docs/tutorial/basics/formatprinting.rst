.. _basics-printing:

Formatted print
###############

Using quotations "" with puts() will allow for standard string formatting to 
occur. By default, a new line character ``/n`` is added at the end of every
string

======== ============================
Sequence Meaning
======== ============================
``\"``   Literal double quote (``"``)
``\\``   Literal backslash (``\``)
``\0``   Binary zero
``\a``   BEL character
``\b``   Backspace
``\f``   Formfeed
``\n``   Newlines
``\r``   Carriage return
``\t``   Horizontal Tab
``\v``   Vertical Tab
======== ============================

String interpolation is also supported through the use of a hashtag and open 
curlybrace (``#{``), followed by any value and a closing curlybrace (``}``).

::

    var name = "Harold"

    # This function will print out "My name is Harrold" with a newline
    print("My name is #{name}")

In contrast WYSIWYG strings start and end with backticks (`````) and have no 
special formatting.

::

	puts(`Hello World`)

See more
========
:ref:`Language reference documentation<jam-literals-strings>`
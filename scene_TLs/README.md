## Things to take in consideration when editing

More than 2 consecutive spaces makes the game crash, avoid it.

Ideally, the translation lines should contain only Shift-JIS compatible characters, 
by default, most of the english and latin chars are.

Inserting noncompliant or unsupported characters may break things. Be aware of that.

Translation should be done in a single line.

It doesn’t appear to be a character limit, but the textbox has a maximum display
capacity, be aware of that when editing.

There are dynamic lines, example: 'One...| Two...', that are splitted or separated by a 
special DOS CP 437 character. Those lines are splitted into different lines to avoid 
issues.


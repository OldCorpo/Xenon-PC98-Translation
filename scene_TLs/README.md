## Things to take in consideration when editing

More than 2 consecutive spaces makes the game crash, avoid it.

Apparently Japanese style spaces doesn't suffer this problem, still testing them,
example of those can be found at the end of s0001.txt and extra_lines.txt

Ideally, the translation lines should contain only Shift-JIS compatible characters, 
by default, most of the english and latin chars are.

Inserting noncompliant or unsupported characters may break things. Be aware of that.

Translation should be done in a single line.

Line breaks are at 60, 120, 180, 240, anything bigger than the last, will be displayed
on the next screen. But there a few exceptions to that on colored fonts.

Any comments or translation notes should be added to the line after the translation
starting with this sign #, example: #This is a comment.

It doesn’t appear to be a character limit, but the textbox has a maximum display
capacity, be aware of that when editing.

There are dynamic lines, example: 'One...| Two...', that are splitted or separated by a 
special DOS CP 437 character. Those lines are splitted into different lines to avoid 
issues.


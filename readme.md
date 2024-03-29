# Increment Decrement
[![GitHub license](https://img.shields.io/github/license/cgjosephlee/increment_decrement.svg)](https://github.com/cgjosephlee/increment_decrement/blob/master/LICENSE)
[![GitHub tag](https://img.shields.io/github/tag/cgjosephlee/increment_decrement.svg)](https://GitHub.com/cgjosephlee/increment_decrement/tags/)
[![Package Control total downloads](https://img.shields.io/packagecontrol/dt/Increment%20Decrement.svg)](https://packagecontrol.io/packages/Increment%20Decrement)

A Sublime Text plugin to increase/decrease values (integer, float, Roman numerals, boolean, etc.) with one keystroke.

## Features
Inspired by `C-a` and `C-x` in vim and [nextval](https://www.vim.org/scripts/script.php?script_id=4536).

Integers and decimals:

| value  | decrement | increment |
|--------|-----------|-----------|
| 5      | 4         | 6         |
| -1     | -2        | 0         |
| 001    | 000       | 002       |
| 4.99   | 4.98      | 5.00      |
| -1.1   | -1.2      | -1.0      |
| .2     | .1        | .3        |
| 2.     | 1.        | 3.        |

Binary and hexadecimal:

| value  | decrement | increment |
|--------|-----------|-----------|
| 0xe    | 0xd       | 0xf       |
| 0b1010 | 0b1001    | 0b1011    |

Roman numerals:\
*Cases are auto handled.*\
*Caveats: Roman numerals > 100 (rarely used) or < 1 (not applicable) are not supported.*

| value  | decrement | increment |
|--------|-----------|-----------|
| III    | II        | IV        |
| ix     | viii      | x         |

Booleans:\
*Cases are auto handled.*

| value  | decrement | increment |
|--------|-----------|-----------|
| TRUE   | FALSE     | FALSE     |
| True   | False     | False     |
| yes    | no        | no        |

## Installation
### Via Package Control
Install [Package Control](https://sublime.wbond.net/installation) and search for `Increment Decrement`.

### Manual installation
Clone this repo to your package folder `Preferences -> Browse Packages`.

## Usage
Place the cursor around the value or select the wanted value, then hit the keystroke!

Tip: Use multi-cursors to select multiple values.
- Select a region and hit <kbd>cmd</kbd> + <kbd>shift</kbd> + <kbd>l</kbd> to place cursors to every EOL ([official doc](https://www.sublimetext.com/docs/3/multiple_selection_with_the_keyboard.html)).
- Hold <kbd>cmd</kbd> ( <kbd>ctrl</kbd> on windows) and click to place multiple cursors.

### Key-bindings (OSX)
- <kbd>cmd</kbd> + <kbd>ctrl</kbd> + <kbd>a</kbd> : increase the values
- <kbd>cmd</kbd> + <kbd>ctrl</kbd> + <kbd>x</kbd> : decrease the values

### Key-bindings (Windows, Linux)
- <kbd>ctrl</kbd> + <kbd>alt</kbd> + <kbd>a</kbd> : increase the values
- <kbd>ctrl</kbd> + <kbd>alt</kbd> + <kbd>x</kbd> : decrease the values

### Command palette
Hit <kbd>cmd</kbd> + <kbd>shift</kbd> + <kbd>p</kbd> and search `increment` or `decrement`.

## Links
- [Where we started](https://gist.github.com/dtao/2788978)
- [Inc-Dec-Value](https://github.com/rmaksim/Sublime-Text-2-Inc-Dec-Value): A good and similar package, but unmaintained.

## License
MIT

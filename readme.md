# Increment Decrement
Sublime Text plugin to increase/decrease selected values (int, float, bool).

## Features
Inspired by `C-a` and `C-x` in vim and [nextval](https://www.vim.org/scripts/script.php?script_id=4536).
```
value -> decrement/increment
5     -> 4/6
-1    -> -2/0
4.99  -> 4.98/5.00
TURE  -> FALSE/FALSE
Ture  -> False/False
false -> true/true
```

## Installation
Clone this repo to your package folder `Preferences -> Browse Packages`.

*Currently not avalible in package control channel.*

## Usage
Place the cursor around the value or select the wanted value, then hit the keystroke!

Tip: Use multi-cursors to select multiple values.
- Select a region and hit <kbd>cmd</kbd> + <kbd>shift</kbd> + <kbd>l</kbd> to place cursors to every EOL ([official doc](https://www.sublimetext.com/docs/3/multiple_selection_with_the_keyboard.html)).
- Hold <kbd>cmd</kbd> ( <kbd>ctrl</kbd> on windows) and click to place multiple cursors.

### Key-bindings (OSX)
- <kbd>cmd</kbd> + <kbd>opt</kbd> + <kbd>a</kbd> : increase the values
- <kbd>cmd</kbd> + <kbd>opt</kbd> + <kbd>x</kbd> : decrease the values

### Key-bindings (Windows)
- <kbd>ctrl</kbd> + <kbd>alt</kbd> + <kbd>a</kbd> : increase the values
- <kbd>ctrl</kbd> + <kbd>alt</kbd> + <kbd>x</kbd> : decrease the values

### Command palette
Hit <kbd>cmd</kbd> + <kbd>shift</kbd> + <kbd>p</kbd> and search `increment` or `decrement`.

## Contributors
- [dtao (original author)](https://gist.github.com/dtao/2788978)
- [halilim (implement searching while nothing selected)](https://gist.github.com/dtao/2788978#gistcomment-1246653)

## License
MIT

# Rainbow Bonsai

Grow a color-cycling bonsai in your terminal. A tapered trunk branches into five foliage pads, one brush stroke at a time. Press **q** to return to your shell.

## Install

With Homebrew on macOS or Linux:

```sh
brew install okburkard1/tap/rainbow-bonsai
```

Homebrew installs Python for you. To update later, run `brew update` followed by `brew upgrade rainbow-bonsai`.

### Manual installation

Use Python 3.8 or newer and a Unix terminal. Ghostty supports the palette updates that animate the colors. The script uses the Python standard library.

```sh
git clone https://github.com/okburkard1/rainbow-bonsai.git
cd rainbow-bonsai
mkdir -p ~/.local/bin
install -m 755 rainbow-bonsai ~/.local/bin/rainbow-bonsai
```

If your shell doesn't already search that directory, add `export PATH="$HOME/.local/bin:$PATH"` to your shell configuration. You can also run `./rainbow-bonsai` directly from the checkout.

## Try it

```sh
rainbow-bonsai --huge --dirt --infinite
```

Three rows of textured brown soil fill the bottom of the window. The tree grows directly from the soil. When a tree finishes, it holds for four seconds before the next one starts.

| Option | Effect |
| --- | --- |
| `--large` | Grow a larger tree. |
| `--huge` | Size the tree to the window. All sizes grow at one brush stroke every 0.03 seconds. |
| `--dirt` | Replace the pot with soil across the full window width. |
| `--no-pot` | Hide the pot. |
| `--infinite` | Grow a succession of trees. |
| `--wait 10` | Hold each finished tree for ten seconds in infinite mode. |
| `--theme ocean` | Choose rainbow, ocean, sakura, or autumn. |
| `--cycle 16` | Take sixteen seconds to cycle through the colors. |
| `--leaves blossom` | Choose classic, blossom, round, or needle. |
| `--seed 42` | Repeat a tree or sequence at the same terminal dimensions. |

## Test

From the checkout, run `python3 tests/smoke.py ./rainbow-bonsai`. The checks exercise growth, terminal resizing, soil coverage, infinite mode, and restoring the screen on exit.

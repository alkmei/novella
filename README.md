            # Novella

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

> novella lets you manage stories

Novella is a command-line tool that allows users to create and manage stories based on plaintext files.

## Usage

At this moment, novella is very barebones, consisting of just core modules and a dream. Below are planned usages for it.

```shell
novella [OPTIONS] COMMAND [ARGS]...
```

**Commands**:

- `chapter`: Handles chapters
- `compile`: Compiles a story
- `init`: Initializes a story

## `chapter`

```shell
novella chapter [OPTIONS] COMMAND [ARGS]...
novella chapter new TITLE [PATH]
```

## `compile`

```shell
novella compile [PATH]
```

## `init`

```shell
novella init TITLE [PATH]
```

**Options**

- `--author`: Specify author name. Default: Anonymous
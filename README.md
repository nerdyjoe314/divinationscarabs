This software is to calculate which maps in Path of Exile should be favorited to maximize value from the Divination Scarab of Curation.

All prices included are subject to change and personal evaluation. Do your own work for the best value.

## Installation requirements:
SCIP, published under the Apache 2.0 License:

https://www.scipopt.org/index.php#download

ensure that running `scip --version` from the command line correctly outputs 
```
SCIP version x.x.x .......

Copyright (C) 2002-202X Konrad-Zuse-Zentrum fuer Informationstechnik Berlin (ZIB)
```

## Adjusting prices:
To adjust prices, adjust one or the other of the files included in the data folder.
Either adjust the price listed in `cards.json`, or add an overriding price in `overrides.json`

## Maintaining the project:
You can make a pull request, and I'll almost certainly approve it. By 3.25, I'd like to go back over the code and clean things up, but not for now.
This scarab might also get changed. Also in the queue of updates is to offer an option to use HiGHS instead of SCIP, for wider portability. https://ergo-code.github.io/HiGHS/dev/

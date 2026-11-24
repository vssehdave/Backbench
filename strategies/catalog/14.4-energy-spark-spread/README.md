# 14.4 Energy - spark spread

- Section: 14.4
- Asset class: Miscellaneous assets
- Harness status: **not testable: other data not available** - needs swap, TIPS, weather or energy data.

## Description (paper)

The spark spread is the difference between the wholesale price of electricity and the price of natural gas required to produce it. 198 A spark spread can be built by, e.g., taking a short position in electricity futures and a long position in the corresponding number of fuel futures. Such positions are used by electricity producers to hedge against changes in the electricity price or in the cost of fuel, as well as by traders or speculators who want to make a bet on a power plant. The number of fuel futures is determined by the so-called heat rate H, which measures the efficiency with which the plant converts fuel into electricity:

H = QF/QE (516)

Here: Q F is the amount of fuel used to produce the amount of electricity Q E; Q F is measured in MMBtu; Btu = British thermal unit, which is approximately 1,055 Joules; MBtu = 1,000 Btu; MMBtu = 1,000,000 Btu; Q E is measured in Mwh = Megawatt hour; the heat rate H is measured in MMBtu/Mwh. The spark spread is measured in $/Mwh. So, if the price of electricity is PE (measured in $/Mwh) and the price of fuel is PF (measured in $/MMBtu), then the spark spread is given by

S = P E − H P F (517)

The hedge ratio for the futures is affected by the available futures contract sizes. Thus, an electricity futures contract is F E = 736 Mwh, and a gas futures contract is F F = 10 , 000 MMBtu. So, the hedge ratio is given by

h = H FE/FF (518)

which generally is not a whole number. Therefore, it is (approximately, within the desired precision) represented as a ratio h ≈ N F /N E with the lowest possible denominator N E, where N F and N E are whole numbers. Then the hedge consists of buying N F gas futures contracts for every N E sold electricity futures contracts.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 14.4. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

# MVM Showcase Order Solver

A Python-based tool that automatically generates optimal performance orders (setlists) for dance showcases, ensuring no performer appears in consecutive performances.

## Overview

This tool reads a CSV file containing team lineups, cleans the data, and uses a constraint-based algorithm to find valid performance orders where:
- No two consecutive teams share any members
- Specific teams can be locked to fixed positions (start, end, or middle)
- Multiple position constraints can be applied simultaneously

## Quick Start

1. Prepare your CSV file following the naming conventions below
2. Run the Jupyter notebook `mvm_showcase_order.ipynb`
3. Adjust constraints as needed (start team, end team, fixed positions)
4. Get valid setlist options!

---

## CSV Naming Conventions

### **Follow These Rules to Minimize Data Cleaning:**

### 1. **Use Lowercase**
- ✅ **Correct**: `sophia`, `leo`, `andrew`
- ❌ **Avoid**: `Sophia`, `LEO`, `AnDrEw`

### 2. **Use Underscores for Multi-Part Names**
- ✅ **Correct**: `sophia_z`, `andrew_lee`, `leo_shen`
- ❌ **Avoid**: `Sophia Z`, `Andrew Lee`, `Leo Shen`

### 3. **No Periods**
- ✅ **Correct**: `sophia_z`, `sophia_d`
- ❌ **Avoid**: `Sophia Z.`, `Sophia D.`

### 4. **No Leading/Trailing Spaces**
- ✅ **Correct**: `talia`
- ❌ **Avoid**: `talia `, `  talia`, `talia  `

### 5. **Consistent Name Format**
Use the **same exact spelling** for each person throughout the entire CSV:
- ✅ **Correct**: Always use `leo_shen` everywhere
- ❌ **Avoid**: Mixing `leo_s`, `Leo S`, `leo shen`, `Leo Shen`

### 6. **Empty Cells**
If a team has fewer members, leave cells empty (don't use spaces, dashes, or "N/A"):
- ✅ **Correct**: `,,,` (empty cells)
- ❌ **Avoid**: `, , ,` or `,N/A,N/A,` or `,-,-,`

---

## Examples

### ✅ **GOOD CSV (No Cleaning Needed)**
```csv
go,nxde,loco,guilty,bad_villain
meso,angela,ava,sophia_z,andy
sophia_z,sherla,sua,wei_lun,meso
luke,eni,adell,sophia_d,haeun
leo_z,meso,aslan,joey,eni
justin,aslan,elena,vivian,mandy
```

### ❌ **BAD CSV (Requires Heavy Cleaning)**
```csv
go,nxde,loco,guilty,bad_villain
Meso,Angela,Ava ,Sophia Z.,Andy
sophia_z,Sherla,sua,Wei Lun,MESO
Luke,eni,Adell,Sophia D.,Haeun
Leo Z,meso,Aslan,joey,Eni
Justin,aslan,Elena,Vivian ,mandy
```

**Problems in the bad CSV:**
- Mixed capitalization: `Meso` vs `meso` vs `MESO`
- Trailing spaces: `Ava `, `Vivian `
- Periods: `Sophia Z.`, `Sophia D.`
- Spaces in names: `Wei Lun`, `Leo Z` (should be `wei_lun`, `leo_z`)
- Inconsistent formatting: `sophia_z` (row 2) vs `Sophia Z.` (row 1)

---

## Name Normalization Rules

If your CSV doesn't follow the conventions above, the cleaning script will automatically:

1. **Strip whitespace** from all cells
2. **Convert to lowercase**
3. **Remove periods** (`.`)
4. **Replace spaces with underscores** (`_`)

### Transformation Examples:
| Original Input | Normalized Output |
|----------------|-------------------|
| `"Leo Shen"` | `"leo_shen"` |
| `"Sophia Z."` | `"sophia_z"` |
| `"  Talia  "` | `"talia"` |
| `"Andrew Lee"` | `"andrew_lee"` |
| `"Wei Lun"` | `"wei_lun"` |

---

## Best Practices

### ✅ **DO:**
- Use a consistent naming scheme from the start
- Double-check for typos before saving
- Use lowercase + underscores for all names
- Leave cells empty if there's no member (don't add spaces)

### ❌ **DON'T:**
- Mix different name formats for the same person
- Add random spaces or punctuation
- Use abbreviations inconsistently (`leo_s` vs `leo_shen`)
- Leave trailing spaces after names

---

## File Structure

```
mvm_script/
├── F25_LineUp - Sheet1.csv        # Input: Team lineup data
├── mvm_showcase_order.ipynb       # Main notebook with solver
├── mvm_showcase_order.py          # Standalone Python script
└── README.md                      # This file
```

---

## How It Works

1. **Data Import**: Reads CSV with team lineups
2. **Data Cleaning**: Normalizes all names using the rules above
3. **Team Mapping**: Auto-generates a dictionary mapping teams to members
4. **Graph Building**: Creates a compatibility graph where teams are nodes
5. **Constraint Solving**: Uses backtracking to find valid Hamiltonian paths
6. **Output**: Returns valid setlists that satisfy all constraints

---

## Usage Example

```python
# Define constraints
start = "go"
end = "dope"
target_team_1 = "xoxz"
target_position_index_1 = 8  # 9th position (0-indexed)

# Run solver
generator = solver.generate_valid_setlists(
    start_team=start,
    end_team=end
)

# Filter by position constraints
for setlist in generator:
    if setlist[target_position_index_1] == target_team_1:
        print(setlist)
```

---

## Troubleshooting

### Issue: "No valid setlists found"
**Possible causes:**
1. Constraints are too restrictive
2. Member overlap makes some positions impossible
3. Team names in constraints don't match CSV (check spelling/formatting)

**Solution:** 
- Use `solver.explain_pair("team1", "team2")` to check compatibility
- Reduce number of position constraints
- Verify team names match exactly (use lowercase + underscores)

### Issue: "Start team 'X' not found"
**Cause:** Team name doesn't exist in your CSV or formatting doesn't match

**Solution:**
- Check that column headers match exactly
- Ensure you're using the cleaned name format (e.g., `"xoxz"` not `"XOXZ"`)

---

## Contributing

When updating the CSV:
1. Follow the naming conventions above
2. Test with the notebook to ensure it runs
3. Commit with descriptive messages

---

## Questions?

For issues or questions, please open an issue on the [GitHub repository](https://github.com/irenez03/mvm_scripts).

---

**Author:** Irene Zheng  
**Last Updated:** October 17, 2025


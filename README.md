# MVM Scripts

A collection of Python tools for MVM (Mixed Vocal Movements) operations:
1. **Showcase Order Generator** - Automatically generates optimal performance orders
2. **Deliberation Analysis** - Analyzes audition scores and votes to identify top candidates 

## What it does:

This script reads a CSV file containing team lineups, cleans the data, and uses a constraint-based algorithm to find valid performance orders where:
- No two consecutive teams share any members
- Specific dances can be constrained to fixed positions (start, end, or middle)


## How to use:

1. Prepare your CSV file following the naming conventions below
2. Run the Jupyter notebook `mvm_showcase_order.ipynb`
3. Adjust constraints as needed (start team, end team, fixed positions)
4. Run the Script to generate possible show order!

---

## CSV Naming Conventions

### **Follow These Rules to Minimize Data Cleaning:**

### 1. **Use Lowercase**
- ✅ **Correct**: `sophia`, `leo`, `andrew`
- ❌ **Avoid**: `Sophia`, `LEO`, `AnDrEw`

### 2. **Use Underscores First+Last Names**
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

# Deliberation Analysis (`mvm_delibs.ipynb`)

## What it does:

This notebook analyzes audition deliberation data from board member votes and ratings. It:
- Calculates composite scores (accuracy + energy + performance)
- Tracks percentage of "yes" votes from board members
- Analyzes improvement scores
- Identifies top candidates across multiple metrics

## How to use:

1. **Export your audition data as CSV** with the following columns:
   - `Timestamp` - When the vote was submitted
   - `Board member` - Name of the board member
   - `Auditionee Name` - Name of the person auditioning
   - `Rating [Accuracy]` - Accuracy rating (numerical)
   - `Rating [Energy ]` - Energy rating (numerical)
   - `Rating [Performance ]` - Performance rating (numerical)
   - `Rating [Improvement ]` - Improvement rating (numerical)
   - `Initial Vote ` - "Yes" or "No"
   - `Additional Comments?` - Optional comments

2. **Update the file path** in Step 1 of the notebook:
   ```python
   file_path = "/path/to/your/delibs.csv"
   ```

3. **Run all cells** in the notebook to:
   - Load and clean the data
   - Calculate composite scores
   - View top performers by composite score
   - View top performers by improvement
   - Find candidates in top N of both metrics

4. **Adjust the top N threshold** as needed:
   ```python
   N = 20  # Change this to view top 10, 15, 20, etc.
   ```

## Output:

The notebook displays three key results:
1. **All auditionees ranked by composite score** - Overall performance ranking
2. **All auditionees ranked by improvement** - Growth potential ranking
3. **Intersection of top N** - Candidates excelling in both metrics

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


## Questions?

If you run into an issue, please contact Irene at izheng0132@gmail.com

---

**Author:** Irene Zheng  
**Last Updated:** November 20, 2025


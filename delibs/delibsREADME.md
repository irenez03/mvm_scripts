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


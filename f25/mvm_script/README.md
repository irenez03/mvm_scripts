# MVM Showcase Order 

A Python script that automatically generates optimal performance orders for MVM showcases! 

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
**Last Updated:** October 17, 2025


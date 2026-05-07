# Examples

## Compress an observation section
### Before
The matrix shows the following values: branch A is 0.58 at setting 1, 0.59 at setting 2, branch B is 0.57, and branch C is 0.56.

### After
The matrix reveals branch-specific behavior rather than uniform degradation. One branch remains comparatively stable at mild-to-moderate settings, while another branch becomes stronger only under heavier degradation. The pattern establishes a question for mechanism analysis rather than resolving it.

## Expand a mechanism section
### Before
Mechanism X has the best correlation, so it is the cause.

### After
Mechanism X is the only tested explanation that tracks the observed branch transition with both a strong directional relationship and a clear structural fit to the result pattern. The other candidates change measurably, but they do not organize the ranking shifts seen in the main matrix. That makes X the most directly supported mechanism in this setting.

## Turn files into an evidence map
### Before
Several experiment files support the claim.

### After

| Claim | Evidence file | Evidence role | Finality | Risk | Notes |
|---|---|---|---|---|---|
| Branch-wise structure exists | `observation_matrix.csv` | Phenomenon-establishing | Final | Low | Use in main results |
| Occlusion best explains the pattern | `mechanism_summary.json` | Mechanism-discriminating | Final | Low | Compare against alternatives |
| The mechanism has design value | `true_validation.csv` | Consequence/method implication | Representative final | Low | Keep claim narrow |

## Keep the conclusion narrow
### Before
We solved the full problem and proved the method is universally better.

### After
The evidence supports a narrower conclusion: the observed failure pattern is most directly explained by the tested mechanism, and that reading yields a concrete but bounded design implication.

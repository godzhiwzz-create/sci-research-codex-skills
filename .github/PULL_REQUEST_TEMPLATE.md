## Summary

<!-- What changed and why? -->

## Evidence, safety, and compatibility

<!-- Describe evidence boundaries, path/file behavior, timestamp impact, remote actions, and compatibility. -->

## Validation

- [ ] `python -m unittest discover -s tests -v`
- [ ] Affected Skills pass `quick_validate.py`
- [ ] Markdown/HTML links and generated metadata were checked
- [ ] README, Pages, VERSION, and CHANGELOG are synchronized when release behavior changed

## Checklist

- [ ] I preserved the repository name and the eight public Skill names, or documented an approved breaking change.
- [ ] I did not add credentials, private paths, unpublished results, caches, or generated fixtures.
- [ ] New write behavior refuses unsafe overwrite and documents its output path.
- [ ] Claims in documentation are supported by repository behavior or tests.

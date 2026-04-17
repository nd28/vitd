# Roadmap

## v0.2.0

- [ ] Interactive `vitd remind --watch` — live dashboard that refreshes every minute
- [ ] Config file (`~/.vitd/config.toml`) for custom targets, skin type, latitude
- [ ] UV index integration — auto-adjust sun target based on local UV index via open API
- [ ] Streak tracking — consecutive days hitting sun + supplement targets
- [ ] `vitd export` — export history as CSV/JSON for doctor visits

## v0.3.0

- [ ] Weight-based supplement calculator — recommend IU based on body weight
- [ ] Skin type (Fitzpatrick scale) support — adjust sun duration by skin type
- [ ] Season-aware targets — higher doses in winter, lower in summer
- [ ] `vitd graph` — ASCII chart of test history over time
- [ ] Correlation notes — tag symptoms (fatigue, bone pain, mood) and correlate with levels

## v0.4.0

- [ ] Co-nutrient tracking — calcium, magnesium, K2 logging
- [ ] Medication interaction warnings — alert if taking certain drugs that affect D absorption
- [ ] Recovery timeline predictor — estimate weeks to sufficiency based on dose + compliance
- [ ] `vitd doctor` — generate a summary report to share with your physician

## v1.0.0

- [ ] Multi-user support — family member profiles
- [ ] Android/iOS push via Termux or Shortcut integrations
- [ ] i18n — support multiple languages
- [ ] Plugin system — community-contributed nutrition databases
- [ ] Full test suite and CI/CD via GitHub Actions

## Ideas / Maybe

- Integration with Apple Health / Google Fit
- Food database with vit D content per serving
- Blood test OCR — scan lab report and auto-log level
- Community anonymized stats — compare recovery curves

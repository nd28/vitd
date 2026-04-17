# vitd

Terminal-based Vitamin D deficiency tracker and assistant.

## Install

```bash
pip install vitd
```

## Usage

```bash
vitd setup --level 10.8    # Initial setup with your test result
vitd                        # Dashboard
vitd sun 20                 # Log 20 min of sun
vitd supp 2000              # Log 2000 IU supplement
vitd remind                 # Active reminders
vitd tips                   # Personalized tips
vitd history                # Past 7 days
vitd test 35                # Update test result
vitd note "felt tired"      # Add a note
```

## Daily reminder

```bash
echo 'vitd remind' >> ~/.bashrc
```

## License

MIT

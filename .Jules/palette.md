## 2024-05-23 - Android SeekBar Accessibility
**Learning:** SeekBars in Android default to having no text representation for their value. This is a critical usability issue for sighted users (guessing values) and accessibility issue for screen reader users (if no content description is provided).
**Action:** Always pair a SeekBar with a dynamic TextView label and ensure `android:contentDescription` (or a `labelFor` association) is present.

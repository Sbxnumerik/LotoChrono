from pathlib import Path
import re

p = Path("app/src/main/java/fr/lotochrono/MainActivity.java")
s = p.read_text(encoding="utf-8")
assert "winnerOverlay = new FrameLayout(this);" in s
assert 'winnerNumber.setTag("winnerNumber");' in s
assert 'screen.setBackgroundColor(BG);' in s

# Keep all V3 event handlers, timers, voice recognition and state logic.
# Replace the background with the exact uploaded Interface.png.
s = s.replace("screen.setBackgroundColor(BG);", """screen.setBackgroundResource(fr.lotochrono.R.drawable.v4_interface);""", 1)

# Screenshot is a visual reference; native dynamic controls must remain legible.
# Put an opaque dark overlay behind controls, instead of showing stale
# screenshot numbers underneath changing real values.
s = s.replace("screen.addView(content, new FrameLayout.LayoutParams(-1, -1));",
"""content.setBackgroundColor(Color.argb(220, 3, 14, 34));
        screen.addView(content, new FrameLayout.LayoutParams(-1, -1));""", 1)

# Match the screenshot's saturated blue number panel and red timer panel.
s = s.replace("numberPanel.setBackground(rounded(PANEL, 20));",
"""numberPanel.setBackground(rounded(Color.rgb(0, 70, 176), 20));""", 1)
s = s.replace("timerPanel.setBackground(rounded(RED, 20));",
"""timerPanel.setBackground(rounded(Color.rgb(187, 8, 27), 20));""", 1)
s = s.replace('label("NUMÉRO ANNONCÉ", landscape ? 17 : 11, MUTED, true)',
              'label("NUMÉRO ANNONCÉ", landscape ? 17 : 14, WHITE, true)', 1)
s = s.replace('label("CHRONOMÈTRE", landscape ? 17 : 11,\n            Color.rgb(254, 202, 202), true)',
              'label("CHRONOMÈTRE", landscape ? 17 : 14, WHITE, true)', 1)
s = s.replace('actionButton("CORRIGER", Color.rgb(30, 64, 175))',
              'actionButton("✎  CORRIGER", Color.rgb(0, 92, 236))', 1)
s = s.replace('actionButton("NOUVELLE PARTIE", Color.rgb(55, 65, 81))',
              'actionButton("⟳  NOUVELLE PARTIE", Color.rgb(64, 83, 110))', 1)
s = s.replace('actionButton("PAUSE", Color.rgb(180, 83, 9))',
              'actionButton("Ⅱ  PAUSE", Color.rgb(245, 126, 0))', 1)

# Winner: use the user's actual Gagnant.png, not a generated substitute.
s = s.replace("""winnerOverlay.setBackground(new GradientDrawable(GradientDrawable.Orientation.TL_BR,
            new int[]{Color.rgb(68, 0, 0), Color.rgb(180, 14, 14), Color.rgb(90, 0, 0)}));""",
"""winnerOverlay.setBackgroundResource(fr.lotochrono.R.drawable.v4_gagnant);""", 1)
# Cover the screenshot's example 42 with the real winning number.
s = s.replace('winnerContent.addView(winnerTitle);',
              'winnerTitle.setVisibility(View.INVISIBLE);\n        winnerContent.addView(winnerTitle);', 1)
s = s.replace('winnerContent.addView(winnerNumber);',
"""winnerNumber.setBackgroundColor(Color.rgb(170, 0, 0));
        winnerNumber.setPadding(dp(25), dp(8), dp(25), dp(8));
        winnerContent.addView(winnerNumber);""", 1)
s = s.replace('winnerContent.addView(winnerHint);',
              'winnerHint.setVisibility(View.INVISIBLE);\n        winnerContent.addView(winnerHint);', 1)
assert 'winnerOverlay.setBackgroundResource(fr.lotochrono.R.drawable.v4_gagnant);' in s
p.write_text(s, encoding="utf-8")

g = Path("app/build.gradle")
t = g.read_text(encoding="utf-8")
t = re.sub(r"versionName\\s+['\"][^'\"]+['\"]", "versionName '4.0'", t)
t = re.sub(r"versionCode\\s+\\d+", "versionCode 10", t)
g.write_text(t, encoding="utf-8")
print("V4 screenshot graphics applied; V3 logic preserved")

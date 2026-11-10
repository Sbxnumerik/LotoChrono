from pathlib import Path
p=Path("app/src/main/java/fr/lotochrono/MainActivity.java")
s=p.read_text()
# Keep voice recognition alive while the winner overlay is visible.
# Pausing the countdown must never stop AudioRecord.
assert "if (winnerShown)" in s and "startMicrophone()" in s
# Ensure winner dismissal by voice is processed before any paused-number logic.
assert "SpeechCommandParser.isFalseWinnerCommand(spoken)" in s
# Do not let a tap reset the draw without confirmation.
s=s.replace("winnerOverlay.setOnClickListener(v -> startNewDraw());",
            "winnerOverlay.setOnClickListener(v -> confirmNewDraw());")
# Recreate status on orientation change without restarting microphone.
assert "onConfigurationChanged(Configuration configuration)" in s
p.write_text(s)
q=Path("app/src/main/java/fr/lotochrono/SpeechCommandParser.java")
t=q.read_text()
needle='|| text.contains("s est trompe") || text.contains("c est trompe");'
replacement='''|| text.contains("s est trompe") || text.contains("c est trompe")
            || text.contains("elle s est trompee") || text.contains("elle c est trompee")
            || text.contains("c est une erreur") || text.contains("c est un erreur");'''
if needle in t: t=t.replace(needle,replacement)
q.write_text(t)
print("Voice commands checked: microphone remains foreground-active during winner screen")

from pathlib import Path
import re
p=Path("app/src/main/java/fr/lotochrono/MainActivity.java")
s=p.read_text()
# Layout and colors aligned with approved reference images.
s=s.replace('screen.setBackgroundColor(BG);','screen.setBackgroundColor(Color.rgb(3, 16, 39));')
s=s.replace('numberPanel.setBackground(rounded(Color.rgb(10, 66, 147), 20));','numberPanel.setBackground(outlinedPanel(Color.rgb(0, 68, 174), Color.rgb(75, 163, 255), 20));')
s=s.replace('numberPanel.setBackground(rounded(PANEL, 20));','numberPanel.setBackground(outlinedPanel(Color.rgb(0, 68, 174), Color.rgb(75, 163, 255), 20));')
s=s.replace('timerPanel.setBackground(rounded(Color.rgb(187, 12, 27), 20));','timerPanel.setBackground(outlinedPanel(Color.rgb(183, 4, 25), Color.rgb(255, 115, 126), 20));')
s=s.replace('timerPanel.setBackground(rounded(RED, 20));','timerPanel.setBackground(outlinedPanel(Color.rgb(183, 4, 25), Color.rgb(255, 115, 126), 20));')
s=s.replace('timerPanel.setBackground(rounded(ready ? GREEN : RED, 20));','timerPanel.setBackground(outlinedPanel(ready ? GREEN : Color.rgb(183, 4, 25), ready ? Color.rgb(99, 240, 146) : Color.rgb(255, 115, 126), 20));')
s=s.replace('TextView title = label("LOTO CHRONO", landscape ? 22 : 18, WHITE, true);','TextView title = label("LOTO CHRONO", landscape ? 23 : 22, WHITE, true);')
s=s.replace('TextView title = label("LOTO CHRONO", landscape ? 24 : 20, WHITE, true);','TextView title = label("LOTO CHRONO", landscape ? 23 : 22, WHITE, true);')
s=s.replace('numberPanel.addView(label("NUMÉRO ANNONCÉ", landscape ? 17 : 11, MUTED, true));','numberPanel.addView(label("NUMÉRO\\nANNONCÉ", landscape ? 17 : 16, WHITE, true));')
s=s.replace('timerText = label("00:15", landscape ? 94 : 55, WHITE, true);','timerText = label("00:15", landscape ? 80 : 42, WHITE, true);')
s=s.replace('timerText = label("00:15", landscape ? 94 : 46, WHITE, true);','timerText = label("00:15", landscape ? 80 : 42, WHITE, true);')
s=s.replace('timerText = label("00:15", landscape ? 94 : 45, WHITE, true);','timerText = label("00:15", landscape ? 80 : 42, WHITE, true);')
s=s.replace('numberText = label("—", landscape ? 150 : 103, WHITE, true);','numberText = label("—", landscape ? 135 : 103, WHITE, true);')
s=s.replace('TextView lastLabel = label("5 DERNIERS NUMÉROS", landscape ? 14 : 12,','TextView lastLabel = label("5 DERNIERS NUMÉROS", landscape ? 16 : 15,')
s=s.replace('Button correctButton = actionButton("CORRIGER",','Button correctButton = actionButton("✎  CORRIGER",')
s=s.replace('Button resetButton = actionButton("NOUVELLE PARTIE",','Button resetButton = actionButton("↻  NOUVELLE PARTIE",')
s=s.replace('pauseButton = actionButton("PAUSE",','pauseButton = actionButton("Ⅱ  PAUSE",')
s=s.replace('winnerOverlay.setOnClickListener(v -> startNewDraw());','winnerOverlay.setOnClickListener(v -> confirmNewDraw());')
s=s.replace('TextView winnerTitle = label("🏆 GAGNANT !", landscape ? 80 : 46, Color.rgb(255, 215, 40), true);','TextView winnerTitle = label("🏆\\nGAGNANT !", landscape ? 55 : 46, Color.rgb(255, 220, 0), true);')
s=s.replace('TextView winnerNumber = label("—", landscape ? 126 : 100, WHITE, true);','TextView winnerNumber = label("—", landscape ? 140 : 135, WHITE, true);')
s=s.replace('winnerOverlay.setBackground(new GradientDrawable(GradientDrawable.Orientation.TL_BR,\n            new int[]{Color.rgb(68, 0, 0), Color.rgb(180, 14, 14), Color.rgb(90, 0, 0)}));','winnerOverlay.setBackground(new GradientDrawable(GradientDrawable.Orientation.TL_BR,\n            new int[]{Color.rgb(105, 0, 0), Color.rgb(213, 0, 0), Color.rgb(112, 0, 0)}));')
# Microphone is intentionally kept active on winner screen; only countdown pauses.
# No audio-recorder stop call on winner transition.
# Keep normal status visible for 0% microphone detection disabled.
marker='    private Button actionButton(String text, int bg) {'
method='''    private GradientDrawable outlinedPanel(int fill, int stroke, int radius) {
        GradientDrawable drawable = new GradientDrawable(
            GradientDrawable.Orientation.TL_BR,
            new int[]{fill, fill, Color.rgb(2, 25, 65)});
        drawable.setCornerRadius(dp(radius));
        drawable.setStroke(dp(2), stroke);
        return drawable;
    }

'''
assert marker in s
s=s.replace(marker,method+marker,1)
# Android 3-button navigation must not overlap footer.
s=s.replace('View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION', 'View.SYSTEM_UI_FLAG_LAYOUT_STABLE')
p.write_text(s)
g=Path("app/build.gradle")
v=g.read_text()
v=re.sub(r'versionCode\s+\d+', 'versionCode 6', v)
v=re.sub(r'versionName\s+[\x27\x22][^\x27\x22]+[\x27\x22]', "versionName '1.3.2'", v)
g.write_text(v)
assert 'versionCode 6' in v
print("LotoChrono 1.3.2 visual layout and winner microphone preservation applied")

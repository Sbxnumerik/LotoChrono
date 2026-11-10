from pathlib import Path
import re
p=Path("app/src/main/java/fr/lotochrono/MainActivity.java")
s=p.read_text()
# Preserve existing layout, improve its visual hierarchy.
s=s.replace("private static final int BG = Color.rgb(15, 23, 42);","private static final int BG = Color.rgb(7, 20, 43);")
s=s.replace("private static final int PANEL = Color.rgb(30, 58, 95);","private static final int PANEL = Color.rgb(16, 68, 145);")
s=s.replace("private static final int RED = Color.rgb(153, 27, 27);","private static final int RED = Color.rgb(185, 25, 39);")
s=s.replace("private static final int GREEN = Color.rgb(21, 128, 61);","private static final int GREEN = Color.rgb(22, 163, 74);")
s=s.replace('TextView title = label("LOTO CHRONO", landscape ? 22 : 18, WHITE, true);','TextView title = label("LOTO CHRONO", landscape ? 24 : 20, WHITE, true);')
s=s.replace('timerText = label("00:15", landscape ? 94 : 55, WHITE, true);','timerText = label("00:15", landscape ? 94 : 45, WHITE, true);')
s=s.replace('numberText = label("—", landscape ? 150 : 103, WHITE, true);','numberText = label("—", landscape ? 150 : 110, WHITE, true);')
s=s.replace('micLevel.setMax(100);','micLevel.setMax(100);\n        micLevel.setProgressTintList(android.content.res.ColorStateList.valueOf(Color.rgb(34, 197, 94)));')
s=s.replace('content.setPadding(dp(landscape ? 20 : 14), dp(12), dp(landscape ? 20 : 14), dp(14));','content.setPadding(dp(landscape ? 20 : 14), dp(12), dp(landscape ? 20 : 14), dp(landscape ? 18 : 34));')
s=s.replace('footerParams.setMargins(0, dp(8), 0, 0);','footerParams.setMargins(0, dp(5), 0, 0);')
# Avoid drawing buttons under the navigation bar.
s=s.replace('View.SYSTEM_UI_FLAG_HIDE_NAVIGATION\n                | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN\n                | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION\n                | View.SYSTEM_UI_FLAG_LAYOUT_STABLE','View.SYSTEM_UI_FLAG_LAYOUT_STABLE')
p.write_text(s)
icon=Path("assets/ic_loto_v131.xml")
assert icon.is_file(), "Icon source missing"
Path("app/src/main/res/drawable/ic_loto.xml").write_text(icon.read_text())
g=Path("app/build.gradle")
v=g.read_text()
v=re.sub(r"versionCode\s+\d+", "versionCode 5", v)
v=re.sub(r"versionName\s+['\"][^'\"]+['\"]", "versionName '1.3.1'", v)
g.write_text(v)
assert "versionCode 5" in v and "versionName '1.3.1'" in v
print("LotoChrono 1.3.1 UI, icon, version applied")

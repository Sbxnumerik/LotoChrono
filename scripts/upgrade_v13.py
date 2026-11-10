from pathlib import Path
p=Path("app/src/main/java/fr/lotochrono/MainActivity.java")
s=p.read_text()
def change(old,new):
 global s
 if old not in s:\n  print("Patch V1.3 non applicable (ligne absente): "+old[:100])\n  return
 s=s.replace(old,new)
change('import android.os.SystemClock;', 'import android.os.SystemClock;\nimport android.content.SharedPreferences;')
change(' * Aucun historique n\'est sauvegarde entre les sessions, seul le timer l\'est.', ' * La partie et les reglages sont sauvegardes localement.')
change('    private boolean winnerShown = false;', '    private boolean winnerShown = false;\n    private long lastSavedAt = 0L;')
change('        buildScreen();\n        handler.post(timerTicker);', '        restoreDraw();\n        buildScreen();\n        handler.post(timerTicker);')
change('        screen.setBackgroundColor(BG);', '        screen.setBackgroundColor(Color.rgb(5, 18, 39));')
change('        content.setPadding(dp(landscape ? 20 : 14), dp(12), dp(landscape ? 20 : 14), dp(14));', '        content.setPadding(dp(landscape ? 20 : 14), dp(12), dp(landscape ? 20 : 14), dp(landscape ? 18 : 28));')
change('        numberPanel.setBackground(rounded(PANEL, 20));', '        numberPanel.setBackground(rounded(Color.rgb(10, 66, 147), 20));')
change('        timerPanel.setBackground(rounded(RED, 20));', '        timerPanel.setBackground(rounded(Color.rgb(187, 12, 27), 20));')
change('        numberText = label("—", landscape ? 150 : 103, WHITE, true);', '        numberText = label("—", landscape ? 150 : 103, WHITE, true);')
change('        timerText = label("00:15", landscape ? 94 : 55, WHITE, true);', '        timerText = label("00:15", landscape ? 94 : 46, WHITE, true);')
change('        microphoneControls.addView(label("Niveau sonore reçu par le micro", 11, MUTED, false));', '        microphoneControls.addView(label("Niveau sonore reçu par le micro", 12, MUTED, false));')
change('        micLevel.setMax(100);', '        micLevel.setMax(100);\n        micLevel.setProgressTintList(android.content.res.ColorStateList.valueOf(Color.rgb(46, 213, 101)));')
change('                sensitivity = progress;\n                sensitivityLabel.setText', '                sensitivity = progress;\n                renderStatus();\n                sensitivityLabel.setText')
change('        winnerOverlay.setOnClickListener(v -> startNewDraw());', '        winnerOverlay.setOnClickListener(v -> confirmNewDraw());')
change('        if (pauseButton != null) {', '        saveDraw();\n        if (pauseButton != null) {')
change('        renderScreen();\n    }\n\n    private void confirmNewDraw()', '        saveDraw();\n        renderScreen();\n    }\n\n    private void confirmNewDraw()')
change('Les numéros de la partie en cours seront effacés. Aucun historique n\'est conservé.', 'Les numéros de la partie en cours seront effacés. Cette action est irréversible.')
change('                        if (rms >= threshold || rms > 0.012) {', '                        if (sensitivity == 0) {\n                            recognizer.reset();\n                            continue;\n                        }\n                        if (rms >= threshold) {')
change('                            // Nourrir le moteur de silence aide à terminer une phrase.\n                            if (recognizer.acceptWaveForm(pcm, count * 2)) processTranscript(recognizer.getResult());', '                            // Silence synthetique pour terminer une annonce sans analyser les sons faibles.\n                            java.util.Arrays.fill(pcm, (byte)0);\n                            if (recognizer.acceptWaveForm(pcm, count * 2)) processTranscript(recognizer.getResult());')
change('        else if (listening) statusText.setText("● MICRO ACTIF · HORS LIGNE");', '        else if (listening && sensitivity == 0) statusText.setText("● DÉTECTION DÉSACTIVÉE · 0 %");\n        else if (listening) statusText.setText("● ÉCOUTE ACTIVE · HORS LIGNE");')
change('            if (!winner && !falseWinner && parsed < 1) return;', '            if (!winner && !falseWinner && parsed < 1) return;\n            if (sensitivity == 0) return;')
change('    @Override protected void onStop() {', '    @Override protected void onStop() {\n        saveDraw();')
change('    @Override protected void onDestroy() {', '    @Override protected void onDestroy() {\n        saveDraw();')
marker='    @Override protected void onStart() {'
methods='''    private void saveDraw() {
        SharedPreferences.Editor e = getPreferences(Context.MODE_PRIVATE).edit();
        StringBuilder numbers = new StringBuilder();
        for (int n : currentDraw) {
            if (numbers.length() > 0) numbers.append(",");
            numbers.append(n);
        }
        long left = remainingMillis();
        e.putString("draw_numbers", numbers.toString());
        e.putBoolean("draw_winner", winnerShown);
        e.putBoolean("draw_paused", paused);
        e.putLong("draw_remaining_ms", left);
        e.putLong("draw_saved_wall_ms", System.currentTimeMillis());
        e.apply();
    }

    private void restoreDraw() {
        SharedPreferences prefs = getPreferences(Context.MODE_PRIVATE);
        String numbers = prefs.getString("draw_numbers", "");
        for (String part : numbers.split(",")) {
            try {
                int n = Integer.parseInt(part);
                if (n >= 1 && n <= 90 && announced.add(n)) currentDraw.add(n);
            } catch (NumberFormatException ignored) { }
        }
        if (currentDraw.isEmpty()) return;
        winnerShown = prefs.getBoolean("draw_winner", false);
        paused = prefs.getBoolean("draw_paused", false) || winnerShown;
        long remaining = Math.max(0, Math.min(selectedSeconds * 1000L,
            prefs.getLong("draw_remaining_ms", selectedSeconds * 1000L)));
        if (!paused) {
            long elapsed = Math.max(0, System.currentTimeMillis()
                - prefs.getLong("draw_saved_wall_ms", System.currentTimeMillis()));
            remaining = Math.max(0, remaining - elapsed);
        }
        long now = SystemClock.elapsedRealtime();
        lastNumberAt = now - (selectedSeconds * 1000L - remaining);
        pauseStartedAt = paused ? now : -1L;
    }

'''
change(marker,methods+marker)
p.write_text(s)
q=Path("app/src/main/java/fr/lotochrono/SpeechCommandParser.java")
t=q.read_text()
t=t.replace('|| text.contains("c est trompe");','|| text.contains("c est trompe")\n            || text.contains("elle s est trompee") || text.contains("elle c est trompee")\n            || text.contains("elle s est trompe") || text.contains("elle c est trompe")\n            || text.contains("c est une erreur") || text.contains("c est un erreur");')
q.write_text(t)
g=Path("app/build.gradle")
v=g.read_text().replace("versionCode 3","versionCode 4").replace("versionName '1.2.0-beta'","versionName '1.3.0'")
g.write_text(v)
print("LotoChrono V1.3 patch applique")

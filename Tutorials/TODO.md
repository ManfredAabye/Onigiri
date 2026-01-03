# TODO-Liste für Blender 5.0 Kompatibilität (Onigiri)

## Erledigte Schritte

- [x] Property-Deklarationen in `Onigiri/__init__.py` (Sliders, CharacterConverter, Onemap) auf Blender 5.0-kompatibles Format umgestellt
- [x] Property-Deklarationen in `Onigiri/template_editor.py` und `Onigiri/animesh.py` angepasst
- [x] Fehlerprüfung nach Property-Anpassungen durchgeführt

## Offene Aufgaben

- [ ] Alle weiteren PropertyGroup- und Operator-Property-Deklarationen im gesamten Projekt auf Blender 5.0-kompatibles Format umstellen
- [ ] Systematische Prüfung aller Module auf weitere inkompatible Property-Deklarationen
- [ ] Fehlerprüfung nach jeder Anpassung (z.B. mit VS Code Fehlerliste)
- [ ] Dokumentation der wichtigsten Änderungen für Nutzer (README/CHANGELOG)
- [ ] Endgültiger Test des Addons in Blender 5.0

## Hinweise

- Property-Deklarationen müssen als Zuweisung mit Typ erfolgen, z.B.:

  ```python
  my_prop: bpy.props.BoolProperty = bpy.props.BoolProperty(default=True)
  ```

- Nach jeder Änderung Fehler prüfen und ggf. weitere Anpassungen vornehmen.

# Handbuch: Mixamo-Avatar für OpenSim/Second Life als glTF exportieren

Dieses Howto beschreibt, wie du ein mit Mixamo geriggtes Avatar-Modell in Blender importierst, für OpenSim/Second Life vorbereitest und als glTF exportierst.

## Voraussetzungen

- Blender 5.0 oder neuer
- Onigiri-Addon installiert und aktiviert
- Mixamo-Avatar als FBX-Datei

## Schritt 1: Mixamo-Avatar importieren

1. Starte Blender und öffne eine neue Szene.
2. Gehe zu `Datei > Importieren > FBX (.fbx)`.
3. Wähle deine Mixamo-Avatar-FBX-Datei aus und importiere sie.
4. Prüfe, ob das Modell und das Rig korrekt angezeigt werden.

## Schritt 2: Rig für OpenSim/Second Life vorbereiten

1. Wähle das importierte Armature-Objekt aus.
2. Öffne das Onigiri-Panel (meist in den Eigenschaften oder im 3D-View rechts).
3. Wähle im Onigiri-Panel die Funktion zum Konvertieren oder Mappen auf ein OpenSim/Second Life-kompatibles Rig:
    - Nutze ggf. die "Character Converter"- oder "Mapper"-Funktion.
    - Wähle als Ziel-Plattform "Second Life / OpenSim".
    - Folge den Anweisungen im Addon, um die Bones korrekt zuzuordnen.
4. Überprüfe die Bone-Namen und Hierarchie. Passe sie ggf. an die OpenSim/SL-Standards an (z.B. "mPelvis", "mTorso", "mHead" usw.).
5. Optional: Nutze die Onigiri-Tools, um Vertex-Gruppen, Gewichtungen und Pose zu optimieren.

## Schritt 3: Modell bereinigen und testen

1. Entferne nicht benötigte Meshes, Bones oder Hilfsobjekte.
2. Prüfe die Skinning-Gewichte und Animationen (falls vorhanden).
3. Stelle sicher, dass das Modell im T-Pose oder A-Pose steht (je nach Zielplattform).

## Schritt 4: Export als glTF

1. Wähle das Armature-Objekt und das Mesh aus.
2. Gehe zu `Datei > Exportieren > glTF 2.0 (.glb/.gltf)`.
3. Wähle die Option `Nur Ausgewählte Objekte` ("Selected Objects").
4. Stelle sicher, dass "Animationen" aktiviert ist, falls du Animationen exportieren möchtest.
5. Wähle einen Speicherort und exportiere die Datei.

## Schritt 5: Import in OpenSim/Second Life

1. Nutze einen Viewer oder ein Import-Tool, das glTF unterstützt (z.B. DreamGrid, OpenSim-Distributionen mit glTF-Support).
2. Lade das glTF-Modell hoch und prüfe das Rigging und die Animationen.
3. Passe ggf. Materialien und Texturen an.

## Tipps & Hinweise

- Mixamo-Rigs müssen oft manuell auf die OpenSim/SL-Bone-Struktur gemappt werden.
- Onigiri bietet Tools zum automatischen und manuellen Mapping.
- Teste das Modell nach dem Upload in einer Testregion.
- Für komplexe Avatare empfiehlt sich ein Zwischenspeichern als Blender-Datei.

---
Fragen oder Probleme? Siehe README, CHANGELOG oder die Onigiri-Dokumentation für weitere Hinweise.

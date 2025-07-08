# Ready Player Me Avatare in Second Life & OpenSim (mit Onigiri)**  

## **Was du brauchst:**  

1. **Blender** (kostenlos von [blender.org](https://blender.org)).  
2. **Onigiri-Add-on** für Blender:  
   - Lade die neueste Version hier herunter: [GitHub Onigiri](https://github.com/aiaustin/Onigiri) (nutze die Datei *Onigiri-2025-01-03-fix-01.zip*).  
   - Installiere sie in Blender unter *Bearbeiten → Einstellungen → Add-ons*.  

## **Vorbereitung:**  

- **Avatar herunterladen:**  
  - Gehe zu [readyplayer.me](https://readyplayer.me), erstelle deinen Avatar und lade ihn als **.glb-Datei** herunter.  
  - Füge diese Parameter an die Download-URL an, um die beste Qualität zu erhalten:  
    `?textureAtlas=none&textureSizeLimit=1024&textureFormat=png&pose=T`  

## **Schritt-für-Schritt-Anleitung:**  

1. **Avatar in Blender importieren:**  
   - Öffne Blender, lösche Standardobjekte (z. B. Würfel) und importiere die *.glb*-Datei.  
   - Prüfe, ob der Avatar in **T-Pose** steht.  

2. **Finger anpassen:**  
   - Second Life benötigt gespreizte Finger. Nutze die Pose-Datei *ReadyPlayerMe-T-Pose-Splayed-Hands-Only.bpl* (downloadbar [hier](https://openvce.net/resources/downloads/ReadyPlayerMe/Onigiri/)).  
   - Aktiviere die Pose unter *Animation → Pose Library*.  

3. **Avatar für Second Life/OpenSim konvertieren:**  
   - Wähle in Onigiri *Character Converter → Load Map* und lade *readyplayerme.onim*.  
   - Klicke auf **Convert** und aktiviere **Project Full Rig**.  
   - Exportiere als **Collada (.dae)-Datei**.  

4. **In Second Life/OpenSim hochladen:**  
   - Lade die *.dae*-Datei hoch:  
     - Setze *Level of Detail (LOD)* auf **0**.  
     - Wähle *Physics* auf **Lowest**.  
     - Aktiviere **Include Skin Weights** und **Include Joint Positions**.  

5. **Avatar anpassen:**  
   - Füge eine **Alpha-Maske** hinzu, um den Standard-Avatar zu verstecken.  
   - Texturiere den Avatar mit den mitgelieferten **Diffuse-** und **Normal-Maps**.  
   - *Tipp:* Du kannst Haarfarben mit einer einfachen Farbtextur ändern.  

## **Wichtige Hinweise:**  

- **Lizenz:** Ready Player Me-Avatare sind nur für **nicht-kommerzielle Nutzung** (CC BY-NC 4.0).  
- **Alternative:** Falls Onigiri nicht funktioniert, probiere **Bento Buddy** (kostenpflichtig ab 2023).  

## **Tipps für Fortgeschrittene:**  

- **Texturen wiederverwenden:** Gleiche Haut-/Haartexturen sparen Upload-Kosten.  
- **Hände entspannen:** Nutze das *bentohandrelax*-Script für natürlichere Posen.  

---

**Fertig!** Dein Ready Player Me-Avatar ist jetzt in Second Life/OpenSim nutzbar.  
Bei Fragen hilft die [GitHub-Seite](https://github.com/aiaustin/Onigiri) weiter.  

---

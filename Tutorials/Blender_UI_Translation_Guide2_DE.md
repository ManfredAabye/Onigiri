# Schritt-für-Schritt-Anleitung translate Onigiri-Add-on

Hier ist eine **einfache Schritt-für-Schritt-Anleitung**, um das **Onigiri-Add-on** für Blender mit einer `.po`/`.mo`-Datei zu übersetzen:

---

## **1. Vorbereitung**

- **Lade das Add-on herunter**:  
  - Hol dir die neueste Version von [GitHub: ManfredAabye/Onigiri](https://github.com/ManfredAabye/Onigiri) (als ZIP oder via `git clone`).  
  - Entpacke es in einen Ordner (z. B. `Onigiri-master`).  

- **Installiere benötigte Tools**:  
  - **Python** (bereits in Blender enthalten).  
  - **Gettext-Tools** (für `.po`/`.mo`-Dateien):  
    - **Windows**: Lade [gettext für Windows](https://mlocati.github.io/articles/gettext-iconv-windows.html).  
    - **Linux/macOS**: Nutze deinen Paketmanager (z. B. `sudo apt install gettext`).  

---

### **2. Übersetzbare Texte extrahieren**

1. **Erstelle eine `.pot`-Datei** (Template):  
   - Navigiere im Terminal zum Add-on-Ordner (z. B. `Onigiri-master`).  
   - Führe diesen Befehl aus, um alle übersetzbaren Strings zu sammeln:  

     ```bash
     find . -name "*.py" | xargs xgettext --from-code=UTF-8 -o translations/onigiri.pot
     ```  

   - *Falls der Ordner `translations` nicht existiert, erstelle ihn vorher.*  

2. **Erstelle eine `.po`-Datei für deine Sprache** (z. B. Deutsch):  

   ```bash
   msginit -i translations/onigiri.pot -o translations/de.po -l de_DE
   ```  

   - Öffne die `de.po`-Datei mit einem Editor wie **Poedit** oder **VS Code** und übersetze alle `msgid`-Einträge.  

---

## **3. Übersetzung in das Add-on integrieren**

1. **Konvertiere `.po` zu `.mo`** (binäres Format):  

   ```bash
   msgfmt translations/de.po -o translations/de.mo
   ```  

2. **Füge die Übersetzung dem Add-on hinzu**:  
   - Erstelle im Add-on-Ordner die Struktur:  

```bash
     Onigiri/
     ├── __init__.py
     ├── translations/
     │   ├── de.po
     │   ├── de.mo
     │   └── ...
```  

- **Bearbeite `__init__.py`**: Füge diesen Code hinzu, um die Übersetzung zu registrieren:  

     ```python
     import os
     import bpy

     # Übersetzung laden
     def register():
         bpy.app.translations.register(__name__, {
             "de_DE": {
                 # Hier die Übersetzungen eintragen (optional, falls nicht dynamisch geladen)
             },
         })

     def unregister():
         bpy.app.translations.unregister(__name__)

     # Automatische .mo-Datei-Nutzung (Blender erwartet sie unter locale/de/LC_MESSAGES/)
     if bpy.app.version >= (2, 80):
         from bpy.utils import resource_path
         locale_dir = os.path.join(os.path.dirname(__file__), "translations")
     else:
         locale_dir = os.path.join(bpy.utils.user_resource('SCRIPTS'), "addons", "Onigiri", "translations")
     ```  

---

## **4. Testen der Übersetzung**

1. **Installiere das Add-on in Blender**:  
   - Gehe zu `Bearbeiten > Einstellungen > Add-ons > Installieren` und wähle die `Onigiri.zip`-Datei.  
2. **Aktiviere die Sprache**:  
   - In Blender: `Bearbeiten > Einstellungen > Sprache` auf **Deutsch** stellen.  
   - Starte Blender neu, um die Übersetzung zu laden.  

---

## **5. (Optional) Weblate für Teamarbeit**

Falls du mit anderen zusammenarbeitest:  

- **Richte ein Weblate-Projekt ein** ([weblate.org](https://weblate.org/)) und lade die `.pot`-Datei hoch.  
- Teammitglieder können dann direkt online übersetzen.  

---

## **Tipps**

- **Poedit**: Nutze die Software [Poedit](https://poedit.net/), um `.po`-Dateien komfortabel zu bearbeiten.  
- **Blender-Dokumentation**: Siehe [Offizieller Übersetzungsleitfaden](https://developer.blender.org/docs/handbook/translating/translator_guide/) für fortgeschrittene Methoden.  
- **Fehlerbehebung**:  
  - Falls die Übersetzung nicht erscheint, prüfe:  
    - Korrekter Pfad der `.mo`-Datei (Blender erwartet `locale/de/LC_MESSAGES/onigiri.mo`).  
    - Syntaxfehler in der `__init__.py`.  

---

**Fertig!** Dein Onigiri-Add-on ist jetzt übersetzbar.  
👉 **Beispiel-Projektstruktur**: [GitHub: ManfredAabye/Onigiri/issues](https://github.com/ManfredAabye/Onigiri/issues) (frage dort bei Problemen!).

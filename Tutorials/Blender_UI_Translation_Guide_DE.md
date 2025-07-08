# **Blender UI Translation Guide**

Hier ist die übersichtliche deutsche Übersetzung des **Blender UI Translation Guide** in einfacher Sprache:

---

## **Blender Übersetzungs-Leitfaden**  

*Wie du die Blender-Oberfläche in deiner Sprache verbessern kannst*  

## **1. Voraussetzungen**  

- **Konto erstellen** auf der [Blender-Übersetzungs-Website](https://developer.blender.org/projects/translations/).  
- **Mitglied werden**: Frage im [Translations-Chat](https://blender.chat/channel/translations) oder erstelle ein Ticket, um dem Übersetzer-Team beizutreten.  
- **Abonniere** das [Translation-Forum](https://devtalk.blender.org/tag/translations) für Updates.  

---

## **2. Übersetzen mit Weblate**  

Die meisten Übersetzungen werden auf der **Weblate-Plattform** bearbeitet:  

- **Basiskonten** können Vorschläge machen (müssen von Teammitgliedern geprüft werden).  
- **Aktive Übersetzer** können Änderungen direkt übernehmen.  
- **Glossar nutzen**: Hilft, Begriffe einheitlich zu übersetzen (z. B. "Shader" → "Schattierer").  

### **Häufige Probleme**  

- **Fehlende Übersetzungen**: Manchmal vergessen Entwickler, Text als "übersetzbar" zu markieren. Melde dies im [Tracker](https://developer.blender.org/maniphest/task/edit/form/1/).  
- **Mehrdeutige Begriffe**: Wörter wie "Light" (Licht/Gewicht) benötigen Kontext – frag im Team nach, falls unklar.  

---

## **3. Wichtige Regeln**  

### **"Blender" übersetzen?**  

- **Normalerweise nicht!** Der Name "Blender" bleibt unverändert (wie "Toyota").  
- **Ausnahme**: Falls die Aussprache in deiner Sprache unmöglich/unpassend ist, kann ein Zusatz hinzugefügt werden (z. B. "Blender 搅拌器" auf Chinesisch).  

### **Markenbegriffe**  

Diese **dürfen nicht übersetzt** werden:  

- *Cycles*, *EEVEE* (immer großgeschrieben), *Grease Pencil*, *Freestyle*, *Line Art*.  

---

## **4. Fortgeschrittene Methoden**  

### **Offline-Übersetzung (PO-Dateien)**  

1. Lade die `.po`-Datei deiner Sprache von Weblate herunter.  
2. Bearbeite sie mit Tools wie **Poedit** oder einem Texteditor.  
3. Lade sie später wieder hoch (*Achtung: Konflikte möglich!*).  

### **Übersetzung testen**  

1. Konvertiere die `.po`-Datei ins `.mo`-Format:  

   ```bash  
   msgfmt --statistics blender-ui-ui-de.po -o blender.mo  
   ```  

2. Kopiere die `blender.mo`-Datei in den Ordner:  
   `[Blender-Verzeichnis]/locale/de/LC_MESSAGES/`.  

---

## **5. Neue Sprache hinzufügen**  

- Muss von einem **Admin** eingefügt werden.  
- Frage im [Tracker](https://developer.blender.org/maniphest/) oder im Chat nach.  

---

## **6. Tipps für Entwickler**  

### **Add-ons übersetzen**  

- Nutze das **I18n-Add-on** in Blender (*System-Kategorie*).  
- Registriere Übersetzungen im Code mit:  

  ```python  
  bpy.app.translations.register(__name__, translations_dict)  
  ```  

- Beispiel: Siehe das [render_copy_settings-Add-on](https://developer.blender.org/diffusion/BA/browse/master/render_copy_settings/).  

### **Sprache schnell wechseln**  

- Erstelle einen **Tastatur-Shortcut** in den Benutzereinstellungen:  
  - Befehl: `wm.context_toggle_enum`  
  - Attribute: `preferences.view.language`  
  - Werte: `en_US` und `de_DE` (oder deine Sprache).  

---

## **Wichtig**  

- **Lizenz**: Übersetzungen unterliegen der **GPL-Lizenz** (wie Blender selbst).  
- **RTL-Sprachen** (Arabisch, Hebräisch): Benötigen das **FriBidi-Tool** für korrekte Darstellung.  

---
**Fragen?** Besuche den [Translations-Chat](https://blender.chat/channel/translations) oder das [Forum](https://devtalk.blender.org/tag/translations).  

*(Vereinfachte Übersetzung des [Original-Leitfadens](https://developer.blender.org/docs/handbook/translating/translator_guide/)).*  

---

### **Zusammenfassung**  

- **Einfacher Einstieg**: Weblate nutzen, Team beitreten.  
- **Klare Regeln**: Markennamen nicht übersetzen, Kontext beachten.  
- **Tools**: Poedit für PO-Dateien, I18n-Add-on für Entwickler.  

Viel Erfolg beim Übersetzen! 🌍✨

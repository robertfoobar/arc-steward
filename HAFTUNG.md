# Haftungsausschluss und Nutzungshinweise

Stand: 2026-09-15

## 1. Gegenstand und Charakter

arc-steward („das Werkzeug“) ist ein quelloffenes, unentgeltlich bereitgestelltes Hilfsmittel des
im [Impressum](https://robertrieger.de/de/impressum/) genannten Anbieters. Es hält die
Architekturdokumentation eines Software-Repositorys nach arc42 oder dem Software Guidebook aktuell
und schreibt dazu Dateien in das Repository, auf dem es ausgeführt wird. Die Dokumentation wird
ganz oder teilweise durch ein großes Sprachmodell (LLM) erzeugt und ist nicht deterministisch:
Identische Eingaben können zu unterschiedlichen Ergebnissen führen. Die Ergebnisse können
unvollständig, veraltet, unzutreffend oder frei erfunden sein.

## 2. Keine Beratung, keine Prüfung, kein Nachweis

Das Werkzeug erbringt keine Architektur-, Sicherheits- oder Rechtsberatung. Die erzeugte
Dokumentation ist keine Architekturbewertung, kein Audit und kein Nachweis über den tatsächlichen
Aufbau, die Sicherheit oder die Qualität des dokumentierten Systems.

## 3. Keine Zusicherung; Hinweis zum Projektnamen

Der Projektname arc-steward ist eine Bezeichnung ohne Erklärungswert. Er enthält weder eine
Zusicherung noch eine Garantie im Sinne des § 443 BGB, insbesondere keine Zusicherung, dass die
erzeugte Dokumentation vollständig, zutreffend oder aktuell ist.

Das Werkzeug ist darauf ausgelegt, nur Dateien unter `docs/architecture/` zu ändern. Das beruht auf
Anweisungen an den ausführenden KI-Agenten und wird technisch nicht erzwungen; eine Zusicherung oder
Garantie, dass keine anderen Dateien verändert werden, wird nicht übernommen.

## 4. Eigenverantwortliche Prüfung

Jede Änderung, die das Werkzeug an einem Repository vornimmt, ist vor ihrer Übernahme durch
fachkundige Personen eigenverantwortlich zu prüfen. Das Werkzeug ist für Repositories unter
Versionskontrolle ausgelegt und sollte nur auf einem sauberen Arbeitsstand ausgeführt werden, damit
Änderungen an versionierten Dateien sichtbar und rückgängig zu machen sind. Änderungen an
ignorierten Dateien, im Verzeichnis `.git` oder außerhalb des Repositorys zeigt die
Versionskontrolle nicht an. Auf Repositories aus nicht vertrauenswürdiger Quelle ist das Werkzeug
nur in einer isolierten Umgebung auszuführen. Ob erzeugte Änderungen übernommen und wie die
Dokumentation verwendet wird, entscheidet die Nutzerin oder der Nutzer. Diese Hinweise schränken
die Haftung des Anbieters nach Abschnitt 5 nicht ein.

## 5. Haftung

(1) Die Bereitstellung erfolgt unentgeltlich und ohne Gegenleistung. Ein Entgelt, ein Abonnement,
eine Spende oder ein Sponsoring werden nicht entgegengenommen; der Zugang zum Werkzeug, zu
Aktualisierungen und zu allen Bestandteilen ist an keine Zahlung und an keine Bereitstellung
personenbezogener Daten geknüpft.

(2) Der Anbieter haftet unbeschränkt

- a) für Vorsatz und grobe Fahrlässigkeit,
- b) für Schäden aus der Verletzung des Lebens, des Körpers oder der Gesundheit, auch bei einfacher
  Fahrlässigkeit,
- c) für arglistig verschwiegene Mängel,
- d) für die Verletzung einer ausdrücklich übernommenen Garantie,
- e) nach dem Produkthaftungsgesetz.

(3) Bei einfacher Fahrlässigkeit haftet der Anbieter im Übrigen nur für die Verletzung einer
Pflicht, deren Erfüllung die ordnungsgemäße Nutzung des Werkzeugs überhaupt erst ermöglicht und auf
deren Einhaltung die Nutzerin oder der Nutzer regelmäßig vertrauen darf. In diesem Fall ist die
Haftung auf den bei Bereitstellung typischerweise vorhersehbaren Schaden begrenzt.

(4) Im Übrigen ist die Haftung für einfache Fahrlässigkeit ausgeschlossen. Weiter gehende
gesetzliche Haftungsbeschränkungen zugunsten des Anbieters, insbesondere die §§ 521, 524 des
Bürgerlichen Gesetzbuchs und § 675 Absatz 2 des Bürgerlichen Gesetzbuchs, bleiben unberührt und
werden durch diese Regelung nicht abbedungen.

(5) Die vorstehenden Beschränkungen gelten auch zugunsten von Personen, deren sich der Anbieter zur
Erfüllung bedient, und für Ansprüche aus unerlaubter Handlung.

(6) Eine Änderung der gesetzlichen Beweislast zum Nachteil der Nutzerin oder des Nutzers ist mit den
vorstehenden Regelungen nicht verbunden.

## 5a. Keine Verträge über digitale Produkte (§§ 327 ff. BGB)

Für die Nutzung des Werkzeugs wird kein Preis gezahlt; personenbezogene Daten werden vom Anbieter
nicht erhoben und nicht verarbeitet. Die §§ 327 ff. BGB sind daher nicht anwendbar (§ 327 Absatz 1
und 3, Absatz 6 Nummer 6 BGB). Eine Aktualisierungspflicht nach § 327f BGB besteht nicht. Der
Anbieter sagt keine Pflege, keine Aktualisierung und keine Verfügbarkeit zu; Angaben zu
unterstützten Versionen in `SECURITY.md` beschreiben die derzeitige Praxis und begründen keine
Verpflichtung.

## 6. Kein Vertrauenstatbestand

Ein Auskunfts-, Beratungs- oder Prüfungsvertrag kommt durch die Bereitstellung, den Download oder
die Nutzung des Werkzeugs nicht zustande. Ein solcher Vertrag bedarf einer ausdrücklichen,
gesonderten schriftlichen Vereinbarung.

## 7. Verhältnis zu den Lizenzbedingungen

Dieser Haftungsausschluss ergänzt die Haftungsregelung der MIT-Lizenz (siehe `LICENSE`) für den
Geltungsbereich des deutschen Rechts. Er beschränkt ausschließlich die Haftung des Anbieters. Er
beschränkt nicht die nach der MIT-Lizenz eingeräumten Nutzungsrechte und begründet für die unter
CC BY-SA 4.0 stehenden arc42-Kapiteltitel (siehe `NOTICE`) keine zusätzlichen oder abweichenden
Bedingungen im Sinne von Abschnitt 2(a)(5)(C) und Abschnitt 3(b)(3) der CC BY-SA 4.0.

## 8. Keine Verbindung zu Dritten

Dieses Projekt ist ein unabhängiges Vorhaben. Es steht in keiner Verbindung zu den Autoren von
arc42, zu Simon Brown, zu Anthropic, zum Mermaid-Projekt oder zu den Herstellern der in der README
genannten Agenten-Umgebungen und wird von diesen weder unterstützt noch geprüft, autorisiert oder
gesponsert.

## 9. Anwendbares Recht

Es gilt deutsches Recht unter Ausschluss des UN-Kaufrechts. Zwingende verbraucherschützende
Vorschriften des Staates, in dem eine Verbraucherin oder ein Verbraucher ihren oder seinen
gewöhnlichen Aufenthalt hat, bleiben unberührt.

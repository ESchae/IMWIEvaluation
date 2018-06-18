from string import Template

send_results_mail = Template('''
$opening 

anbei erhalten Sie die bisherigen Ergebnisse der Evaluation Ihrer Lehrveranstaltungen.

Folgende Veranstaltungen wurden evaluiert:

$evaluated_lectures

Die Ergebnisse von Evaluationen, an denen weniger als drei Personen teilgenommen haben,
werden nicht verschickt.

Falls Sie gerne noch mehr Rückmeldungen erhalten möchten, können Sie folgendes versuchen:
Antworten Sie bitte auf diese Mail und nennen Sie einen Termin, bis wann Sie die Evaluation verlängern möchten.
In diesem Fall werden nochmals automatisierte Erinnerungsmails an die Teilnehmenden verschickt.
Gleichzeitig können Sie die Evaluation erneut in Ihren Veranstaltungen ansprechen.
Sie erhalten die neuen Ergebnisse abschließend zum vereinbartem Termin.


Vielen Dank nochmals für Ihre Mithilfe!
Mit freundlichen Grüßen
IMWI Studentischer Ausschuss - Verantwortliche Elke Schächtele

''')
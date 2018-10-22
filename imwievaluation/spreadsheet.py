import gspread
from oauth2client.service_account import ServiceAccountCredentials as sa_creds


# TODO: after generating, save key + title / lecturer for later use!
class SpreadsheetHandler(object):
    """ Class to handle data transfer via Google Spreadsheets Python API.

    Uses gspread: https://github.com/burnash/gspread.

    """

    def __init__(self, creds_file='client_secret.json'):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = sa_creds.from_json_keyfile_name(creds_file, scope)
        self._client = gspread.authorize(creds)

    def generate(self, title, worksheet_title='Teilnehmer',
                 header=('Vorname', 'Nachname', 'E-Mail')):
        sh = self._client.create(title)
        # make spreadsheet accessible to everyone via url
        # also accessible for people without google account
        sh.share(None, perm_type='anyone', role='writer')
        # configure the first worksheet of the spreadsheet (index 0)
        worksheet = sh.get_worksheet(0)
        worksheet.append_row(header)
        worksheet.update_title(worksheet_title)
        # print(worksheet.row_values(1))
        # worksheet.append_row(['Vorname', 'Nachname', 'E-Mail'])
        return Spreadsheet(sh, worksheet)

    def get(self, title):
        sh = self._client.open(title)
        worksheet = sh.get_worksheet(0)
        return Spreadsheet(sh, worksheet)

    def get_by_key(self, key):
        sh = self._client.open_by_key(key)
        worksheet = sh.get_worksheet(0)
        return Spreadsheet(sh, worksheet)


class Spreadsheet(object):

    def __init__(self, sh, worksheet):
        self.sh = sh
        self.worksheet = worksheet
        self.url = 'https://docs.google.com/spreadsheets/d/%s' % sh.id

    def get_data(self):
        return self.worksheet.get_all_records()

from anki_export import ApkgReader
import pyexcel_xlsxwx

with ApkgReader('minnano.apkg') as apkg:
    pyexcel_xlsxwx.save_data('minnano.xlsx', apkg.export(), config={'format': None})
import dropbox

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)
        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to)

def main():
    access_token = 'zp_ELfFzrVAAAAAAAAAADk-KVo73eh2nM2oM7hma3aGcf9sXaT5ruGonMmyI7PHN'
    transferData = TransferData(access_token)
    file_from = 'feed_rss.xml'
    file_to = '/Aplicaciones/rssPivot/feed_rss.xml'  # The full path to upload the file to, including the file name
    # API v2
    transferData.upload_file(file_from, file_to)


import dropbox
import json
from pathlib import Path

from dropbox.files import WriteMode

from misc import Misc
from dropbox import DropboxOAuth2FlowNoRedirect
from dropbox.exceptions import ApiError

class DropboxHelper:

    def __init__(self, data_folder_path):
        self.APP_KEY = None
        self.APP_SECRET = None
        self.auth_flow = None
        self.auth_result = None
        self.data_folder_path = data_folder_path

        self._get_dropbox_credentials()
        if self.APP_KEY is not None and self.APP_SECRET is not None:
            self.auth_flow = DropboxOAuth2FlowNoRedirect(self.APP_KEY,
                                                    consumer_secret=self.APP_SECRET,
                                                    token_access_type='offline',
                                                    scope=['files.content.read', 'files.content.write', 'account_info.read'])

    def get_auth_url(self):
        if self.auth_flow is not None:
            return self.auth_flow.start()
        else:
            return None

    def authorize(self, auth_code):
        try:
            self.auth_result = self.auth_flow.finish(auth_code)
            return True
        except Exception as e:
            self.auth_result = None
            return False

    def upload_file(self, file, folder):

        upload_result = {}

        with dropbox.Dropbox(oauth2_access_token=self.auth_result.access_token,
                             oauth2_access_token_expiration=self.auth_result.expires_at,
                             oauth2_refresh_token=self.auth_result.refresh_token,
                             app_key=self.APP_KEY,
                             app_secret=self.APP_SECRET) as dbx:

            root_namespace_id = dbx.users_get_current_account().root_info.root_namespace_id
            dbx = dbx.with_path_root(dropbox.common.PathRoot.root(root_namespace_id))

            with open(file, 'rb') as f:
                try:
                    upload_path = '{}/{}'.format(Misc.DropboxUploadPath.value, folder, file.name)
                    upload_path_with_file_name = '{}/{}'.format(upload_path, file.name)

                    dbx.files_upload(f.read(), upload_path_with_file_name, mode=WriteMode('overwrite'))
                    upload_result['message'] = '{} uploaded to {}'.format(file.name, upload_path)
                    upload_result['status'] = True
                except ApiError as err:
                    upload_result['message'] = str(err)
                    upload_result['status'] = False

        return upload_result

    def upload_files(self, uploads, upload_message_event, upload_signal):

        upload_status = True
        with dropbox.Dropbox(oauth2_access_token=self.auth_result.access_token,
                             oauth2_access_token_expiration=self.auth_result.expires_at,
                             oauth2_refresh_token=self.auth_result.refresh_token,
                             app_key=self.APP_KEY,
                             app_secret=self.APP_SECRET) as dbx:

            root_namespace_id = dbx.users_get_current_account().root_info.root_namespace_id
            dbx = dbx.with_path_root(dropbox.common.PathRoot.root(root_namespace_id))

            for file in uploads.keys():
                for person in uploads[file]:

                    upload_result = {}

                    with open(file, 'rb') as f:
                        try:
                            upload_path = '{}/{}'.format(Misc.DropboxUploadPath.value, person, file.name)
                            upload_path_with_file_name = '{}/{}'.format(upload_path, file.name)

                            dbx.files_upload(f.read(), upload_path_with_file_name, mode=WriteMode('overwrite'))
                            upload_result['message'] = '{} uploaded to {}'.format(file.name, upload_path)
                            upload_result['status'] = True
                        except ApiError as err:
                            upload_result['message'] = str(err)
                            upload_result['status'] = False


                    upload_message_event(upload_result['message'])

                    if not upload_result['status']:
                        upload_status = False

                    upload_signal.emit()

        return upload_status

    def _get_dropbox_credentials(self):
        cred_file = self.data_folder_path / Misc.DropboxCredsFileName.value

        try:
            with open(cred_file) as json_file:
                creds = json.load(json_file)
                self.APP_KEY = creds['key']
                self.APP_SECRET = creds['secret']
        except FileNotFoundError:
            self.APP_KEY = None
            self.APP_SECRET = None
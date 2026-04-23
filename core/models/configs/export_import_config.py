from core.models.configs.base_config import BaseConfig


class ExportImportDialogConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.export_text = (
                "Export your password metadata to a JSON file. "
                "This file contains only public keys, descriptions and lengths - "
                "no passwords or secret phrases are exported."
            )
        self.import_text = (
                "Import password metadata from a JSON file. "
                "The file must contain valid password metadata in the same format as export. "
                "Existing passwords with the same public keys will NOT be overwritten."
            )

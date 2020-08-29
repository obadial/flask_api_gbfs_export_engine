from gbfs.controllers.json_export import json_export


def export_data(data):
    json_export(data)
    print("New JSON export available")

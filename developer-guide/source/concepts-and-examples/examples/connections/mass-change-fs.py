import dataiku


def mass_change_connection(project, origin_conn, dest_conn):
    """Mass change dataset connections in a project (filesystem connections only)"""

    for dataset in project.list_datasets(as_type='objects'):
        ds_settings = dataset.get_settings()
        if ds_settings.type == 'Filesystem':
            params = ds_settings.get_raw().get('params')
            if params.get('connection') == origin_conn:
                params['connection'] = dest_conn
                ds_settings.save()

client = dataiku.api_client()
project = client.get_default_project()
mass_change_connection(project, "FSCONN_SOURCE", "FSCONN_DEST")

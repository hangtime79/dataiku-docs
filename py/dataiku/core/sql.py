from platform_exec import open_dku_stream
import pandas as pd


class SQLExecutor:
    def __init__(self, connection):
        self.connection = connection

    def _stream(self, query):
        args = ['sql', self.connection, '-e', '%s ' % query]
        return open_dku_stream(args)

    def exec_query(self, query):
        with self._stream(query) as dku_output:
            return pd.read_table(dku_output,
                                 sep='\t',
                                 doublequote=True,
                                 quotechar='"')
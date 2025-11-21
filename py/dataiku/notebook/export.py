"""
Adds a export dataset button in ipython notebook output.
"""


import weakref
import os
import sys
import uuid
import requests
import struct
import Queue
import threading
from IPython.core import display
import pandas as pd


class CSVGenerator(threading.Thread):
    
    def __init__(self, df):
        self.df = df
        self.end_mark = []
        self.data = []
        self.force_stop = False
        self.queue = Queue.Queue(100)
        threading.Thread.__init__(self)
        self.start()
        
    # Run thread
    def run(self):
        try:
            self.df.to_csv(self, header=False, index=False, chunksize=100)
        except:
            # This is expected to happen!
            pass
        self.write(self.end_mark)
        
    # Write from Pandas to_csv()
    def write(self, data):
        if self.force_stop:
            # Only way I found to stop the CSV writer...
            raise IOError("CSVGenerator has been shutdown")
        else:
            self.queue.put(data)
        
    # Necessary to let Pandas think we're a stream
    def read(self):
        pass
    
    # Return a generator
    def gen(self):
        while not self.force_stop:
            item = self.queue.get()
            if item is self.end_mark:
                break
            yield item
            
    # Throw an IOError to Pandas to_csv() (raised in write())
    # Implicitly kill the thread
    def shutdown(self):
        self.force_stop = True
        try:
            while True:
                self.queue.get(False)
        except:
            self.queue.put(self.end_mark)
        

class IPythonExporter:
    
    _internal_map = dict()
    
    @staticmethod
    def collect_collected():
        keys_to_remove = []
        for k, v in IPythonExporter._internal_map.iteritems():
            if v() is None:
                keys_to_remove.append(k)
        for k in keys_to_remove:
            del IPythonExporter._internal_map[k]
    
    @staticmethod
    def register_dataframe(df):
        
        IPythonExporter.collect_collected()
        
        for k, v in IPythonExporter._internal_map.iteritems():
            if v() is df:
                return k
        
        # Assuming perfect uniqueness
        new_id = str(uuid.uuid4())
        IPythonExporter._internal_map[new_id] = weakref.ref(df)
        return new_id
    
    @staticmethod
    def generate_export_button(df):
        id = IPythonExporter.register_dataframe(df)
        return """
            <button style="display:none" 
            class="btn ipython-export-btn" 
            """+("id=\"btn-df-%s\""%id)+""" 
            onclick="_export_df("""+("'%s'"%id)+""")">
                Export dataframe
            </button>
            
            <script>
                
                function _check_export_df_possible(dfid,yes_fn,no_fn) {
                    console.log('Checking dataframe exportability...')
                    if(!IPython || !IPython.notebook || !IPython.notebook.kernel || !IPython.notebook.kernel.running) {
                        console.log('Export is not possible (IPython kernel is not available)')
                        if(no_fn) {
                            no_fn();
                        }
                    } else {
                        var pythonCode = 'from dataiku.notebook.export import IPythonExporter;IPythonExporter._check_export_stdout("'+dfid+'")';
                        IPython.notebook.kernel.execute(pythonCode,{iopub: {output: function(resp) {
                            var size = /^([0-9]+)x([0-9]+)$/.exec(resp.content.data)
                            if(!size) {
                                console.log('Export is not possible (dataframe is not in-memory anymore)')
                                if(no_fn) {
                                    no_fn();
                                }
                            } else {
                                console.log('Export is possible')
                                if(yes_fn) {
                                    yes_fn(1*size[1],1*size[2]);
                                }
                            }
                        }}});
                    }
                }
            
                function _export_df(dfid) {
                    
                    var btn = $('#btn-df-'+dfid);
                    var btns = $('.ipython-export-btn');
                    
                    _check_export_df_possible(dfid,function() {
                        
                        window.parent.openExportModalFromIPython('Pandas dataframe',function(data) {
                            btns.prop('disabled',true);
                            btn.text('Exporting...');
                            IPython.notebook.kernel.execute('from dataiku.notebook.export import IPythonExporter;IPythonExporter._run_export("'+dfid+'","'+data.exportId+'")',{iopub:{output: function(resp) {
                                _check_export_df_possible(dfid,function(rows, cols) {
                                    $('#btn-df-'+dfid)
                                        .css('display','inline-block')
                                        .text('Export this dataframe ('+rows+' rows, '+cols+' cols)')
                                        .prop('disabled',false);
                                },function() {
                                    $('#btn-df-'+dfid).css('display','none');
                                });
                            }}});
                        });
                    
                    }, function(){
                            alert('Unable to export : the Dataframe object is not loaded in memory');
                            btn.css('display','none');
                    });
                    
                }
                
                (function(dfid) {
                
                    var retryCount = 10;
                
                    function is_valid_websock(s) {
                        return s && s.readyState==1;
                    }
                
                    function check_conn() {
                        
                        if(!IPython || !IPython.notebook) {
                            // Don't even try to go further
                            return;
                        }
                        
                        // Check if IPython is ready
                        if(IPython.notebook.kernel 
                        && IPython.notebook.kernel.running
                        && is_valid_websock(IPython.notebook.kernel.shell_channel)
                        && is_valid_websock(IPython.notebook.kernel.stdin_channel)
                        && is_valid_websock(IPython.notebook.kernel.iopub_channel)
                        ) {
                            
                            _check_export_df_possible(dfid,function(rows, cols) {
                                $('#btn-df-'+dfid).css('display','inline-block');
                                $('#btn-df-'+dfid).text('Export this dataframe ('+rows+' rows, '+cols+' cols)');
                            });
                            
                        } else {
                            
                            // Retry later
                            
                            if(retryCount>0) {
                                setTimeout(check_conn,500);
                                retryCount--;
                            }
                            
                        }
                    };
                    
                    setTimeout(check_conn,100);
                    
                })("""+"\"%s\""%id+""");
                
            </script>
            
        """
    
    @staticmethod
    def export_dataframe(df):
        html = IPythonExporter.generate_export_button(df)
        display.display_html(html, raw=True)
    
    @staticmethod
    def encode_dataframe(df, csv):
        def writeInt(n, ba):
            ba += struct.pack('!i', n)
        def writeStr(s, ba):
            s = ("%s" % s).encode('utf-8')
            writeInt(len(s), ba)
            if len(s) > 0:
                ba += struct.pack('!%ds' % len(s), s)
        buffer = bytearray()
        writeInt(len(df.columns), buffer)
        for c in df.columns:
            writeStr(str(c), buffer)
            writeStr('string', buffer)
        writeInt(len(df.index), buffer)
        yield buffer
        buffer = bytearray()
        for chunk in csv.gen():
            buffer += chunk
            if len(buffer) > 200000:
                yield buffer
                buffer = bytearray()
        if len(buffer) > 0:
            yield buffer
    
    @staticmethod
    def _check_export(df_id):
        IPythonExporter.collect_collected()
        if IPythonExporter._internal_map.has_key(df_id):
            df = IPythonExporter._internal_map[df_id]();
            if df is not None:
                return df.shape
            else:
                return False
        else:
            return False
        
    @staticmethod
    def _check_export_stdout(df_id):
        size = IPythonExporter._check_export(df_id)
        sys.stdout.write('%dx%d'%size if size else 'ERROR')

    @staticmethod
    def _run_export(df_id, export_id):
        backend_port = os.getenv('DKU_BACKEND_PORT')
        if IPythonExporter._check_export(df_id):
            df = IPythonExporter._internal_map[df_id]()
            csv = CSVGenerator(df)
            try:
                requests.put("http://127.0.0.1:%s/dip/api/ipython/bind-export?%s"%(backend_port,export_id),data=IPythonExporter.encode_dataframe(df,csv))
                sys.stdout.write('OK')
            except:
                sys.stdout.write('ERROR')
            finally:
                csv.shutdown()
                
        else:
            sys.stdout.write('ERROR')
        
orig_to_html = pd.DataFrame._repr_html_
def to_html_with_export(df, *args, **kwargs):
    global orig_to_html
    html = IPythonExporter.generate_export_button(df)
    html += orig_to_html(df,*args,**kwargs)
    return html


SETUP = False

def setup():
    global SETUP
    if not SETUP:
        pd.DataFrame._repr_html_ = to_html_with_export
        SETUP = True

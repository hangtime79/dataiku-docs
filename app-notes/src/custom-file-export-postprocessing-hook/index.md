# HOWTO: Make a custom File export postprocessing hook

Write code like:

```
package mypackage;
import java.io.File;
import com.dataiku.dip.export.hooks.FileExportPostprocessingHook;
import com.dataiku.dip.export.input.ExportInput;
import com.dataiku.dip.graphicsexport.model.EnrichedExport;
import com.dataiku.dip.security.AuthCtx;
import com.dataiku.dip.utils.DKULogger;
import com.dataiku.dip.utils.JSON;

public class MyHook extends FileExportPostprocessingHook {

    @Override
    public void onPostDataExportToFile(AuthCtx authCtx, File file, ExportInput input) {
        logger.infoV("onPostDataExportToFile: authCtx=%s file=%s (s=%s) input=%s", 
                              authCtx, file, file.length(), JSON.json(input));
    }

    @Override
    public void onPostGraphicExport(AuthCtx authCtx, File file, EnrichedExport exportDefinition) {
        logger.infoV("onPostGraphicExport authCtx=%s file=%s (s=%s) exmlrt=%s",
                              authCtx, file, file.length(), JSON.json(exportDefinition));
    }

    @Override
    public void onPostModelDocumentationExport(AuthCtx authCtx, File file, FullModelId modelId) {
        logger.infoVonPostModelDocumentationExport authCtx=%s file=%s (s=%s) modelId=%s",
                              authCtx, file, file.length(), JSON.json(modelId));
    }

    private static DKULogger logger = DKULogger.getLogger("myhook");
}
```

Compile this class, linking against:

* `INSTALLDIR/lib/ivy/common-run/*`
* `INSTALLDIR/lib/ivy/backend-run/*`
* `INSTALLDIR/dist/*`

Package it to a jar. 

For example you can use this build.xml:

```
<project name="myhook" default="jar">
    <property name="build.dir" value="build" />
    <property name="dist.dir" value="dist" />
    <property environment="env"/>

    <target name="clean">
        <delete dir="${dist.dir}" />
        <delete dir="${build.dir}" />
    </target>

    <target name="jar">
        <path id="lib.path.id">
            <fileset dir="${env.INSTALLDIR}/lib/ivy/backend-run" />
            <fileset dir="${env.INSTALLDIR}/lib/ivy/common-run" />
            <fileset dir="${env.INSTALLDIR}/dist" includes="*.jar" />
        </path>
        <mkdir dir="${build.dir}" />
        <mkdir dir="${dist.dir}" />
        <javac debug="true" destdir="${build.dir}" classpathref="lib.path.id" encoding="utf-8" includeantruntime="false">
            <compilerarg value="-Xlint:all" />
            <src>
                <pathelement location="src" />
            </src>
        </javac>
        <jar destfile="${dist.dir}/myexporthook.jar" basedir="${build.dir}" />
    </target>
</project>
```

Place the resulting jar in `DATADIR/java`

Edit config/dip.properties, and add:

```
dku.exports.disableDirectDownload=true
dku.exports.fileExportPostprocessingHookClass=mypackage.MyHook
```

Restart DSS

Save and test. In case of errors during test, errors can be found in `DATADIR/run/backend.log`

*Warning*: These instructions are provided as-is, as custom file export postprocessing hook is an experimental advanced option. The API may change in a future DSS release.
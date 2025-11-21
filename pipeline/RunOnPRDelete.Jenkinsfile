// The variable SOURCE_PROJECT_NAME is passed by the parent multi-branch pipeline which is using https://plugins.jenkins.io/multibranch-action-triggers/ plugin
// The variable SOURCE_PROJECT_NAME is equal to the branch name which is like PR-XXX
def FOLDER_FOR_BUILT_DSSDOC = "/data/www/dss-doc-staging.dku.sh/htdocs"

pipeline {
    agent {
        label "dss-doc-staging"
    }
    stages {
        stage("Remove folder with the dss-doc") {
            steps {
                script {
                    if (SOURCE_PROJECT_NAME.startsWith("PR-") && !SOURCE_PROJECT_NAME.contains("../")) {
                        def DSS_DOC_FOLDER = "${FOLDER_FOR_BUILT_DSSDOC}/$SOURCE_PROJECT_NAME/"
                        sh "[ -d '$DSS_DOC_FOLDER' ] && rm -rf $DSS_DOC_FOLDER"
                    }
                }
            }
        }
    }
}
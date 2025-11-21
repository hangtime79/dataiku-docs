Dynamic namespace management
#############################

In Kubernetes, the namespace is the unit for access control and resources control.

DSS can either use a single namespace, multiple static namespaces, or multiple dynamic namespaces. In the latter case, DSS will itself create namespaces dynamically depending on what is requested, which allows for isolation of security and resources.

For example, you may want to:

* Create one namespace per user, in order to put limits on what the user can do
* Create one namespace per project
* Create one namespace per team

DSS leverages variables expansion for this. For example, to have one namespace per user, you can configure DSS to execute in namespace ``ns-${dssUserLogin}``. If user ``user1`` runs something, DSS will expand this and run in namespace ``ns-user1``. If this namespace does not exist, DSS can create it on the fly (assuming DSS has been granted sufficient rights)

Namespace policies
====================

DSS can automatically apply policies to the dynamic namespaces, notably resource quotas (in order to limit the total amount of computation/memory available to a namespace/user/team/project/...) and limit ranges (in order to set default resource control for computations running in the dynamic namespace).

In order to apply a namespace policy, go to Administration > Settings > Containerized execution, and add a namespace policy. Select a pattern (regular expression) for which namespaces it will apply to, and to which clusters it will apply (including saying if it should apply to the default unmanaged cluster).

Policies are applied each time DSS creates a namespace and can be applied manually by clicking the button.

Policy elements must be YAML representations of Kubernetes quota-level objects, such as ``ResourceQuota`` or ``LimitRange``.

For more details, please see https://kubernetes.io/docs/concepts/policy/ 
# Security contexts in K8S clusters

Much can be read on security contexts on pods. Best start with [the official spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.26/#podsecuritycontext-v1-core)

While not restricted to Openshift clusters, experience shows that non-empty security contexts are mostly found when dealing with Openshift cluster, probably because Openshift clusters have [security context constraints](https://docs.redhat.com/en/documentation/openshift_container_platform/3.11/html-single/architecture/index?extIdCarryOver=true&sc_cid=701f2000001Css5AAC#security-context-constraints) and they are activated OOTB.

## Using DSS with runAsNonRoot

Enable the `runAsNonRoot` feature flag in dip.properties. That's all. Then DSS adds a security context with ``runAsNonRoot: true`` in its pods/deployments/replica sets.

## Using DSS with runAsUser

A typical Openshift cluster will use a security context constraint with `MustRunAsRange` , which implies that each pod will be run by its kubelet as a user with a UID in that range (probably taken randomly). The consequence is that any code in the container that relies on the current user to be `dataiku`, or on permissions being set on files/folders in the pod, will face "permission denied" or "ENOACCESS" problems. A countermeasure is to run as a user with a fixed UID in that range, ie. to not let the kubelet decide.

In DSS, the setup is:

- add a line in dip.properties with `dku.container.dataiku.uid=the_uid_you_want_to_use`  (otherwise DSS uses UID `500`)
- add a line in dip.properties to activate the `podRunAsUid` feature flag
- rebuild all the container images (container-exec, spark, api-deployer, code env images, code studio templates)

The reason you need to rebuild images is that the `dataiku` user is created in the images with the `dku.container.dataiku.uid` UID, and the folders/files permissions set for this `dataiku` user.

## Using DSS with readOnlyRootFilesystem

On a pristine DSS, containerized operations will fail if the cluster imposes a read-only root filesystem in the pod (via a security context constraint for example). Most containerized operations will need a local storage of sorts, usually the working directory (which is `/home/dataiku`), or a tmp for various reasons, and the read-only root filesystem security constraint forbids that.

Support for `readOnlyRootFilesystem` has been added in 14.2.0. No image rebuild is needed. It works by adding an volume in the pod which is mounted as read-write for `/home/dataiku`. The contents of `/home/dataiku` that are present on the container image are copied to the mounted `/home/dataiku` with an init container. Another volume for `/tmp` is also mounted as read-write.

### Python recipe/notebooks, webapps,... CDE and API deployments
To enable to run with a read-only root filesystem in the pod, you need to add an entry `readOnlyRootFilesystem -> true` in the "Custom properties" of the container configuration(s) in Administration > Settings > Containerized execution. 

Additional optional properties:

- `writableHomeVolumeDesc` : controls the volume spec for `/home/dataiku`. Will be an `emptyDir` by default, without specification of the `medium`. For example you can request an emptyDir in memory with a 8GB max size with a value `emptyDir:\n  medium: Memory\n  sizeLimit: 8Gi` (note the indenting)
- `writableHomeVolumeSizeLimit` : if `writableHomeVolumeDesc` isn't set, the max size of the `emptyDir`
- `writableTmpVolumeDesc` : controls the volume spec for `/tmp`. Will be an `emptyDir` by default, without specification of the `medium`
- `writableTmpVolumeSizeLimit` if `writableTmpVolumeDesc` isn't set, the max size of the `emptyDir`

CDE and API deployments use the same custom properties (in the infrastructure settings for API deployments).

### Spark

To enable spark jobs to run with the `readOnlyRootFilesystem` option, you need to make the executor pods set themselves up with read-write volumes. This can be done with a pod template, or with properties (that Spark will write into the template). The target is to have in the pod

- a writable `/home/dataiku`
- a writable `/tmp`

There's a pod template yaml bundled in the DSS install, so you can reference it with a spark property `spark.kubernetes.executor.podTemplateFile -> ${dku.install.dir}/resources/spark/spark-readOnlyRootFilesystem.template.yaml` . The same can be achieved with this set of properties (see [the Spark doc](https://spark.apache.org/docs/latest/running-on-kubernetes.html#using-kubernetes-volumes) ). For example, you can add the spark properties:

- `spark.kubernetes.local.dirs.tmpfs -> true`
- `spark.kubernetes.driver.volumes.emptyDir.vol-tmp.mount.path -> /tmp`
- `spark.kubernetes.driver.volumes.emptyDir.vol-tmp.mount.readOnly -> false`
- `spark.kubernetes.driver.volumes.emptyDir.vol-tmp.options.sizeLimit -> 1Gi`
- `spark.kubernetes.driver.volumes.emptyDir.vol-home.mount.path -> /home/dataiku`
- `spark.kubernetes.driver.volumes.emptyDir.vol-home.mount.readOnly -> false`
- `spark.kubernetes.driver.volumes.emptyDir.vol-home.options.sizeLimit -> 1Gi`

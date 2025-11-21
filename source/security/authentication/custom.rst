Custom Authenticator and/or User Supplier
################################################

While DSS provides support for various authenticators and user suppliers, there may be cases where you require a more customized solution to meet your specific needs. DSS offers the flexibility to extend its capabilities by implementing your own custom authenticators and user suppliers.

Custom authenticators and user suppliers are Java components that can be packaged as DSS plugins. This allows for easy installation on multiple instances and sharing through the DSS plugin market.

To create a custom authenticator and/or user supplier, you can either create a new plugin or extend an existing one. You have the option to create a component that serves as:

- Authenticator: Supports user authentication only.
- User supplier: Provides user information to DSS only.
- Authenticator and User supplier: Supports both user authentication and user information supply to DSS.

Please note that DSS currently does not support multiple custom user suppliers.

Once you have created the component that suits your requirements, you will need to define a new Java class within your plugin. The Java interface Javadoc should provide sufficient guidance from this point onward.


Packaging the plugin
********************

Since the plugin components are written in Java, the source code needs to be compiled into a .jar library. To accomplish this, you will need Apache Ant. After compilation, the DSS backend must be restarted.

To package the plugin, follow these steps:

1. Navigate to the plugin directory where the `build.xml` file is located (e.g. `$DSS_HOME/plugins/`).
2. Execute the `ant jar` command to create a `.jar` file in the `java-lib` directory.

Once the plugin is packaged, it can be shared with others, and you won't need to rebuild the `.jar` file. It will be bundled within the plugin itself.


DSS security settings
*********************

In DSS, go to `Settings` > `Security & Audit` > `User login & provisioning` > `Custom authenticator and supplier` section and perform the following steps:

- Enable the Custom authenticator and supplier feature.
- Specify the full class name of your custom authenticator in the `Custom user authenticator full class name` field, for example, `com.example.MyCustomAuthenticator`.
- Specify the full class name of your custom user supplier in the `Custom user supplier full class name` field, for example, `com.example.MyCustomUserSupplier`.
- Restart DSS for the changes to take effect.
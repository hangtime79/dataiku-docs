# Howto: Enable hashed API keys

  * [1. Overview](#1-overview)
  * [2. Availability and limitations](#2-availability-and-limitations)
  * [3. Enable](#3-enable)

<a name="1-overview"></a>

## 1. Overview

Starting with version 13.1, DSS can hash global, personal and project API keys. This behavior is enabled by default on newly installed instances, but is disabled on upgraded instances.

This note describes how to enable this feature.

<a name="2-availability-and-limitations"></a>

## 2. Availability and limitations

### 2.1. Availability

This feature is available for all node types.

### 2.2. Limitations

After activation, users will no longer be able to retrieve existing API keys from the user interface nor the public API.

<a name="3-enable"></a>

## 3. Enable

* Log in via SSH to the DSS VM and sudo as the unix dataiku user
* Stop DSS
* Run the activation command
```bash
./bin/dku enable-hashed-api-keys
# for Govern: ./bin/dkugovern enable-hashed-api-keys
```
* Start DSS

That command will enable the feature and hash all existing API keys.

> Note: The command does nothing if the feature is already enabled.


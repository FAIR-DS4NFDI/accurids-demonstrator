# ACCURIDS Demonstrator

## Overview 

We implemented a use case scenario about clinical trials with a setup of two ACCURIDS instances with corresponding configuration, customization and user groups.

We realize data exchange between the Accurids instances by the FAIR Dataspace. 

Two services (consumer and provider) based on the Eclipse Dataspace Components Connector enable the connection between the Accurids instances over the FAIR Dataspace using the Internation Dataspace (IDS) protocol.

A Python script manages the communication between consumer and provider service. The script exeutes the data transfer through the HTTP data plane of the Eclipse Connector in order to synchronize datsets between the two Accurids instances.

## Pharma Instance

Available at https://pharma.accurids.com as a demo instance to capture the basic clinical trial information and requirements for collecting human biosample data in trials performed at clinical research institutions such as a university hospital.

## Hospital Instance

Available a https://hospital.accurids.com as a demo instance to master patient information and collection of bio samples as part of the clinical trial perform for the sponsoring pharma company.

## Consumer and Producer

The consumer and producer are based on a Eclipse Connector launcher. The setup is similar to the Eclipse Connector [Samples](https://github.com/eclipse-edc/Samples).

You can copy the `build.gradle.kts` or into the launchers folder of the [Eclipse Connector code repository](https://github.com/eclipse-edc/Connector/tree/main/launchers) and execute `./gradlew clean launchers:accurids:build` to build the `accurids-connector.jar`.

In a command prompt, start the provider and the consumer:

Consumer: 

`java -Dedc.keystore=./certs/cert.pfx -Dedc.keystore.password=123456 -Dedc.fs.config=./config/consumer-configuration.properties -jar accurids-connector.jar`

Provider:

`java -Dedc.keystore=./certs/cert.pfx -Dedc.keystore.password=123456 -Dedc.fs.config=./config/provider-configuration.properties -jar accurids-connector.jar`

## Demo Script

### Preparation

Prepare a virtual environment

`python -m venv venv`

Activate the virtual environment

`.\venv\Scripts\activate` (in Windows)

Install dependencies

`pip install requests colorlog jsonpath_ng rich`

### Execution

`python .\edc_demo.py`

The script expects to find the API keys for the two Accurids instances in two environment variables: `API_KEY_PHARMA` and `API_KEY_HOSPITAL`.

Once the script is running, it first prepares the dataspace i.e., creating assets, roles, policies, and afterwards it continuously looks for changes in monitored datasets in Accurids. 
As soon as a change is detected, the script executes a synchronization between the Accurids instances using the IDS prototcol.

### Docker Container

The Demonstrator setup of `Consumer`, `Provider` and the Python script is available as a Docker container in the `Packages` section of this code repository: [https://github.com/FAIR-DS4NFDI/accurids-demonstrator/pkgs/container/accurids-demonstrator](https://github.com/FAIR-DS4NFDI/accurids-demonstrator/pkgs/container/accurids-demonstrator).

You can execute the container with following command:

`docker run --env API_KEY_PHARMA=<key1> --env API_KEY_HOSPITAL=<key2> accurids-demonstrator`

Replace `<key1>` and `<key2>` with the API keys of the Pharma instance and the Hospital instance.

#### Example log from an execution

```
2024-12-03T12:10:58Z root         DEBUG    API KEY 1: API-Key-From-Hospital
2024-12-03T12:10:58Z root         DEBUG    API KEY 2: API-Key-From-Pharma

2024-12-03T12:10:58Z root         INFO     1. 1.  CREATE ASSET SOURCE HOSPITAL HUMAN BIOSAMPLE
2024-12-03T12:10:58Z root         INFO     1. 2.  CREATE ASSET TARGET FILE HOSPITAL HUMAN BIOSAMPLE
2024-12-03T12:10:59Z root         INFO     1. 3.  CREATE ASSET TARGET GRAPHQL HOSPITAL
2024-12-03T12:10:59Z root         INFO     1. 4.  CREATE ASSET SOURCE HOSPITAL PATIENT COLLABORATION
2024-12-03T12:10:59Z root         INFO     1. 5.  CREATE ASSET TARGET FILE HOSPITAL PATIENT COLLABORATION
2024-12-03T12:10:59Z root         INFO     1. 6.  CREATE ASSET SOURCE PHARMA REFERENCE DATA
2024-12-03T12:10:59Z root         INFO     1. 7.  CREATE ASSET TARGET FILE PHARMA REFERENCE DATA
2024-12-03T12:10:59Z root         INFO     1. 8.  CREATE ASSET TARGET GRAPHQL PHARMA
2024-12-03T12:10:59Z root         INFO     1. 9.  CREATE ASSET SOURCE PHARMA SHAPES
2024-12-03T12:10:59Z root         INFO     1. 10. CREATE ASSET TARGET FILE PHARMA SHAPES
2024-12-03T12:10:59Z root         INFO     1. 11. CREATE ASSET SOURCE PHARMA TRIAL
2024-12-03T12:10:59Z root         INFO     1. 12. CREATE ASSET TARGET FILE PHARMA TRIAL
2024-12-03T12:10:59Z root         INFO     2. CREATE POLICY
2024-12-03T12:10:59Z root         INFO     3. CREATE CONTRACT
2024-12-03T12:10:59Z root         INFO     
2024-12-03T12:10:59Z root         INFO     UPDATE CYCLE 00001
2024-12-03T12:10:59Z root         INFO     
2024-12-03T12:10:59Z root         INFO     PHARMA REFERENCE DATA
2024-12-03T12:10:59Z root         INFO     
2024-12-03T12:10:59Z root         INFO       Download Pharma Reference Data
2024-12-03T12:10:59Z root         INFO     
2024-12-03T12:10:59Z root         INFO         4. FETCH CATALOG
2024-12-03T12:10:59Z root         INFO         5. NEGOTIATE CONTRACT SOURCE
2024-12-03T12:10:59Z root         INFO         6. GET AGREEMENT ID SOURCE
2024-12-03T12:10:59Z root         INFO             Agreement ID: None
2024-12-03T12:10:59Z root         INFO               no agreement identifier found, poll again in a second (1)
2024-12-03T12:11:00Z root         INFO             Agreement ID: None
2024-12-03T12:11:00Z root         INFO               no agreement identifier found, poll again in a second (2)
2024-12-03T12:11:01Z root         INFO             Agreement ID: f2f1d3d0-2316-4f7e-aacc-43c681f9ef33
2024-12-03T12:11:01Z root         INFO     
2024-12-03T12:11:01Z root         INFO         7. START TRANSFER SOURCE
2024-12-03T12:11:01Z root         INFO             Transfer ID: ffb178f3-d10a-4283-afaf-7b40a867d195
2024-12-03T12:11:01Z root         INFO     
2024-12-03T12:11:01Z root         INFO         8. GET ENDPOINT DATA REFERENCE SOURCE
2024-12-03T12:11:01Z root         INFO             Endpoint: None Token: None...
2024-12-03T12:11:01Z root         INFO               no data endpoint found, poll again in a second (1)
2024-12-03T12:11:02Z root         INFO             Endpoint: None Token: None...
2024-12-03T12:11:02Z root         INFO               no data endpoint found, poll again in a second (2)
2024-12-03T12:11:03Z root         INFO             Endpoint: http://localhost:19291/public Token: eyJraWQi...
2024-12-03T12:11:03Z root         INFO     
2024-12-03T12:11:03Z root         INFO         9. GET THE DATA FROM ACCURIDS API PHARMA
2024-12-03T12:11:05Z root         INFO             Download done.
2024-12-03T12:11:05Z root         INFO           This is the first download.
2024-12-03T12:11:05Z root         INFO     
2024-12-03T12:11:05Z root         INFO       Upload Pharma Reference Data
2024-12-03T12:11:05Z root         INFO     
2024-12-03T12:11:05Z root         INFO         10. FETCH CATALOG TARGET FILE
2024-12-03T12:11:05Z root         INFO     
2024-12-03T12:11:05Z root         INFO         11. NEGOTIATE CONTRACT TARGET FILE
2024-12-03T12:11:05Z root         INFO             Negotiation ID: 2c37fed6-962e-46c7-8633-afd54e619593
2024-12-03T12:11:05Z root         INFO     
2024-12-03T12:11:05Z root         INFO         12. GET AGREEMENT ID TARGET FILE
2024-12-03T12:11:05Z root         INFO             Agreement ID: None
2024-12-03T12:11:05Z root         INFO               no agreement identifier found, poll again in a second (1)
2024-12-03T12:11:06Z root         INFO             Agreement ID: efd69358-d6c7-4673-b473-2afef2bf2c2e
2024-12-03T12:11:06Z root         INFO     
2024-12-03T12:11:06Z root         INFO         13. START TRANSFER TARGET FILE
2024-12-03T12:11:06Z root         INFO             Transfer ID: 0f417394-21aa-44b7-a16a-5ed26d33e44b
2024-12-03T12:11:06Z root         INFO     
2024-12-03T12:11:06Z root         INFO         14. GET ENDPOINT DATA REFERENCE TARGET FILE
2024-12-03T12:11:06Z root         INFO             Endpoint: None Token: None...
2024-12-03T12:11:06Z root         INFO               no data endpoint found, poll again in a second (1)
2024-12-03T12:11:07Z root         INFO             Endpoint: http://localhost:19291/public Token: eyJraWQi...
2024-12-03T12:11:07Z root         INFO     
2024-12-03T12:11:07Z root         INFO         15. PUSH THE DATA TO ACCURIDS API HOSPITAL FILE UPLOAD
2024-12-03T12:11:07Z root         DEBUG            File upload complete.
2024-12-03T12:11:07Z root         INFO     
2024-12-03T12:11:07Z root         INFO         16. FETCH CATALOG TARGET GRAPHQL
2024-12-03T12:11:07Z root         INFO     
2024-12-03T12:11:07Z root         INFO         17. NEGOTIATE CONTRACT TARGET GRAPHQL
2024-12-03T12:11:07Z root         INFO             Negotiation ID: c354e12c-768d-4ba7-a319-b4b0d8ea4163
2024-12-03T12:11:07Z root         INFO     
2024-12-03T12:11:07Z root         INFO         18. GET AGREEMENT ID TARGET GRAPHQL
2024-12-03T12:11:07Z root         INFO             Agreement ID: None
2024-12-03T12:11:08Z root         INFO     
2024-12-03T12:11:08Z root         INFO         19. START TRANSFER TARGET GRAPHQL
2024-12-03T12:11:08Z root         INFO     
2024-12-03T12:11:08Z root         INFO         20. GET ENDPOINT DATA REFERENCE TARGET GRAPHQL
2024-12-03T12:11:08Z root         INFO             Endpoint: None Token: None...
2024-12-03T12:11:08Z root         INFO               no data endpoint found, poll again in a second (1)
2024-12-03T12:11:09Z root         INFO             Endpoint: http://localhost:19291/public Token: eyJraWQi...
2024-12-03T12:11:09Z root         INFO     
2024-12-03T12:11:09Z root         INFO         21. PUSH THE DATA TO ACCURIDS API HOSPITAL DATASET UPDATE
2024-12-03T12:11:09Z root         DEBUG          Updating the dataset failed. Trying to create a new one.
2024-12-03T12:11:09Z root         INFO             Dataset upload done.
2024-12-03T12:11:09Z root         INFO     
2024-12-03T12:11:09Z root         INFO     PHARMA SHAPES
2024-12-03T12:11:09Z root         INFO     
2024-12-03T12:11:09Z root         INFO       Download Pharma Shapes
2024-12-03T12:11:09Z root         INFO     
2024-12-03T12:11:09Z root         INFO         4. FETCH CATALOG
2024-12-03T12:11:09Z root         INFO     
2024-12-03T12:11:09Z root         INFO         5. NEGOTIATE CONTRACT SOURCE
2024-12-03T12:11:09Z root         INFO     
2024-12-03T12:11:09Z root         INFO         6. GET AGREEMENT ID SOURCE
2024-12-03T12:11:09Z root         INFO             Agreement ID: None
2024-12-03T12:11:09Z root         INFO               no agreement identifier found, poll again in a second (1)
2024-12-03T12:11:10Z root         INFO             Agreement ID: None
2024-12-03T12:11:10Z root         INFO               no agreement identifier found, poll again in a second (2)
2024-12-03T12:11:11Z root         INFO             Agreement ID: 3094bc3e-c728-4b09-a6b0-c203bf8f78cf
2024-12-03T12:11:11Z root         INFO     
2024-12-03T12:11:11Z root         INFO         7. START TRANSFER SOURCE
2024-12-03T12:11:12Z root         INFO             Transfer ID: 6365467e-4299-4f8a-96df-149a260abf5e
2024-12-03T12:11:12Z root         INFO     
2024-12-03T12:11:12Z root         INFO         8. GET ENDPOINT DATA REFERENCE SOURCE
2024-12-03T12:11:12Z root         INFO             Endpoint: None Token: None...
2024-12-03T12:11:12Z root         INFO               no data endpoint found, poll again in a second (1)
2024-12-03T12:11:13Z root         INFO             Endpoint: None Token: None...
2024-12-03T12:11:13Z root         INFO               no data endpoint found, poll again in a second (2)
2024-12-03T12:11:14Z root         INFO     
2024-12-03T12:11:14Z root         INFO         9. GET THE DATA FROM ACCURIDS API PHARMA
2024-12-03T12:11:14Z root         INFO             Download done.
2024-12-03T12:11:14Z root         INFO           This is the first download.
2024-12-03T12:11:14Z root         INFO     
2024-12-03T12:11:14Z root         INFO       Upload Pharma Shapes
2024-12-03T12:11:14Z root         INFO     
2024-12-03T12:11:14Z root         INFO         10. FETCH CATALOG TARGET FILE
2024-12-03T12:11:14Z root         INFO     
2024-12-03T12:11:14Z root         INFO         11. NEGOTIATE CONTRACT TARGET FILE
2024-12-03T12:11:14Z root         INFO             Negotiation ID: 0739cc2d-cfdd-4945-af74-346226fab590
2024-12-03T12:11:14Z root         INFO     
2024-12-03T12:11:14Z root         INFO         12. GET AGREEMENT ID TARGET FILE
2024-12-03T12:11:14Z root         INFO             Agreement ID: None
2024-12-03T12:11:14Z root         INFO               no agreement identifier found, poll again in a second (1)
2024-12-03T12:11:15Z root         INFO             Agreement ID: cdff3c1c-78b1-4a82-be8b-f2652df18767
2024-12-03T12:11:15Z root         INFO     
2024-12-03T12:11:15Z root         INFO         13. START TRANSFER TARGET FILE
2024-12-03T12:11:15Z root         DEBUG          start_transfer_target_file_pharma_shapes as json:
2024-12-03T12:11:15Z root         INFO             Transfer ID: 7917c5e6-e9d0-4174-958d-8d41fe0ccf84
2024-12-03T12:11:15Z root         INFO     
2024-12-03T12:11:15Z root         INFO         14. GET ENDPOINT DATA REFERENCE TARGET FILE
2024-12-03T12:11:15Z root         INFO             Endpoint: None Token: None...
2024-12-03T12:11:15Z root         INFO               no data endpoint found, poll again in a second (1)
2024-12-03T12:11:16Z root         INFO             Endpoint: http://localhost:19291/public Token: eyJraWQi...
2024-12-03T12:11:16Z root         INFO     
2024-12-03T12:11:16Z root         INFO         15. PUSH THE DATA TO ACCURIDS API HOSPITAL FILE UPLOAD
2024-12-03T12:11:16Z root         DEBUG          Content-Length: 12762
2024-12-03T12:11:16Z root         DEBUG            File upload complete.
2024-12-03T12:11:16Z root         INFO     
2024-12-03T12:11:16Z root         INFO         16. FETCH CATALOG TARGET GRAPHQL
22024-12-03T12:11:16Z root         INFO     
2024-12-03T12:11:16Z root         INFO         17. NEGOTIATE CONTRACT TARGET GRAPHQL
2024-12-03T12:11:16Z root         INFO             Negotiation ID: 7e449f8c-cc64-470b-8c86-d5baf5547595
2024-12-03T12:11:16Z root         INFO     
2024-12-03T12:11:16Z root         INFO         18. GET AGREEMENT ID TARGET GRAPHQL
2024-12-03T12:11:16Z root         INFO             Agreement ID: None
2024-12-03T12:11:16Z root         INFO               no agreement identifier found, poll again in a second (1)
2024-12-03T12:11:17Z root         INFO             Agreement ID: 6625542d-5571-4ef4-a36d-669cd89228e0
2024-12-03T12:11:17Z root         INFO     
2024-12-03T12:11:17Z root         INFO         19. START TRANSFER TARGET GRAPHQL
2024-12-03T12:11:17Z root         INFO             Transfer ID: d2fed797-0209-4d6f-a48a-38393494e9bb
2024-12-03T12:11:17Z root         INFO     
2024-12-03T12:11:17Z root         INFO         20. GET ENDPOINT DATA REFERENCE TARGET GRAPHQL
2024-12-03T12:11:17Z root         INFO             Endpoint: None Token: None...
2024-12-03T12:11:17Z root         INFO               no data endpoint found, poll again in a second (1)
2024-12-03T12:11:18Z root         INFO             Endpoint: http://localhost:19291/public Token: eyJraWQi...
2024-12-03T12:11:18Z root         INFO     
2024-12-03T12:11:18Z root         INFO         21. PUSH THE DATA TO ACCURIDS API HOSPITAL DATASET UPDATE
2024-12-03T12:11:18Z root         INFO             Dataset upload done.
2024-12-03T12:11:18Z root         INFO     
2024-12-03T12:11:18Z root         INFO     PHARMA TRIAL
2024-12-03T12:11:18Z root         INFO     
2024-12-03T12:11:18Z root         INFO       Download Pharma Trial
2024-12-03T12:11:18Z root         INFO     
2024-12-03T12:11:18Z root         INFO         4. FETCH CATALOG
2024-12-03T12:11:18Z root         INFO     
2024-12-03T12:11:18Z root         INFO         5. NEGOTIATE CONTRACT SOURCE
2024-12-03T12:11:18Z root         INFO             Negotiation ID: b783fe38-ec89-4c1e-ba4e-12be702aa6ed
2024-12-03T12:11:18Z root         INFO     
2024-12-03T12:11:18Z root         INFO         6. GET AGREEMENT ID SOURCE
2024-12-03T12:11:18Z root         INFO             Agreement ID: None
2024-12-03T12:11:18Z root         INFO               no agreement identifier found, poll again in a second (1)
2024-12-03T12:11:19Z root         INFO             Agreement ID: 3092d040-98d5-43fe-bdf0-f2f2d3e0dd68
2024-12-03T12:11:19Z root         INFO     
2024-12-03T12:11:19Z root         INFO         7. START TRANSFER SOURCE
2024-12-03T12:11:19Z root         INFO             Transfer ID: 5d0f3ec2-db29-4784-af82-87825339f397
2024-12-03T12:11:19Z root         INFO     
2024-12-03T12:11:19Z root         INFO         8. GET ENDPOINT DATA REFERENCE SOURCE
2024-12-03T12:11:19Z root         INFO             Endpoint: None Token: None...
2024-12-03T12:11:19Z root         INFO               no data endpoint found, poll again in a second (1)
2024-12-03T12:11:20Z root         INFO             Endpoint: None Token: None...
2024-12-03T12:11:20Z root         INFO               no data endpoint found, poll again in a second (2)
2024-12-03T12:11:22Z root         INFO             Endpoint: http://localhost:19291/public Token: eyJraWQi...
2024-12-03T12:11:22Z root         INFO     
2024-12-03T12:11:22Z root         INFO         9. GET THE DATA FROM ACCURIDS API PHARMA
2024-12-03T12:11:22Z root         INFO             Download done.
2024-12-03T12:11:22Z root         INFO           This is the first download.
2024-12-03T12:11:22Z root         INFO     
2024-12-03T12:11:22Z root         INFO       Upload Pharma Trial
2024-12-03T12:11:22Z root         INFO     
2024-12-03T12:11:22Z root         INFO         10. FETCH CATALOG TARGET FILE
2024-12-03T12:11:22Z root         INFO         11. NEGOTIATE CONTRACT TARGET FILE
2024-12-03T12:11:22Z root         INFO             Negotiation ID: 55e2aec9-ec45-4b47-94cd-b6bb266185c4
2024-12-03T12:11:22Z root         INFO     
2024-12-03T12:11:22Z root         INFO         12. GET AGREEMENT ID TARGET FILE
2024-12-03T12:11:22Z root         INFO             Agreement ID: None
2024-12-03T12:11:22Z root         INFO               no agreement identifier found, poll again in a second (1)
2024-12-03T12:11:23Z root         INFO             Agreement ID: 780b864d-738c-49b7-84fd-5ee8f144f3ed
2024-12-03T12:11:23Z root         INFO     
2024-12-03T12:11:23Z root         INFO         13. START TRANSFER TARGET FILE
2024-12-03T12:11:23Z root         INFO             Transfer ID: 73e7623d-1ab0-417e-8121-68a552d96c18
2024-12-03T12:11:23Z root         INFO     
2024-12-03T12:11:23Z root         INFO         14. GET ENDPOINT DATA REFERENCE TARGET FILE
2024-12-03T12:11:23Z root         INFO             Endpoint: None Token: None...
2024-12-03T12:11:23Z root         INFO               no data endpoint found, poll again in a second (1)
2024-12-03T12:11:24Z root         INFO             Endpoint: None Token: None...
2024-12-03T12:11:24Z root         INFO               no data endpoint found, poll again in a second (2)
2024-12-03T12:11:25Z root         INFO             Endpoint: http://localhost:19291/public Token: eyJraWQi...
2024-12-03T12:11:25Z root         INFO     
2024-12-03T12:11:25Z root         INFO         15. PUSH THE DATA TO ACCURIDS API HOSPITAL FILE UPLOAD
2024-12-03T12:11:25Z root         DEBUG            File upload complete.
2024-12-03T12:11:25Z root         INFO     
2024-12-03T12:11:25Z root         INFO         16. FETCH CATALOG TARGET GRAPHQL
2024-12-03T12:11:25Z root         INFO         17. NEGOTIATE CONTRACT TARGET GRAPHQL
2024-12-03T12:11:25Z root         INFO             Negotiation ID: bbec2540-7177-4a8c-b0e2-1774972a502b
2024-12-03T12:11:25Z root         INFO     
2024-12-03T12:11:25Z root         INFO         18. GET AGREEMENT ID TARGET GRAPHQL
2024-12-03T12:11:25Z root         INFO             Agreement ID: None
2024-12-03T12:11:25Z root         INFO               no agreement identifier found, poll again in a second (1)
2024-12-03T12:11:26Z root         INFO             Agreement ID: ed0bee10-f7f9-466c-a0d5-04b7094a133c
2024-12-03T12:11:26Z root         INFO     
2024-12-03T12:11:26Z root         INFO         19. START TRANSFER TARGET GRAPHQL
2024-12-03T12:11:26Z root         INFO             Transfer ID: 7342b689-000d-4fb8-b054-49f97e7a77c4
2024-12-03T12:11:26Z root         INFO     
2024-12-03T12:11:26Z root         INFO         20. GET ENDPOINT DATA REFERENCE TARGET GRAPHQL
2024-12-03T12:11:26Z root         INFO             Endpoint: None Token: None...
2024-12-03T12:11:26Z root         INFO               no data endpoint found, poll again in a second (1)
2024-12-03T12:11:27Z root         INFO             Endpoint: http://localhost:19291/public Token: eyJraWQi...
2024-12-03T12:11:27Z root         INFO     
2024-12-03T12:11:27Z root         INFO         21. PUSH THE DATA TO ACCURIDS API HOSPITAL DATASET UPDATE
2024-12-03T12:11:27Z root         INFO             Dataset upload done.
2024-12-03T12:11:27Z root         INFO     
2024-12-03T12:11:27Z root         INFO     HOSPITAL HUMAN BIOSAMPLE
2024-12-03T12:11:27Z root         INFO     
2024-12-03T12:11:27Z root         INFO       Download Hospital Human Biosample
2024-12-03T12:11:27Z root         INFO     
2024-12-03T12:11:27Z root         INFO         4. FETCH CATALOG
2024-12-03T12:11:27Z root         INFO     
2024-12-03T12:11:27Z root         INFO         5. NEGOTIATE CONTRACT SOURCE
2024-12-03T12:11:27Z root         INFO             Negotiation ID: f09ed1c7-bebe-4fe5-aab4-de94d3d717a5
2024-12-03T12:11:27Z root         INFO     
2024-12-03T12:11:27Z root         INFO         6. GET AGREEMENT ID SOURCE
2024-12-03T12:11:27Z root         INFO             Agreement ID: None
2024-12-03T12:11:27Z root         INFO               no agreement identifier found, poll again in a second (1)
2024-12-03T12:11:28Z root         INFO             Agreement ID: e545783d-5a99-471a-bf6d-0eb11c4230cb
2024-12-03T12:11:28Z root         INFO     
2024-12-03T12:11:28Z root         INFO         7. START TRANSFER SOURCE
2024-12-03T12:11:28Z root         INFO             Transfer ID: 8c95002c-f33a-4e63-93a3-371dfac84b0d
2024-12-03T12:11:28Z root         INFO     
2024-12-03T12:11:28Z root         INFO         8. GET ENDPOINT DATA REFERENCE SOURCE
2024-12-03T12:11:28Z root         INFO             Endpoint: None Token: None...
2024-12-03T12:11:28Z root         INFO               no data endpoint found, poll again in a second (1)
2024-12-03T12:11:29Z root         INFO             Endpoint: http://localhost:19291/public Token: eyJraWQi...
2024-12-03T12:11:29Z root         INFO     
2024-12-03T12:11:29Z root         INFO         9. GET THE DATA FROM ACCURIDS API HOSPITAL
2024-12-03T12:11:30Z root         ERROR          File download failed.
2024-12-03T12:11:30Z root         INFO     
2024-12-03T12:11:30Z root         INFO     HOSPITAL PATIENT COLLABORATION
2024-12-03T12:11:30Z root         INFO     
2024-12-03T12:11:30Z root         INFO       Download Hospital Patient Collaboration
2024-12-03T12:11:30Z root         INFO     
2024-12-03T12:11:30Z root         INFO         4. FETCH CATALOG
2024-12-03T12:11:30Z root         INFO     
2024-12-03T12:11:30Z root         INFO         5. NEGOTIATE CONTRACT SOURCE
2024-12-03T12:11:30Z root         INFO             Negotiation ID: fb55fe27-28d9-4b56-9750-0e5e69d443e5
2024-12-03T12:11:30Z root         INFO     
2024-12-03T12:11:30Z root         INFO         6. GET AGREEMENT ID SOURCE
2024-12-03T12:11:30Z root         INFO             Agreement ID: None
2024-12-03T12:11:30Z root         INFO               no agreement identifier found, poll again in a second (1)
2024-12-03T12:11:31Z root         INFO             Agreement ID: fff8d104-928d-4c29-8609-3fbee77e1df6
2024-12-03T12:11:31Z root         INFO     
2024-12-03T12:11:31Z root         INFO         7. START TRANSFER SOURCE
2024-12-03T12:11:31Z root         INFO             Transfer ID: 63028b5e-b93e-4918-83c3-e184d9269393
2024-12-03T12:11:31Z root         INFO     
2024-12-03T12:11:31Z root         INFO         8. GET ENDPOINT DATA REFERENCE SOURCE
2024-12-03T12:11:31Z root         INFO             Endpoint: None Token: None...
2024-12-03T12:11:31Z root         INFO               no data endpoint found, poll again in a second (1)
2024-12-03T12:11:32Z root         INFO             Endpoint: None Token: None...
2024-12-03T12:11:32Z root         INFO               no data endpoint found, poll again in a second (2)
2024-12-03T12:11:33Z root         INFO             Endpoint: http://localhost:19291/public Token: eyJraWQi...
2024-12-03T12:11:33Z root         INFO     
2024-12-03T12:11:33Z root         INFO         9. GET THE DATA FROM ACCURIDS API HOSPITAL
2024-12-03T12:11:33Z root         INFO             Download done.
2024-12-03T12:11:33Z root         INFO           This is the first download.
2024-12-03T12:11:33Z root         INFO     
2024-12-03T12:11:33Z root         INFO       Upload Hospital Patient Collaboration
2024-12-03T12:11:33Z root         INFO     
2024-12-03T12:11:33Z root         INFO         10. FETCH CATALOG TARGET FILE
2024-12-03T12:11:33Z root         INFO     
2024-12-03T12:11:33Z root         INFO         11. NEGOTIATE CONTRACT TARGET FILE
2024-12-03T12:11:33Z root         INFO             Negotiation ID: aea71b7e-9a6b-448b-9384-29d8799dbf78
2024-12-03T12:11:33Z root         INFO     
2024-12-03T12:11:33Z root         INFO         12. GET AGREEMENT ID TARGET FILE
2024-12-03T12:11:33Z root         INFO             Agreement ID: None
2024-12-03T12:11:33Z root         INFO               no agreement identifier found, poll again in a second (1)
2024-12-03T12:11:34Z root         INFO             Agreement ID: 8ff8a0ef-49e1-4a2c-badb-91547f83debc
2024-12-03T12:11:34Z root         INFO     
2024-12-03T12:11:34Z root         INFO         13. START TRANSFER TARGET FILE
2024-12-03T12:11:34Z root         INFO             Transfer ID: 337234a0-4d7d-4d63-a300-0ad5e203b909
2024-12-03T12:11:34Z root         INFO     
2024-12-03T12:11:34Z root         INFO         14. GET ENDPOINT DATA REFERENCE TARGET FILE
2024-12-03T12:11:34Z root         INFO             Endpoint: None Token: None...
2024-12-03T12:11:34Z root         INFO               no data endpoint found, poll again in a second (1)
2024-12-03T12:11:35Z root         INFO             Endpoint: http://localhost:19291/public Token: eyJraWQi...
2024-12-03T12:11:35Z root         INFO     
2024-12-03T12:11:35Z root         INFO         15. PUSH THE DATA TO ACCURIDS API PHARMA FILE UPLOAD
2024-12-03T12:11:35Z root         DEBUG            File upload complete.
2024-12-03T12:11:35Z root         INFO     
2024-12-03T12:11:35Z root         INFO         16. FETCH CATALOG TARGET GRAPHQL
2024-12-03T12:11:35Z root         INFO     
2024-12-03T12:11:35Z root         INFO         17. NEGOTIATE CONTRACT TARGET GRAPHQL
2024-12-03T12:11:35Z root         INFO             Negotiation ID: 7155ada9-1f10-485b-a8c3-fe670c35eed8
2024-12-03T12:11:35Z root         INFO     
2024-12-03T12:11:35Z root         INFO         18. GET AGREEMENT ID TARGET GRAPHQL
2024-12-03T12:11:35Z root         INFO             Agreement ID: None
2024-12-03T12:11:35Z root         INFO               no agreement identifier found, poll again in a second (1)
2024-12-03T12:11:36Z root         INFO             Agreement ID: 55c8b028-88bf-4b86-a11e-e0501b1c4cb3
2024-12-03T12:11:36Z root         INFO     
2024-12-03T12:11:36Z root         INFO         19. START TRANSFER TARGET GRAPHQL
2024-12-03T12:11:36Z root         INFO             Transfer ID: c4b26927-681c-4ca3-8338-13f10b30a382
2024-12-03T12:11:36Z root         INFO     
2024-12-03T12:11:36Z root         INFO         20. GET ENDPOINT DATA REFERENCE TARGET GRAPHQL
2024-12-03T12:11:36Z root         INFO             Endpoint: None Token: None...
2024-12-03T12:11:36Z root         INFO               no data endpoint found, poll again in a second (1)
2024-12-03T12:11:37Z root         INFO             Endpoint: http://localhost:19291/public Token: eyJraWQi...
2024-12-03T12:11:37Z root         INFO     
2024-12-03T12:11:37Z root         INFO         21. PUSH THE DATA TO ACCURIDS API PHARMA DATASET UPDATE
2024-12-03T12:11:37Z root         INFO             Dataset upload done.
2024-12-03T12:11:37Z root         INFO     
2024-12-03T12:11:37Z root         INFO     UPDATE CYCLE 00002
2024-12-03T12:11:37Z root         INFO     
2024-12-03T12:11:37Z root         INFO     PHARMA REFERENCE DATA
...
```
import requests, json, sys, logging, colorlog, uuid, time, os
from datetime import datetime
import jsonpath_ng.ext
from rich.pretty import pprint,pretty_repr

json_folder="./json/"
provider_url_and_management_port="http://localhost:19193"
consumer_url_and_management_port="http://localhost:29193"

timeout_agreement=10 # number of seconds to poll for an agreement identifier
timeout_transfer=10 # number of seconds to poll for an endpoint data reference
stepwise_confirmation=False
repeat_after=0 # number of seconds to wait before running the next execution cycle

### PREREQUISITES

### Execute in Windows Command Prompt (powershell needs further escaping or quotes)
### Start consumer: java -Dedc.keystore=./certs/cert.pfx -Dedc.keystore.password=123456 -Dedc.fs.config=./config/consumer-configuration.properties -jar accurids-connector.jar
### Start provider: java -Dedc.keystore=./certs/cert.pfx -Dedc.keystore.password=123456 -Dedc.fs.config=./config/provider-configuration.properties -jar accurids-connector.jar

### setup logging
timestamp=datetime.fromtimestamp(datetime.timestamp(datetime.now()), tz=None).strftime("%d-%m-%Y-%H-%M-%S")
logfile=f"edc_demo.log"
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%Y-%m-%dT%H:%M:%SZ', filename=logfile, filemode='w')

stdout=colorlog.StreamHandler(stream=sys.stdout)
fmt=colorlog.ColoredFormatter(fmt="%(purple)s%(filename)s:%(lineno)s%(reset)s %(log_color)s%(message)s%(reset)s", datefmt='%Y-%m-%dT%H:%M:%SZ')
stdout.setFormatter(fmt)
stdout.setLevel(logging.INFO)
logging.getLogger('').addHandler(stdout)

### READ API KEYS FROM ENV VARIABLES

accurids_apikey_pharma = os.environ['API_KEY_PHARMA']
accurids_apikey_hospital = os.environ['API_KEY_HOSPITAL']

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook(exc_type, exc_value, exc_traceback) 
        return
    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
sys.excepthook=handle_exception

def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

def try_find_value_in_json(jsonpath_expr, json_data):
    try:
        return jsonpath_expr.find(json_data)[0].value
    except:
        return None
    
def call_endpoint(endpoint, data=None):
    if data:
        response = requests.post(url=endpoint, data=data, headers={"Content-Type": "application/json"})
    else:
        response = requests.get(url=endpoint, headers={"Content-Type": "application/json"})
    response_dict = response.json() 
    logging.debug(f"Response:\n{json.dumps(response_dict, indent=4, sort_keys=True)}")
    return response_dict

### MAIN

### Read the JSON messages for later POST

### ASSETS
create_asset_source_hospital_human_biosample=None
with open(json_folder+'create-asset-accurids-source-hospital-human-biosample.json', 'r') as create_asset_file:
    create_asset_source_hospital_human_biosample = json.load(create_asset_file)
create_asset_source_hospital_human_biosample=json.loads(json.dumps(create_asset_source_hospital_human_biosample).replace("{{APIKEY}}", accurids_apikey_hospital))
logging.debug(f"create_asset_source_hospital_human_biosample as json:\n{json.dumps(create_asset_source_hospital_human_biosample,indent=4)}")

create_asset_target_file_hospital_human_biosample=None
with open(json_folder+'create-asset-accurids-target-file-hospital-human-biosample.json', 'r') as create_asset_file:
    create_asset_target_file_hospital_human_biosample = json.load(create_asset_file)
create_asset_target_file_hospital_human_biosample=json.loads(json.dumps(create_asset_target_file_hospital_human_biosample).replace("{{APIKEY}}", accurids_apikey_pharma))
logging.debug(f"create_asset_target_file_hospital_human_biosample as json:\n{json.dumps(create_asset_target_file_hospital_human_biosample,indent=4)}")

create_asset_target_graphql_hospital=None
with open(json_folder+'create-asset-accurids-target-graphql-hospital.json', 'r') as create_asset_file:
    create_asset_target_graphql_hospital = json.load(create_asset_file)
create_asset_target_graphql_hospital=json.loads(json.dumps(create_asset_target_graphql_hospital).replace("{{APIKEY}}", accurids_apikey_pharma))
logging.debug(f"create_asset_target_graphql_hospital as json:\n{json.dumps(create_asset_target_graphql_hospital,indent=4)}")

create_asset_source_hospital_patient_collaboration=None
with open(json_folder+'create-asset-accurids-source-hospital-patient-collaboration.json', 'r') as create_asset_file:
    create_asset_source_hospital_patient_collaboration = json.load(create_asset_file)
create_asset_source_hospital_patient_collaboration=json.loads(json.dumps(create_asset_source_hospital_patient_collaboration).replace("{{APIKEY}}", accurids_apikey_hospital))
logging.debug(f"create_asset_source_hospital_patient_collaboration as json:\n{json.dumps(create_asset_source_hospital_patient_collaboration,indent=4)}")

create_asset_target_file_hospital_patient_collaboration=None
with open(json_folder+'create-asset-accurids-target-file-hospital-patient-collaboration.json', 'r') as create_asset_file:
    create_asset_target_file_hospital_patient_collaboration = json.load(create_asset_file)
create_asset_target_file_hospital_patient_collaboration=json.loads(json.dumps(create_asset_target_file_hospital_patient_collaboration).replace("{{APIKEY}}", accurids_apikey_pharma))
logging.debug(f"create_asset_target_file_hospital_patient_collaboration as json:\n{json.dumps(create_asset_target_file_hospital_patient_collaboration,indent=4)}")



create_asset_source_pharma_reference_data=None
with open(json_folder+'create-asset-accurids-source-pharma-reference-data.json', 'r') as create_asset_file:
    create_asset_source_pharma_reference_data = json.load(create_asset_file)
create_asset_source_pharma_reference_data=json.loads(json.dumps(create_asset_source_pharma_reference_data).replace("{{APIKEY}}", accurids_apikey_pharma))
logging.debug(f"create_asset_source_pharma_reference_data as json:\n{json.dumps(create_asset_source_pharma_reference_data,indent=4)}")

create_asset_target_file_pharma_reference_data=None
with open(json_folder+'create-asset-accurids-target-file-pharma-reference-data.json', 'r') as create_asset_file:
    create_asset_target_file_pharma_reference_data = json.load(create_asset_file)
create_asset_target_file_pharma_reference_data=json.loads(json.dumps(create_asset_target_file_pharma_reference_data).replace("{{APIKEY}}", accurids_apikey_hospital))
logging.debug(f"create_asset_target_file_pharma_reference_data as json:\n{json.dumps(create_asset_target_file_pharma_reference_data,indent=4)}")

create_asset_target_graphql_pharma=None
with open(json_folder+'create-asset-accurids-target-graphql-pharma.json', 'r') as create_asset_file:
    create_asset_target_graphql_pharma = json.load(create_asset_file)
create_asset_target_graphql_pharma=json.loads(json.dumps(create_asset_target_graphql_pharma).replace("{{APIKEY}}", accurids_apikey_hospital))
logging.debug(f"create_asset_target_graphql_pharma as json:\n{json.dumps(create_asset_target_graphql_pharma,indent=4)}")

create_asset_source_pharma_shapes=None
with open(json_folder+'create-asset-accurids-source-pharma-shapes.json', 'r') as create_asset_file:
    create_asset_source_pharma_shapes = json.load(create_asset_file)
create_asset_source_pharma_shapes=json.loads(json.dumps(create_asset_source_pharma_shapes).replace("{{APIKEY}}", accurids_apikey_pharma))
logging.debug(f"create_asset_source_pharma_shapes as json:\n{json.dumps(create_asset_source_pharma_shapes,indent=4)}")

create_asset_target_file_pharma_shapes=None
with open(json_folder+'create-asset-accurids-target-file-pharma-shapes.json', 'r') as create_asset_file:
    create_asset_target_file_pharma_shapes = json.load(create_asset_file)
create_asset_target_file_pharma_shapes=json.loads(json.dumps(create_asset_target_file_pharma_shapes).replace("{{APIKEY}}", accurids_apikey_hospital))
logging.debug(f"create_asset_target_file_pharma_shapes as json:\n{json.dumps(create_asset_target_file_pharma_shapes,indent=4)}")

create_asset_source_pharma_trial=None
with open(json_folder+'create-asset-accurids-source-pharma-trial.json', 'r') as create_asset_file:
    create_asset_source_pharma_trial = json.load(create_asset_file)
create_asset_source_pharma_trial=json.loads(json.dumps(create_asset_source_pharma_trial).replace("{{APIKEY}}", accurids_apikey_pharma))
logging.debug(f"create_asset_source_pharma_trial as json:\n{json.dumps(create_asset_source_pharma_trial,indent=4)}")

create_asset_target_file_pharma_trial=None
with open(json_folder+'create-asset-accurids-target-file-pharma-trial.json', 'r') as create_asset_file:
    create_asset_target_file_pharma_trial = json.load(create_asset_file)
create_asset_target_file_pharma_trial=json.loads(json.dumps(create_asset_target_file_pharma_trial).replace("{{APIKEY}}", accurids_apikey_hospital))
logging.debug(f"create_asset_target_file_pharma_trial as json:\n{json.dumps(create_asset_target_file_pharma_trial,indent=4)}")


### POLICIES
create_policy=None
with open(json_folder+'create-policy-accurids.json', 'r') as create_policy_file:
    create_policy = json.load(create_policy_file)
logging.debug(f"create_policy_source as json:\n{json.dumps(create_policy,indent=4)}")

### CONTRACT
create_contract=None
with open(json_folder+'create-contract-definition-accurids.json', 'r') as create_contract_file:
    create_contract = json.load(create_contract_file)
logging.debug(f"create_contract as json:\n{json.dumps(create_contract,indent=4)}")

### CATALOG
fetch_catalog=None
with open(json_folder+'fetch-catalog.json', 'r') as fetch_catalog_file:
    fetch_catalog = json.load(fetch_catalog_file)
logging.debug(f"fetch_catalog as json:\n{json.dumps(fetch_catalog,indent=4)}")


### CONTRACT NEGOTIATION
negotiate_contract_source_hospital_human_biosample=None
with open(json_folder+'negotiate-contract-accurids-source-hospital-human-biosample.json', 'r') as negotiate_contract_file:
    negotiate_contract_source_hospital_human_biosample = json.load(negotiate_contract_file)
logging.debug(f"negotiate_contract_source_hospital_human_biosample as json:\n{json.dumps(negotiate_contract_source_hospital_human_biosample,indent=4)}")

negotiate_contract_target_file_hospital_human_biosample=None
with open(json_folder+'negotiate-contract-accurids-target-file-hospital-human-biosample.json', 'r') as negotiate_contract_file:
    negotiate_contract_target_file_hospital_human_biosample = json.load(negotiate_contract_file)
logging.debug(f"negotiate_contract_target_file_hospital_human_biosample as json:\n{json.dumps(negotiate_contract_target_file_hospital_human_biosample,indent=4)}")

negotiate_contract_target_graphql_hospital=None
with open(json_folder+'negotiate-contract-accurids-target-graphql-hospital.json', 'r') as negotiate_contract_file:
    negotiate_contract_target_graphql_hospital = json.load(negotiate_contract_file)
logging.debug(f"negotiate_contract_target_graphql_hospital as json:\n{json.dumps(negotiate_contract_target_graphql_hospital,indent=4)}")

negotiate_contract_source_hospital_patient_collaboration=None
with open(json_folder+'negotiate-contract-accurids-source-hospital-patient-collaboration.json', 'r') as negotiate_contract_file:
    negotiate_contract_source_hospital_patient_collaboration = json.load(negotiate_contract_file)
logging.debug(f"negotiate_contract_source_hospital_patient_collaboration as json:\n{json.dumps(negotiate_contract_source_hospital_patient_collaboration,indent=4)}")

negotiate_contract_target_file_hospital_patient_collaboration=None
with open(json_folder+'negotiate-contract-accurids-target-file-hospital-patient-collaboration.json', 'r') as negotiate_contract_file:
    negotiate_contract_target_file_hospital_patient_collaboration = json.load(negotiate_contract_file)
logging.debug(f"negotiate_contract_target_file_hospital_patient_collaboration as json:\n{json.dumps(negotiate_contract_target_file_hospital_patient_collaboration,indent=4)}")


negotiate_contract_source_pharma_reference_data=None
with open(json_folder+'negotiate-contract-accurids-source-pharma-reference-data.json', 'r') as negotiate_contract_file:
    negotiate_contract_source_pharma_reference_data = json.load(negotiate_contract_file)
logging.debug(f"negotiate_contract_source_pharma_reference_data as json:\n{json.dumps(negotiate_contract_source_pharma_reference_data,indent=4)}")

negotiate_contract_target_file_pharma_reference_data=None
with open(json_folder+'negotiate-contract-accurids-target-file-pharma-reference-data.json', 'r') as negotiate_contract_file:
    negotiate_contract_target_file_pharma_reference_data = json.load(negotiate_contract_file)
logging.debug(f"negotiate_contract_target_file_pharma_reference_data as json:\n{json.dumps(negotiate_contract_target_file_pharma_reference_data,indent=4)}")

negotiate_contract_target_graphql_pharma=None
with open(json_folder+'negotiate-contract-accurids-target-graphql-pharma.json', 'r') as negotiate_contract_file:
    negotiate_contract_target_graphql_pharma = json.load(negotiate_contract_file)
logging.debug(f"negotiate_contract_target_graphql_pharma as json:\n{json.dumps(negotiate_contract_target_graphql_pharma,indent=4)}")

negotiate_contract_source_pharma_shapes=None
with open(json_folder+'negotiate-contract-accurids-source-pharma-shapes.json', 'r') as negotiate_contract_file:
    negotiate_contract_source_pharma_shapes = json.load(negotiate_contract_file)
logging.debug(f"negotiate_contract_source_pharma_shapes as json:\n{json.dumps(negotiate_contract_source_pharma_shapes,indent=4)}")

negotiate_contract_target_file_pharma_shapes=None
with open(json_folder+'negotiate-contract-accurids-target-file-pharma-shapes.json', 'r') as negotiate_contract_file:
    negotiate_contract_target_file_pharma_shapes = json.load(negotiate_contract_file)
logging.debug(f"negotiate_contract_target_file_pharma_shapes as json:\n{json.dumps(negotiate_contract_target_file_pharma_shapes,indent=4)}")

negotiate_contract_source_pharma_trial=None
with open(json_folder+'negotiate-contract-accurids-source-pharma-trial.json', 'r') as negotiate_contract_file:
    negotiate_contract_source_pharma_trial = json.load(negotiate_contract_file)
logging.debug(f"negotiate_contract_source_pharma_trial as json:\n{json.dumps(negotiate_contract_source_pharma_trial,indent=4)}")

negotiate_contract_target_file_pharma_trial=None
with open(json_folder+'negotiate-contract-accurids-target-file-pharma-trial.json', 'r') as negotiate_contract_file:
    negotiate_contract_target_file_pharma_trial = json.load(negotiate_contract_file)
logging.debug(f"negotiate_contract_target_file_pharma_trial as json:\n{json.dumps(negotiate_contract_target_file_pharma_trial,indent=4)}")


### TRANSFER
start_transfer_source_hospital_human_biosample=None
with open(json_folder+'start-transfer-accurids-source-hospital-human-biosample.json', 'r') as start_transfer_file:
    start_transfer_source_hospital_human_biosample = json.load(start_transfer_file)
logging.debug(f"start_transfer_source_hospital_human_biosample as json:\n{json.dumps(start_transfer_source_hospital_human_biosample,indent=4)}")

start_transfer_target_file_hospital_human_biosample=None
with open(json_folder+'start-transfer-accurids-target-file-hospital-human-biosample.json', 'r') as start_transfer_file:
    start_transfer_target_file_hospital_human_biosample = json.load(start_transfer_file)
logging.debug(f"start_transfer_target_file_hospital_human_biosample as json:\n{json.dumps(start_transfer_target_file_hospital_human_biosample,indent=4)}")

start_transfer_target_graphql_hospital=None
with open(json_folder+'start-transfer-accurids-target-graphql-hospital.json', 'r') as start_transfer_file:
    start_transfer_target_graphql_hospital = json.load(start_transfer_file)
logging.debug(f"start_transfer_target_graphql_hospital as json:\n{json.dumps(start_transfer_target_graphql_hospital,indent=4)}")

start_transfer_source_hospital_patient_collaboration=None
with open(json_folder+'start-transfer-accurids-source-hospital-patient-collaboration.json', 'r') as start_transfer_file:
    start_transfer_source_hospital_patient_collaboration = json.load(start_transfer_file)
logging.debug(f"start_transfer_source_hospital_patient_collaboration as json:\n{json.dumps(start_transfer_source_hospital_patient_collaboration,indent=4)}")

start_transfer_target_file_hospital_patient_collaboration=None
with open(json_folder+'start-transfer-accurids-target-file-hospital-patient-collaboration.json', 'r') as start_transfer_file:
    start_transfer_target_file_hospital_patient_collaboration = json.load(start_transfer_file)
logging.debug(f"start_transfer_target_file_hospital_patient_collaboration as json:\n{json.dumps(start_transfer_target_file_hospital_patient_collaboration,indent=4)}")



start_transfer_source_pharma_reference_data=None
with open(json_folder+'start-transfer-accurids-source-pharma-reference-data.json', 'r') as start_transfer_file:
    start_transfer_source_pharma_reference_data = json.load(start_transfer_file)
logging.debug(f"start_transfer_source_pharma_reference_data as json:\n{json.dumps(start_transfer_source_pharma_reference_data,indent=4)}")

start_transfer_target_file_pharma_reference_data=None
with open(json_folder+'start-transfer-accurids-target-file-pharma-reference-data.json', 'r') as start_transfer_file:
    start_transfer_target_file_pharma_reference_data = json.load(start_transfer_file)
logging.debug(f"start_transfer_target_file_pharma_reference_data as json:\n{json.dumps(start_transfer_target_file_pharma_reference_data,indent=4)}")

start_transfer_target_graphql_pharma=None
with open(json_folder+'start-transfer-accurids-target-graphql-pharma.json', 'r') as start_transfer_file:
    start_transfer_target_graphql_pharma = json.load(start_transfer_file)
logging.debug(f"start_transfer_target_graphql_pharma as json:\n{json.dumps(start_transfer_target_graphql_pharma,indent=4)}")

start_transfer_source_pharma_shapes=None
with open(json_folder+'start-transfer-accurids-source-pharma-shapes.json', 'r') as start_transfer_file:
    start_transfer_source_pharma_shapes = json.load(start_transfer_file)
logging.debug(f"start_transfer_source_pharma_shapes as json:\n{json.dumps(start_transfer_source_pharma_shapes,indent=4)}")

start_transfer_target_file_pharma_shapes=None
with open(json_folder+'start-transfer-accurids-target-file-pharma-shapes.json', 'r') as start_transfer_file:
    start_transfer_target_file_pharma_shapes = json.load(start_transfer_file)
logging.debug(f"start_transfer_target_file_pharma_shapes as json:\n{json.dumps(start_transfer_target_file_pharma_shapes,indent=4)}")

start_transfer_source_pharma_trial=None
with open(json_folder+'start-transfer-accurids-source-pharma-trial.json', 'r') as start_transfer_file:
    start_transfer_source_pharma_trial = json.load(start_transfer_file)
logging.debug(f"start_transfer_source_pharma_trial as json:\n{json.dumps(start_transfer_source_pharma_trial,indent=4)}")

start_transfer_target_file_pharma_trial=None
with open(json_folder+'start-transfer-accurids-target-file-pharma-trial.json', 'r') as start_transfer_file:
    start_transfer_target_file_pharma_trial = json.load(start_transfer_file)
logging.debug(f"start_transfer_target_file_pharma_trial as json:\n{json.dumps(start_transfer_target_file_pharma_trial,indent=4)}")


### Execute the workflow

logging.info(f"1. 1.  CREATE ASSET SOURCE HOSPITAL HUMAN BIOSAMPLE")
if stepwise_confirmation: input("Press Enter to continue...")
call_endpoint(f"{provider_url_and_management_port}/management/v3/assets", json.dumps(create_asset_source_hospital_human_biosample))

logging.info(f"1. 2.  CREATE ASSET TARGET FILE HOSPITAL HUMAN BIOSAMPLE")
if stepwise_confirmation: input("Press Enter to continue...")
call_endpoint(f"{provider_url_and_management_port}/management/v3/assets", json.dumps(create_asset_target_file_hospital_human_biosample))

logging.info(f"1. 3.  CREATE ASSET TARGET GRAPHQL HOSPITAL")
if stepwise_confirmation: input("Press Enter to continue...")
call_endpoint(f"{provider_url_and_management_port}/management/v3/assets", json.dumps(create_asset_target_graphql_hospital))

logging.info(f"1. 4.  CREATE ASSET SOURCE HOSPITAL PATIENT COLLABORATION")
if stepwise_confirmation: input("Press Enter to continue...")
call_endpoint(f"{provider_url_and_management_port}/management/v3/assets", json.dumps(create_asset_source_hospital_patient_collaboration))

logging.info(f"1. 5.  CREATE ASSET TARGET FILE HOSPITAL PATIENT COLLABORATION")
if stepwise_confirmation: input("Press Enter to continue...")
call_endpoint(f"{provider_url_and_management_port}/management/v3/assets", json.dumps(create_asset_target_file_hospital_patient_collaboration))

logging.info(f"1. 6.  CREATE ASSET SOURCE PHARMA REFERENCE DATA")
if stepwise_confirmation: input("Press Enter to continue...")
call_endpoint(f"{provider_url_and_management_port}/management/v3/assets", json.dumps(create_asset_source_pharma_reference_data))

logging.info(f"1. 7.  CREATE ASSET TARGET FILE PHARMA REFERENCE DATA")
if stepwise_confirmation: input("Press Enter to continue...")
call_endpoint(f"{provider_url_and_management_port}/management/v3/assets", json.dumps(create_asset_target_file_pharma_reference_data))

logging.info(f"1. 8.  CREATE ASSET TARGET GRAPHQL PHARMA")
if stepwise_confirmation: input("Press Enter to continue...")
call_endpoint(f"{provider_url_and_management_port}/management/v3/assets", json.dumps(create_asset_target_graphql_pharma))

logging.info(f"1. 9.  CREATE ASSET SOURCE PHARMA SHAPES")
if stepwise_confirmation: input("Press Enter to continue...")
call_endpoint(f"{provider_url_and_management_port}/management/v3/assets", json.dumps(create_asset_source_pharma_shapes))

logging.info(f"1. 10. CREATE ASSET TARGET FILE PHARMA SHAPES")
if stepwise_confirmation: input("Press Enter to continue...")
call_endpoint(f"{provider_url_and_management_port}/management/v3/assets", json.dumps(create_asset_target_file_pharma_shapes))

logging.info(f"1. 11. CREATE ASSET SOURCE PHARMA TRIAL")
if stepwise_confirmation: input("Press Enter to continue...")
call_endpoint(f"{provider_url_and_management_port}/management/v3/assets", json.dumps(create_asset_source_pharma_trial))

logging.info(f"1. 12. CREATE ASSET TARGET FILE PHARMA TRIAL")
if stepwise_confirmation: input("Press Enter to continue...")
call_endpoint(f"{provider_url_and_management_port}/management/v3/assets", json.dumps(create_asset_target_file_pharma_trial))



logging.info(f"2. CREATE POLICY")
if stepwise_confirmation: input("Press Enter to continue...")
call_endpoint(f"{provider_url_and_management_port}/management/v3/policydefinitions", json.dumps(create_policy))

logging.info(f"3. CREATE CONTRACT")
if stepwise_confirmation: input("Press Enter to continue...")
call_endpoint(f"{provider_url_and_management_port}/management/v3/contractdefinitions", json.dumps(create_contract))



def hospital_human_biosample():
    ############################################################
    ##### Hospital Human Biosample 
    ############################################################
    global negotiate_contract_source_hospital_human_biosample, start_transfer_source_hospital_human_biosample, negotiate_contract_target_file_hospital_human_biosample, start_transfer_target_file_hospital_human_biosample, negotiate_contract_target_graphql_hospital, start_transfer_target_graphql_hospital

    logging.info("")
    logging.info("HOSPITAL HUMAN BIOSAMPLE")
    logging.info("")
    logging.info("  Download Hospital Human Biosample")
    logging.info("")
    logging.info(f"    4. FETCH CATALOG")
    if stepwise_confirmation: input("Press Enter to continue...")
    response_json=call_endpoint(f"{provider_url_and_management_port}/management/v3/catalog/request", json.dumps(fetch_catalog))
    jsonPath = f"$.\"dcat:dataset\"[?id = \"hospitalHumanBiosample\"].\"odrl:hasPolicy\".\"@id\""
    logging.debug(f"       JSON PATH: {jsonPath}")
    jsonpath_expr = jsonpath_ng.ext.parse(jsonPath)
    dataset_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Dataset ID: {dataset_id}")
    if (not dataset_id or not dataset_id.startswith("MQ")):
        logging.error(f"      Found an unexpected kind of dataset identifier: {dataset_id}")
        return ""

    logging.info("")
    logging.info(f"    5. NEGOTIATE CONTRACT SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    negotiate_contract_source_hospital_human_biosample=json.loads(json.dumps(negotiate_contract_source_hospital_human_biosample).replace("{{DATASET_ID}}", dataset_id))
    logging.debug(f"      negotiate_contract_source_hospital_human_biosample as json:\n{json.dumps(negotiate_contract_source_hospital_human_biosample, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations", json.dumps(negotiate_contract_source_hospital_human_biosample))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    negotiation_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Negotiation ID: {negotiation_id}")
    if (not negotiation_id or not is_valid_uuid(negotiation_id)):
        logging.error(f"      Found an unexpected kind of negotiation identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    6. GET AGREEMENT ID SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the agreement identifier
    endtime = time.time() + timeout_agreement
    count=0
    agreement_id=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations/{negotiation_id}")
        jsonpath_expr = jsonpath_ng.ext.parse('$.contractAgreementId')
        agreement_id=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Agreement ID: {agreement_id}")
        if (not agreement_id or not is_valid_uuid(agreement_id)):
            if (time.time()+1 < endtime):
                logging.info(f"          no agreement identifier found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not agreement_id or not is_valid_uuid(agreement_id)):
        logging.error(f"      Found an unexpected kind of agreement identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    7. START TRANSFER SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    start_transfer_source_hospital_human_biosample=json.loads(json.dumps(start_transfer_source_hospital_human_biosample).replace("{{CONTRACT_ID}}", agreement_id))
    logging.debug(f"      start_transfer_source_hospital_human_biosample as json:\n{json.dumps(start_transfer_source_hospital_human_biosample, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/transferprocesses", json.dumps(start_transfer_source_hospital_human_biosample))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    transfer_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Transfer ID: {transfer_id}")
    if (not transfer_id or not is_valid_uuid(transfer_id)):
        logging.error(f"      Found an unexpected kind of transfer identifier: {transfer_id}")
        return ""

    logging.info("")
    logging.info(f"    8. GET ENDPOINT DATA REFERENCE SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the endpoint data reference
    endtime = time.time() + timeout_transfer
    count=0
    data_endpoint=None
    token=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/edrs/{transfer_id}/dataaddress")
        jsonpath_expr = jsonpath_ng.ext.parse('$.endpoint')
        data_endpoint=try_find_value_in_json(jsonpath_expr, response_json)
        jsonpath_expr = jsonpath_ng.ext.parse('$.authorization')
        token=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Endpoint: {data_endpoint} Token: {token[:8] if token else None}...")
        if (not data_endpoint or not token):
            if (time.time()+1 < endtime):
                logging.info(f"          no data endpoint found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not data_endpoint or not token):
        logging.error(f"      Found an unexpected data endpoint: {data_endpoint} with token: {token}")
        return ""

    logging.info("")
    logging.info(f"    9. GET THE DATA FROM ACCURIDS API HOSPITAL")
    if stepwise_confirmation: input("Press Enter to continue...")
    response = requests.get(url=data_endpoint, headers={"Authorization": token, "Accept": "text/turtle"})
    logging.debug(f"      Headers:\n{pretty_repr(dict(response.headers))}")
    logging.debug(f"      Content:\n{pretty_repr(response.content)}")

    if (not response.content or b'' == response.content or b'{"errors":["NOT_AUTHORIZED"]}' == response.content):
        logging.error(f"      File download failed.")
        return ""

    turtle=response.content

    f = open('hospitalHumanBiosample.ttl', "w", encoding="utf-8")
    f.write(str(turtle, 'utf-8'))
    f.close()

    logging.info("        Download done.")

    if not turtle:
        logging.info("      Empty file. Skip upload.")
        return ""

    if (os.path.isfile('hospitalHumanBiosample_previous.ttl')):
        previous_turtle = open('hospitalHumanBiosample_previous.ttl', "rb").read()
        if str(turtle, 'utf-8') == str(previous_turtle, 'utf-8'):
            logging.info("      The downloaded file is the same as before. Skip upload.")
            return ""
        else:
            logging.info("      The downloaded file is different from before.")
            f = open('hospitalHumanBiosample_previous.ttl', "w", encoding="utf-8")
            f.write(str(turtle, 'utf-8'))
            f.close()
    else:
        logging.info("      This is the first download.")
        f = open('hospitalHumanBiosample_previous.ttl', "w", encoding="utf-8")
        f.write(str(turtle, 'utf-8'))
        f.close()

    if stepwise_confirmation: input("Press Enter to continue...")

    logging.info("")
    logging.info("  Upload Hospital Human Biosample")
    logging.info("")

    logging.info(f"    10. FETCH CATALOG TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    dataset_id=""
    response_json=call_endpoint(f"{provider_url_and_management_port}/management/v3/catalog/request", json.dumps(fetch_catalog))
    jsonpath_expr = jsonpath_ng.ext.parse(f"$.\"dcat:dataset\"[?id = \"hospitalHumanBiosampleFile\"].\"odrl:hasPolicy\".\"@id\"")
    dataset_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Dataset ID: {dataset_id}")
    if (not dataset_id or not dataset_id.startswith("MQ")):
        logging.error(f"      Found an unexpected kind of dataset identifier: {dataset_id}")
        return ""

    logging.info("")
    logging.info(f"    11. NEGOTIATE CONTRACT TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    negotiation_id=""
    negotiate_contract_target_file_hospital_human_biosample=json.loads(json.dumps(negotiate_contract_target_file_hospital_human_biosample).replace("{{DATASET_ID}}", dataset_id))
    logging.debug(f"      negotiate_contract_target_file_hospital_human_biosample as json:\n{json.dumps(negotiate_contract_target_file_hospital_human_biosample, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations", json.dumps(negotiate_contract_target_file_hospital_human_biosample))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    negotiation_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Negotiation ID: {negotiation_id}")
    if (not negotiation_id or not is_valid_uuid(negotiation_id)):
        logging.error(f"      Found an unexpected kind of negotiation identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    12. GET AGREEMENT ID TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the agreement identifier
    endtime = time.time() + timeout_agreement
    count=0
    agreement_id=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations/{negotiation_id}")
        jsonpath_expr = jsonpath_ng.ext.parse('$.contractAgreementId')
        agreement_id=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Agreement ID: {agreement_id}")
        if (not agreement_id or not is_valid_uuid(agreement_id)):
            if (time.time()+1 < endtime):
                logging.info(f"          no agreement identifier found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not agreement_id or not is_valid_uuid(agreement_id)):
        logging.error(f"      Found an unexpected kind of agreement identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    13. START TRANSFER TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    transfer_id=""
    start_transfer_target_file_hospital_human_biosample=json.loads(json.dumps(start_transfer_target_file_hospital_human_biosample).replace("{{CONTRACT_ID}}", agreement_id))
    logging.debug(f"      start_transfer_target_file_hospital_human_biosample as json:\n{json.dumps(start_transfer_target_file_hospital_human_biosample, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/transferprocesses", json.dumps(start_transfer_target_file_hospital_human_biosample))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    transfer_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Transfer ID: {transfer_id}")
    if (not transfer_id or not is_valid_uuid(transfer_id)):
        logging.error(f"      Found an unexpected kind of transfer identifier: {transfer_id}")
        return ""

    logging.info("")
    logging.info(f"    14. GET ENDPOINT DATA REFERENCE TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the endpoint data reference
    endtime = time.time() + timeout_transfer
    count=0
    data_endpoint=None
    token=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/edrs/{transfer_id}/dataaddress")
        jsonpath_expr = jsonpath_ng.ext.parse('$.endpoint')
        data_endpoint=try_find_value_in_json(jsonpath_expr, response_json)
        jsonpath_expr = jsonpath_ng.ext.parse('$.authorization')
        token=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Endpoint: {data_endpoint} Token: {token[:8] if token else None}...")
        if (not data_endpoint or not token):
            if (time.time()+1 < endtime):
                logging.info(f"          no data endpoint found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not data_endpoint or not token):
        logging.error(f"      Found an unexpected data endpoint: {data_endpoint} with token: {token}")
        return ""

    logging.info("")
    logging.info(f"    15. PUSH THE DATA TO ACCURIDS API PHARMA FILE UPLOAD")
    if stepwise_confirmation: input("Press Enter to continue...")

    #FILE MULTIPART
    boundary = "---------888888888"
    file_content = open('hospitalHumanBiosample.ttl', "rb").read()
    body = f"""\r\n\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"upload\"; filename=\"hospitalHumanBiosample.ttl\"\r\nContent-Type: application/octet-stream\r\n\r\n{file_content.decode("utf-8")}\r\n--{boundary}--\r\n"""

    logging.debug(f"      Body:\n|START|{body}|END|")
    content_length=str(len(body))
    logging.debug(f"      Content-Length: {content_length}")

    # Headers
    headers = {
        "Authorization": token,
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": content_length
    }
    logging.debug(f"      Request Headers:\n{headers}")

    response = requests.post(url=data_endpoint, headers={"Authorization": token, "Content-Type": f"multipart/form-data; boundary={boundary}", "Content-Length": f"{content_length}" }, data=body)

    logging.debug(f"      Response Headers:\n{pretty_repr(dict(response.headers))}")
    logging.debug(f"      Response Content:\n{pretty_repr(response.content)}")

    if (not response.content or not b'success' in response.content):
        logging.error(f"        File upload failed.")
        return ""
    else:
        logging.debug(f"        File upload complete.")

    logging.info("")
    logging.info(f"    16. FETCH CATALOG TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    dataset_id=""
    response_json=call_endpoint(f"{provider_url_and_management_port}/management/v3/catalog/request", json.dumps(fetch_catalog))
    jsonpath_expr = jsonpath_ng.ext.parse(f"$.\"dcat:dataset\"[?id = \"hospitalGraphql\"].\"odrl:hasPolicy\".\"@id\"")
    dataset_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Dataset ID: {dataset_id}")
    if (not dataset_id or not dataset_id.startswith("MQ")):
        logging.error(f"      Found an unexpected kind of dataset identifier: {dataset_id}")
        return ""

    logging.info("")
    logging.info(f"    17. NEGOTIATE CONTRACT TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    negotiation_id=""
    negotiate_contract_target_graphql_hospital=json.loads(json.dumps(negotiate_contract_target_graphql_hospital).replace("{{DATASET_ID}}", dataset_id))
    logging.debug(f"      negotiate_contract_target_graphql_hospital as json:\n{json.dumps(negotiate_contract_target_graphql_hospital, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations", json.dumps(negotiate_contract_target_graphql_hospital))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    negotiation_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Negotiation ID: {negotiation_id}")
    if (not negotiation_id or not is_valid_uuid(negotiation_id)):
        logging.error(f"      Found an unexpected kind of negotiation identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    18. GET AGREEMENT ID TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the agreement identifier
    endtime = time.time() + timeout_agreement
    count=0
    agreement_id=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations/{negotiation_id}")
        jsonpath_expr = jsonpath_ng.ext.parse('$.contractAgreementId')
        agreement_id=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Agreement ID: {agreement_id}")
        if (not agreement_id or not is_valid_uuid(agreement_id)):
            if (time.time()+1 < endtime):
                logging.info(f"          no agreement identifier found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not agreement_id or not is_valid_uuid(agreement_id)):
        logging.error(f"      Found an unexpected kind of agreement identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    19. START TRANSFER TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    transfer_id=""
    start_transfer_target_graphql_hospital=json.loads(json.dumps(start_transfer_target_graphql_hospital).replace("{{CONTRACT_ID}}", agreement_id))
    logging.debug(f"      start_transfer_target_graphql_hospital as json:\n{json.dumps(start_transfer_target_graphql_hospital, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/transferprocesses", json.dumps(start_transfer_target_graphql_hospital))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    transfer_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Transfer ID: {transfer_id}")
    if (not transfer_id or not is_valid_uuid(transfer_id)):
        logging.error(f"      Found an unexpected kind of transfer identifier: {transfer_id}")
        return ""

    logging.info("")
    logging.info(f"    20. GET ENDPOINT DATA REFERENCE TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the endpoint data reference
    endtime = time.time() + timeout_transfer
    count=0
    data_endpoint=None
    token=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/edrs/{transfer_id}/dataaddress")
        jsonpath_expr = jsonpath_ng.ext.parse('$.endpoint')
        data_endpoint=try_find_value_in_json(jsonpath_expr, response_json)
        jsonpath_expr = jsonpath_ng.ext.parse('$.authorization')
        token=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Endpoint: {data_endpoint} Token: {token[:8] if token else None}...")
        if (not data_endpoint or not token):
            if (time.time()+1 < endtime):
                logging.info(f"          no data endpoint found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not data_endpoint or not token):
        logging.error(f"      Found an unexpected data endpoint: {data_endpoint} with token: {token}")
        return ""

    logging.info("")
    logging.info(f"    21. PUSH THE DATA TO ACCURIDS API PHARMA DATASET UPDATE")
    if stepwise_confirmation: input("Press Enter to continue...")

    sources = f'{{type: FILE, fileName: "{os.path.basename('hospitalHumanBiosample.ttl')}"}},'
    sources = sources[:-1]

    mutation = """
        mutation {
            updateDataset(
                tag: "hospital-1-human-biosample",
                name: "Hospital 1 - Human Biosample",
                description: "",
                datasetSources: [%s]
                append: false
            ) {
                id
            }
        }
    """ % (
        sources
    )

    logging.debug(f"      query: {mutation}")
    response = requests.post(url=data_endpoint, headers={"Authorization": token}, json={"query": mutation})
    logging.debug(f"      Response Headers:\n{pretty_repr(dict(response.headers))}")
    logging.debug(f"      Response Content:\n{pretty_repr(response.content)}")
    if not b'{"errors"' in response.content:
        logging.info("        Dataset upload done.")
    else:
        logging.debug(f"      Updating the dataset failed. Trying to create a new one.")

        mutation = """
            mutation {
                createDataset(
                    tag: "hospital-1-human-biosample",
                    name: "Hospital 1 - Human Biosample",
                    description: "",
                    datasetSources: [%s]
                ) {
                    id
                }
            }
        """ % (
            sources
        )

        logging.debug(f"      query: {mutation}")
        response = requests.post(url=data_endpoint, headers={"Authorization": token}, json={"query": mutation})
        logging.debug(f"      Response Headers:\n{pretty_repr(dict(response.headers))}")
        logging.debug(f"      Response Content:\n{pretty_repr(response.content)}")
        if not b'{"errors"' in response.content:
            logging.info("        Dataset upload done.")
        else:
            logging.error("        Dataset upload failed.")
            return ""


def hospital_patient_collaboration():
    ############################################################
    ##### Hospital Patient Collaboration 
    ############################################################
    global negotiate_contract_source_hospital_patient_collaboration, start_transfer_source_hospital_patient_collaboration, negotiate_contract_target_file_hospital_patient_collaboration, start_transfer_target_file_hospital_patient_collaboration, negotiate_contract_target_graphql_hospital, start_transfer_target_graphql_hospital

    logging.info("")
    logging.info("HOSPITAL PATIENT COLLABORATION")
    logging.info("")
    logging.info("  Download Hospital Patient Collaboration")
    logging.info("")
    logging.info(f"    4. FETCH CATALOG")
    if stepwise_confirmation: input("Press Enter to continue...")
    response_json=call_endpoint(f"{provider_url_and_management_port}/management/v3/catalog/request", json.dumps(fetch_catalog))
    jsonPath = f"$.\"dcat:dataset\"[?id = \"hospitalPatientCollaboration\"].\"odrl:hasPolicy\".\"@id\""
    logging.debug(f"       JSON PATH: {jsonPath}")
    jsonpath_expr = jsonpath_ng.ext.parse(jsonPath)
    dataset_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Dataset ID: {dataset_id}")
    if (not dataset_id or not dataset_id.startswith("MQ")):
        logging.error(f"      Found an unexpected kind of dataset identifier: {dataset_id}")
        return ""

    logging.info("")
    logging.info(f"    5. NEGOTIATE CONTRACT SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    negotiate_contract_source_hospital_patient_collaboration=json.loads(json.dumps(negotiate_contract_source_hospital_patient_collaboration).replace("{{DATASET_ID}}", dataset_id))
    logging.debug(f"      negotiate_contract_source_hospital_patient_collaboration as json:\n{json.dumps(negotiate_contract_source_hospital_patient_collaboration, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations", json.dumps(negotiate_contract_source_hospital_patient_collaboration))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    negotiation_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Negotiation ID: {negotiation_id}")
    if (not negotiation_id or not is_valid_uuid(negotiation_id)):
        logging.error(f"      Found an unexpected kind of negotiation identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    6. GET AGREEMENT ID SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the agreement identifier
    endtime = time.time() + timeout_agreement
    count=0
    agreement_id=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations/{negotiation_id}")
        jsonpath_expr = jsonpath_ng.ext.parse('$.contractAgreementId')
        agreement_id=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Agreement ID: {agreement_id}")
        if (not agreement_id or not is_valid_uuid(agreement_id)):
            if (time.time()+1 < endtime):
                logging.info(f"          no agreement identifier found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not agreement_id or not is_valid_uuid(agreement_id)):
        logging.error(f"      Found an unexpected kind of agreement identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    7. START TRANSFER SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    start_transfer_source_hospital_patient_collaboration=json.loads(json.dumps(start_transfer_source_hospital_patient_collaboration).replace("{{CONTRACT_ID}}", agreement_id))
    logging.debug(f"      start_transfer_source_hospital_patient_collaboration as json:\n{json.dumps(start_transfer_source_hospital_patient_collaboration, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/transferprocesses", json.dumps(start_transfer_source_hospital_patient_collaboration))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    transfer_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Transfer ID: {transfer_id}")
    if (not transfer_id or not is_valid_uuid(transfer_id)):
        logging.error(f"      Found an unexpected kind of transfer identifier: {transfer_id}")
        return ""

    logging.info("")
    logging.info(f"    8. GET ENDPOINT DATA REFERENCE SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the endpoint data reference
    endtime = time.time() + timeout_transfer
    count=0
    data_endpoint=None
    token=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/edrs/{transfer_id}/dataaddress")
        jsonpath_expr = jsonpath_ng.ext.parse('$.endpoint')
        data_endpoint=try_find_value_in_json(jsonpath_expr, response_json)
        jsonpath_expr = jsonpath_ng.ext.parse('$.authorization')
        token=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Endpoint: {data_endpoint} Token: {token[:8] if token else None}...")
        if (not data_endpoint or not token):
            if (time.time()+1 < endtime):
                logging.info(f"          no data endpoint found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not data_endpoint or not token):
        logging.error(f"      Found an unexpected data endpoint: {data_endpoint} with token: {token}")
        return ""

    logging.info("")
    logging.info(f"    9. GET THE DATA FROM ACCURIDS API HOSPITAL")
    if stepwise_confirmation: input("Press Enter to continue...")
    response = requests.get(url=data_endpoint, headers={"Authorization": token, "Accept": "text/turtle"})
    logging.debug(f"      Headers:\n{pretty_repr(dict(response.headers))}")
    logging.debug(f"      Content:\n{pretty_repr(response.content)}")

    if (not response.content or b'' == response.content or b'{"errors":["NOT_AUTHORIZED"]}' == response.content):
        logging.error(f"      File download failed.")
        return ""

    turtle=response.content

    f = open('hospitalPatientCollaboration.ttl', "w", encoding="utf-8")
    f.write(str(turtle, 'utf-8'))
    f.close()

    logging.info("        Download done.")

    if not turtle:
        logging.info("      Empty file. Skip upload.")
        return ""

    if (os.path.isfile('hospitalPatientCollaboration_previous.ttl')):
        previous_turtle = open('hospitalPatientCollaboration_previous.ttl', "rb").read()
        if str(turtle, 'utf-8') == str(previous_turtle, 'utf-8'):
            logging.info("      The downloaded file is the same as before. Skip upload.")
            return ""
        else:
            logging.info("      The downloaded file is different from before.")
            f = open('hospitalPatientCollaboration_previous.ttl', "w", encoding="utf-8")
            f.write(str(turtle, 'utf-8'))
            f.close()
    else:
        logging.info("      This is the first download.")
        f = open('hospitalPatientCollaboration_previous.ttl', "w", encoding="utf-8")
        f.write(str(turtle, 'utf-8'))
        f.close()

    if stepwise_confirmation: input("Press Enter to continue...")

    logging.info("")
    logging.info("  Upload Hospital Patient Collaboration")
    logging.info("")

    logging.info(f"    10. FETCH CATALOG TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    dataset_id=""
    response_json=call_endpoint(f"{provider_url_and_management_port}/management/v3/catalog/request", json.dumps(fetch_catalog))
    jsonpath_expr = jsonpath_ng.ext.parse(f"$.\"dcat:dataset\"[?id = \"hospitalPatientCollaborationFile\"].\"odrl:hasPolicy\".\"@id\"")
    dataset_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Dataset ID: {dataset_id}")
    if (not dataset_id or not dataset_id.startswith("MQ")):
        logging.error(f"      Found an unexpected kind of dataset identifier: {dataset_id}")
        return ""

    logging.info("")
    logging.info(f"    11. NEGOTIATE CONTRACT TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    negotiation_id=""
    negotiate_contract_target_file_hospital_patient_collaboration=json.loads(json.dumps(negotiate_contract_target_file_hospital_patient_collaboration).replace("{{DATASET_ID}}", dataset_id))
    logging.debug(f"      negotiate_contract_target_file_hospital_patient_collaboration as json:\n{json.dumps(negotiate_contract_target_file_hospital_patient_collaboration, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations", json.dumps(negotiate_contract_target_file_hospital_patient_collaboration))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    negotiation_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Negotiation ID: {negotiation_id}")
    if (not negotiation_id or not is_valid_uuid(negotiation_id)):
        logging.error(f"      Found an unexpected kind of negotiation identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    12. GET AGREEMENT ID TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the agreement identifier
    endtime = time.time() + timeout_agreement
    count=0
    agreement_id=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations/{negotiation_id}")
        jsonpath_expr = jsonpath_ng.ext.parse('$.contractAgreementId')
        agreement_id=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Agreement ID: {agreement_id}")
        if (not agreement_id or not is_valid_uuid(agreement_id)):
            if (time.time()+1 < endtime):
                logging.info(f"          no agreement identifier found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not agreement_id or not is_valid_uuid(agreement_id)):
        logging.error(f"      Found an unexpected kind of agreement identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    13. START TRANSFER TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    transfer_id=""
    start_transfer_target_file_hospital_patient_collaboration=json.loads(json.dumps(start_transfer_target_file_hospital_patient_collaboration).replace("{{CONTRACT_ID}}", agreement_id))
    logging.debug(f"      start_transfer_target_file_hospital_patient_collaboration as json:\n{json.dumps(start_transfer_target_file_hospital_patient_collaboration, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/transferprocesses", json.dumps(start_transfer_target_file_hospital_patient_collaboration))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    transfer_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Transfer ID: {transfer_id}")
    if (not transfer_id or not is_valid_uuid(transfer_id)):
        logging.error(f"      Found an unexpected kind of transfer identifier: {transfer_id}")
        return ""

    logging.info("")
    logging.info(f"    14. GET ENDPOINT DATA REFERENCE TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the endpoint data reference
    endtime = time.time() + timeout_transfer
    count=0
    data_endpoint=None
    token=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/edrs/{transfer_id}/dataaddress")
        jsonpath_expr = jsonpath_ng.ext.parse('$.endpoint')
        data_endpoint=try_find_value_in_json(jsonpath_expr, response_json)
        jsonpath_expr = jsonpath_ng.ext.parse('$.authorization')
        token=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Endpoint: {data_endpoint} Token: {token[:8] if token else None}...")
        if (not data_endpoint or not token):
            if (time.time()+1 < endtime):
                logging.info(f"          no data endpoint found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not data_endpoint or not token):
        logging.error(f"      Found an unexpected data endpoint: {data_endpoint} with token: {token}")
        return ""

    logging.info("")
    logging.info(f"    15. PUSH THE DATA TO ACCURIDS API PHARMA FILE UPLOAD")
    if stepwise_confirmation: input("Press Enter to continue...")

    #FILE MULTIPART
    boundary = "---------888888888"
    file_content = open('hospitalPatientCollaboration.ttl', "rb").read()
    body = f"""\r\n\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"upload\"; filename=\"hospitalPatientCollaboration.ttl\"\r\nContent-Type: application/octet-stream\r\n\r\n{file_content.decode("utf-8")}\r\n--{boundary}--\r\n"""

    logging.debug(f"      Body:\n|START|{body}|END|")
    content_length=str(len(body))
    logging.debug(f"      Content-Length: {content_length}")

    # Headers
    headers = {
        "Authorization": token,
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": content_length
    }
    logging.debug(f"      Request Headers:\n{headers}")

    response = requests.post(url=data_endpoint, headers={"Authorization": token, "Content-Type": f"multipart/form-data; boundary={boundary}", "Content-Length": f"{content_length}" }, data=body)

    logging.debug(f"      Response Headers:\n{pretty_repr(dict(response.headers))}")
    logging.debug(f"      Response Content:\n{pretty_repr(response.content)}")

    if (not response.content or not b'success' in response.content):
        logging.error(f"        File upload failed.")
        return ""
    else:
        logging.debug(f"        File upload complete.")

    logging.info("")
    logging.info(f"    16. FETCH CATALOG TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    dataset_id=""
    response_json=call_endpoint(f"{provider_url_and_management_port}/management/v3/catalog/request", json.dumps(fetch_catalog))
    jsonpath_expr = jsonpath_ng.ext.parse(f"$.\"dcat:dataset\"[?id = \"hospitalGraphql\"].\"odrl:hasPolicy\".\"@id\"")
    dataset_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Dataset ID: {dataset_id}")
    if (not dataset_id or not dataset_id.startswith("MQ")):
        logging.error(f"      Found an unexpected kind of dataset identifier: {dataset_id}")
        return ""

    logging.info("")
    logging.info(f"    17. NEGOTIATE CONTRACT TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    negotiation_id=""
    negotiate_contract_target_graphql_hospital=json.loads(json.dumps(negotiate_contract_target_graphql_hospital).replace("{{DATASET_ID}}", dataset_id))
    logging.debug(f"      negotiate_contract_target_graphql_hospital as json:\n{json.dumps(negotiate_contract_target_graphql_hospital, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations", json.dumps(negotiate_contract_target_graphql_hospital))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    negotiation_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Negotiation ID: {negotiation_id}")
    if (not negotiation_id or not is_valid_uuid(negotiation_id)):
        logging.error(f"      Found an unexpected kind of negotiation identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    18. GET AGREEMENT ID TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the agreement identifier
    endtime = time.time() + timeout_agreement
    count=0
    agreement_id=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations/{negotiation_id}")
        jsonpath_expr = jsonpath_ng.ext.parse('$.contractAgreementId')
        agreement_id=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Agreement ID: {agreement_id}")
        if (not agreement_id or not is_valid_uuid(agreement_id)):
            if (time.time()+1 < endtime):
                logging.info(f"          no agreement identifier found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not agreement_id or not is_valid_uuid(agreement_id)):
        logging.error(f"      Found an unexpected kind of agreement identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    19. START TRANSFER TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    transfer_id=""
    start_transfer_target_graphql_hospital=json.loads(json.dumps(start_transfer_target_graphql_hospital).replace("{{CONTRACT_ID}}", agreement_id))
    logging.debug(f"      start_transfer_target_graphql_hospital as json:\n{json.dumps(start_transfer_target_graphql_hospital, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/transferprocesses", json.dumps(start_transfer_target_graphql_hospital))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    transfer_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Transfer ID: {transfer_id}")
    if (not transfer_id or not is_valid_uuid(transfer_id)):
        logging.error(f"      Found an unexpected kind of transfer identifier: {transfer_id}")
        return ""

    logging.info("")
    logging.info(f"    20. GET ENDPOINT DATA REFERENCE TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the endpoint data reference
    endtime = time.time() + timeout_transfer
    count=0
    data_endpoint=None
    token=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/edrs/{transfer_id}/dataaddress")
        jsonpath_expr = jsonpath_ng.ext.parse('$.endpoint')
        data_endpoint=try_find_value_in_json(jsonpath_expr, response_json)
        jsonpath_expr = jsonpath_ng.ext.parse('$.authorization')
        token=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Endpoint: {data_endpoint} Token: {token[:8] if token else None}...")
        if (not data_endpoint or not token):
            if (time.time()+1 < endtime):
                logging.info(f"          no data endpoint found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not data_endpoint or not token):
        logging.error(f"      Found an unexpected data endpoint: {data_endpoint} with token: {token}")
        return ""

    logging.info("")
    logging.info(f"    21. PUSH THE DATA TO ACCURIDS API PHARMA DATASET UPDATE")
    if stepwise_confirmation: input("Press Enter to continue...")

    sources = f'{{type: FILE, fileName: "{os.path.basename('hospitalPatientCollaboration.ttl')}"}},'
    sources = sources[:-1]

    mutation = """
        mutation {
            updateDataset(
                tag: "hospital-1-patient-collaboration",
                name: "Hospital 1 - Patient Collaboration",
                description: "",
                datasetSources: [%s]
                append: false
            ) {
                id
            }
        }
    """ % (
        sources
    )

    logging.debug(f"      query: {mutation}")
    response = requests.post(url=data_endpoint, headers={"Authorization": token}, json={"query": mutation})
    logging.debug(f"      Response Headers:\n{pretty_repr(dict(response.headers))}")
    logging.debug(f"      Response Content:\n{pretty_repr(response.content)}")
    if not b'{"errors"' in response.content:
        logging.info("        Dataset upload done.")
    else:
        logging.debug(f"      Updating the dataset failed. Trying to create a new one.")

        mutation = """
            mutation {
                createDataset(
                    tag: "hospital-1-patient-collaboration",
                    name: "Hospital 1 - Patient Collaboration",
                    description: "",
                    datasetSources: [%s]
                ) {
                    id
                }
            }
        """ % (
            sources
        )

        logging.debug(f"      query: {mutation}")
        response = requests.post(url=data_endpoint, headers={"Authorization": token}, json={"query": mutation})
        logging.debug(f"      Response Headers:\n{pretty_repr(dict(response.headers))}")
        logging.debug(f"      Response Content:\n{pretty_repr(response.content)}")
        if not b'{"errors"' in response.content:
            logging.info("        Dataset upload done.")
        else:
            logging.error("        Dataset upload failed.")
            return ""

def pharma_reference_data():
    ############################################################
    ##### Pharma Reference Data
    ############################################################
    global negotiate_contract_source_pharma_reference_data, start_transfer_source_pharma_reference_data, negotiate_contract_target_file_pharma_reference_data, start_transfer_target_file_pharma_reference_data, negotiate_contract_target_graphql_pharma, start_transfer_target_graphql_pharma
    
    logging.info("")
    logging.info("PHARMA REFERENCE DATA")
    logging.info("")
    logging.info("  Download Pharma Reference Data")
    logging.info("")
    logging.info(f"    4. FETCH CATALOG")
    if stepwise_confirmation: input("Press Enter to continue...")
    response_json=call_endpoint(f"{provider_url_and_management_port}/management/v3/catalog/request", json.dumps(fetch_catalog))
    jsonPath = f"$.\"dcat:dataset\"[?id = \"pharmaReferenceData\"].\"odrl:hasPolicy\".\"@id\""
    logging.debug(f"       JSON PATH: {jsonPath}")
    jsonpath_expr = jsonpath_ng.ext.parse(jsonPath)
    dataset_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Dataset ID: {dataset_id}")
    if (not dataset_id or not dataset_id.startswith("MQ")):
        logging.error(f"      Found an unexpected kind of dataset identifier: {dataset_id}")
        return ""

    logging.info("")
    logging.info(f"    5. NEGOTIATE CONTRACT SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    negotiate_contract_source_pharma_reference_data=json.loads(json.dumps(negotiate_contract_source_pharma_reference_data).replace("{{DATASET_ID}}", dataset_id))
    logging.debug(f"      negotiate_contract_source_pharma_reference_data as json:\n{json.dumps(negotiate_contract_source_pharma_reference_data, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations", json.dumps(negotiate_contract_source_pharma_reference_data))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    negotiation_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Negotiation ID: {negotiation_id}")
    if (not negotiation_id or not is_valid_uuid(negotiation_id)):
        logging.error(f"      Found an unexpected kind of negotiation identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    6. GET AGREEMENT ID SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the agreement identifier
    endtime = time.time() + timeout_agreement
    count=0
    agreement_id=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations/{negotiation_id}")
        jsonpath_expr = jsonpath_ng.ext.parse('$.contractAgreementId')
        agreement_id=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Agreement ID: {agreement_id}")
        if (not agreement_id or not is_valid_uuid(agreement_id)):
            if (time.time()+1 < endtime):
                logging.info(f"          no agreement identifier found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not agreement_id or not is_valid_uuid(agreement_id)):
        logging.error(f"      Found an unexpected kind of agreement identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    7. START TRANSFER SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    start_transfer_source_pharma_reference_data=json.loads(json.dumps(start_transfer_source_pharma_reference_data).replace("{{CONTRACT_ID}}", agreement_id))
    logging.debug(f"      start_transfer_source_pharma_reference_data as json:\n{json.dumps(start_transfer_source_pharma_reference_data, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/transferprocesses", json.dumps(start_transfer_source_pharma_reference_data))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    transfer_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Transfer ID: {transfer_id}")
    if (not transfer_id or not is_valid_uuid(transfer_id)):
        logging.error(f"      Found an unexpected kind of transfer identifier: {transfer_id}")
        return ""

    logging.info("")
    logging.info(f"    8. GET ENDPOINT DATA REFERENCE SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the endpoint data reference
    endtime = time.time() + timeout_transfer
    count=0
    data_endpoint=None
    token=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/edrs/{transfer_id}/dataaddress")
        jsonpath_expr = jsonpath_ng.ext.parse('$.endpoint')
        data_endpoint=try_find_value_in_json(jsonpath_expr, response_json)
        jsonpath_expr = jsonpath_ng.ext.parse('$.authorization')
        token=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Endpoint: {data_endpoint} Token: {token[:8] if token else None}...")
        if (not data_endpoint or not token):
            if (time.time()+1 < endtime):
                logging.info(f"          no data endpoint found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not data_endpoint or not token):
        logging.error(f"      Found an unexpected data endpoint: {data_endpoint} with token: {token}")
        return ""

    logging.info("")
    logging.info(f"    9. GET THE DATA FROM ACCURIDS API PHARMA")
    if stepwise_confirmation: input("Press Enter to continue...")
    response = requests.get(url=data_endpoint, headers={"Authorization": token, "Accept": "text/turtle"})
    logging.debug(f"      Headers:\n{pretty_repr(dict(response.headers))}")
    logging.debug(f"      Content:\n{pretty_repr(response.content)}")

    if (not response.content or b'' == response.content or b'{"errors":["NOT_AUTHORIZED"]}' == response.content):
        logging.error(f"      File download failed.")
        return ""

    turtle=response.content

    f = open('pharmaReferenceData.ttl', "w", encoding="utf-8")
    f.write(str(turtle, 'utf-8'))
    f.close()

    logging.info("        Download done.")

    if not turtle:
        logging.info("      Empty file. Skip upload.")
        return ""

    if (os.path.isfile('pharmaReferenceData_previous.ttl')):
        previous_turtle = open('pharmaReferenceData_previous.ttl', "rb").read()
        if str(turtle, 'utf-8') == str(previous_turtle, 'utf-8'):
            logging.info("      The downloaded file is the same as before. Skip upload.")
            return ""
        else:
            logging.info("      The downloaded file is different from before.")
            f = open('pharmaReferenceData_previous.ttl', "w", encoding="utf-8")
            f.write(str(turtle, 'utf-8'))
            f.close()
    else:
        logging.info("      This is the first download.")
        f = open('pharmaReferenceData_previous.ttl', "w", encoding="utf-8")
        f.write(str(turtle, 'utf-8'))
        f.close()

    if stepwise_confirmation: input("Press Enter to continue...")

    logging.info("")
    logging.info("  Upload Pharma Reference Data")
    logging.info("")

    logging.info(f"    10. FETCH CATALOG TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    dataset_id=""
    response_json=call_endpoint(f"{provider_url_and_management_port}/management/v3/catalog/request", json.dumps(fetch_catalog))
    jsonpath_expr = jsonpath_ng.ext.parse(f"$.\"dcat:dataset\"[?id = \"pharmaReferenceDataFile\"].\"odrl:hasPolicy\".\"@id\"")
    dataset_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Dataset ID: {dataset_id}")
    if (not dataset_id or not dataset_id.startswith("MQ")):
        logging.error(f"      Found an unexpected kind of dataset identifier: {dataset_id}")
        return ""

    logging.info("")
    logging.info(f"    11. NEGOTIATE CONTRACT TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    negotiation_id=""
    negotiate_contract_target_file_pharma_reference_data=json.loads(json.dumps(negotiate_contract_target_file_pharma_reference_data).replace("{{DATASET_ID}}", dataset_id))
    logging.debug(f"      negotiate_contract_target_file_pharma_reference_data as json:\n{json.dumps(negotiate_contract_target_file_pharma_reference_data, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations", json.dumps(negotiate_contract_target_file_pharma_reference_data))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    negotiation_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Negotiation ID: {negotiation_id}")
    if (not negotiation_id or not is_valid_uuid(negotiation_id)):
        logging.error(f"      Found an unexpected kind of negotiation identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    12. GET AGREEMENT ID TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the agreement identifier
    endtime = time.time() + timeout_agreement
    count=0
    agreement_id=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations/{negotiation_id}")
        jsonpath_expr = jsonpath_ng.ext.parse('$.contractAgreementId')
        agreement_id=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Agreement ID: {agreement_id}")
        if (not agreement_id or not is_valid_uuid(agreement_id)):
            if (time.time()+1 < endtime):
                logging.info(f"          no agreement identifier found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not agreement_id or not is_valid_uuid(agreement_id)):
        logging.error(f"      Found an unexpected kind of agreement identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    13. START TRANSFER TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    transfer_id=""
    start_transfer_target_file_pharma_reference_data=json.loads(json.dumps(start_transfer_target_file_pharma_reference_data).replace("{{CONTRACT_ID}}", agreement_id))
    logging.debug(f"      start_transfer_target_file_pharma_reference_data as json:\n{json.dumps(start_transfer_target_file_pharma_reference_data, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/transferprocesses", json.dumps(start_transfer_target_file_pharma_reference_data))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    transfer_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Transfer ID: {transfer_id}")
    if (not transfer_id or not is_valid_uuid(transfer_id)):
        logging.error(f"      Found an unexpected kind of transfer identifier: {transfer_id}")
        return ""

    logging.info("")
    logging.info(f"    14. GET ENDPOINT DATA REFERENCE TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the endpoint data reference
    endtime = time.time() + timeout_transfer
    count=0
    data_endpoint=None
    token=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/edrs/{transfer_id}/dataaddress")
        jsonpath_expr = jsonpath_ng.ext.parse('$.endpoint')
        data_endpoint=try_find_value_in_json(jsonpath_expr, response_json)
        jsonpath_expr = jsonpath_ng.ext.parse('$.authorization')
        token=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Endpoint: {data_endpoint} Token: {token[:8] if token else None}...")
        if (not data_endpoint or not token):
            if (time.time()+1 < endtime):
                logging.info(f"          no data endpoint found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not data_endpoint or not token):
        logging.error(f"      Found an unexpected data endpoint: {data_endpoint} with token: {token}")
        return ""

    logging.info("")
    logging.info(f"    15. PUSH THE DATA TO ACCURIDS API HOSPITAL FILE UPLOAD")
    if stepwise_confirmation: input("Press Enter to continue...")

    #FILE MULTIPART
    boundary = "---------888888888"
    file_content = open('pharmaReferenceData.ttl', "rb").read()
    body = f"""\r\n\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"upload\"; filename=\"pharmaReferenceData.ttl\"\r\nContent-Type: application/octet-stream\r\n\r\n{file_content.decode("utf-8")}\r\n--{boundary}--\r\n"""

    logging.debug(f"      Body:\n|START|{body}|END|")
    content_length=str(len(body))
    logging.debug(f"      Content-Length: {content_length}")

    # Headers
    headers = {
        "Authorization": token,
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": content_length
    }
    logging.debug(f"      Request Headers:\n{headers}")

    response = requests.post(url=data_endpoint, headers={"Authorization": token, "Content-Type": f"multipart/form-data; boundary={boundary}", "Content-Length": f"{content_length}" }, data=body)

    logging.debug(f"      Response Headers:\n{pretty_repr(dict(response.headers))}")
    logging.debug(f"      Response Content:\n{pretty_repr(response.content)}")

    if (not response.content or not b'success' in response.content):
        logging.error(f"        File upload failed.")
        return ""
    else:
        logging.debug(f"        File upload complete.")

    logging.info("")
    logging.info(f"    16. FETCH CATALOG TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    dataset_id=""
    response_json=call_endpoint(f"{provider_url_and_management_port}/management/v3/catalog/request", json.dumps(fetch_catalog))
    jsonpath_expr = jsonpath_ng.ext.parse(f"$.\"dcat:dataset\"[?id = \"pharmaGraphql\"].\"odrl:hasPolicy\".\"@id\"")
    dataset_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Dataset ID: {dataset_id}")
    if (not dataset_id or not dataset_id.startswith("MQ")):
        logging.error(f"      Found an unexpected kind of dataset identifier: {dataset_id}")
        return ""

    logging.info("")
    logging.info(f"    17. NEGOTIATE CONTRACT TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    negotiation_id=""
    negotiate_contract_target_graphql_pharma=json.loads(json.dumps(negotiate_contract_target_graphql_pharma).replace("{{DATASET_ID}}", dataset_id))
    logging.debug(f"      negotiate_contract_target_graphql_pharma as json:\n{json.dumps(negotiate_contract_target_graphql_pharma, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations", json.dumps(negotiate_contract_target_graphql_pharma))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    negotiation_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Negotiation ID: {negotiation_id}")
    if (not negotiation_id or not is_valid_uuid(negotiation_id)):
        logging.error(f"      Found an unexpected kind of negotiation identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    18. GET AGREEMENT ID TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the agreement identifier
    endtime = time.time() + timeout_agreement
    count=0
    agreement_id=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations/{negotiation_id}")
        jsonpath_expr = jsonpath_ng.ext.parse('$.contractAgreementId')
        agreement_id=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Agreement ID: {agreement_id}")
        if (not agreement_id or not is_valid_uuid(agreement_id)):
            if (time.time()+1 < endtime):
                logging.info(f"          no agreement identifier found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not agreement_id or not is_valid_uuid(agreement_id)):
        logging.error(f"      Found an unexpected kind of agreement identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    19. START TRANSFER TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    transfer_id=""
    start_transfer_target_graphql_pharma=json.loads(json.dumps(start_transfer_target_graphql_pharma).replace("{{CONTRACT_ID}}", agreement_id))
    logging.debug(f"      start_transfer_target_graphql_pharma as json:\n{json.dumps(start_transfer_target_graphql_pharma, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/transferprocesses", json.dumps(start_transfer_target_graphql_pharma))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    transfer_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Transfer ID: {transfer_id}")
    if (not transfer_id or not is_valid_uuid(transfer_id)):
        logging.error(f"      Found an unexpected kind of transfer identifier: {transfer_id}")
        return ""

    logging.info("")
    logging.info(f"    20. GET ENDPOINT DATA REFERENCE TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the endpoint data reference
    endtime = time.time() + timeout_transfer
    count=0
    data_endpoint=None
    token=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/edrs/{transfer_id}/dataaddress")
        jsonpath_expr = jsonpath_ng.ext.parse('$.endpoint')
        data_endpoint=try_find_value_in_json(jsonpath_expr, response_json)
        jsonpath_expr = jsonpath_ng.ext.parse('$.authorization')
        token=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Endpoint: {data_endpoint} Token: {token[:8] if token else None}...")
        if (not data_endpoint or not token):
            if (time.time()+1 < endtime):
                logging.info(f"          no data endpoint found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not data_endpoint or not token):
        logging.error(f"      Found an unexpected data endpoint: {data_endpoint} with token: {token}")
        return ""

    logging.info("")
    logging.info(f"    21. PUSH THE DATA TO ACCURIDS API HOSPITAL DATASET UPDATE")
    if stepwise_confirmation: input("Press Enter to continue...")

    sources = f'{{type: FILE, fileName: "{os.path.basename('pharmaReferenceData.ttl')}"}},'
    sources = sources[:-1]

    mutation = """
        mutation {
            updateDataset(
                tag: "reference-data",
                name: "Reference Data",
                description: "",
                datasetSources: [%s]
                append: false
            ) {
                id
            }
        }
    """ % (
        sources
    )

    logging.debug(f"      query: {mutation}")
    response = requests.post(url=data_endpoint, headers={"Authorization": token}, json={"query": mutation})
    logging.debug(f"      Response Headers:\n{pretty_repr(dict(response.headers))}")
    logging.debug(f"      Response Content:\n{pretty_repr(response.content)}")
    if not b'{"errors"' in response.content:
        logging.info("        Dataset upload done.")
    else:
        logging.debug(f"      Updating the dataset failed. Trying to create a new one.")

        mutation = """
            mutation {
                createDataset(
                    tag: "reference-data",
                    name: "Reference Data",
                    description: "",
                    datasetSources: [%s]
                ) {
                    id
                }
            }
        """ % (
            sources
        )

        logging.debug(f"      query: {mutation}")
        response = requests.post(url=data_endpoint, headers={"Authorization": token}, json={"query": mutation})
        logging.debug(f"      Response Headers:\n{pretty_repr(dict(response.headers))}")
        logging.debug(f"      Response Content:\n{pretty_repr(response.content)}")
        if not b'{"errors"' in response.content:
            logging.info("        Dataset upload done.")
        else:
            logging.error("        Dataset upload failed.")
            return ""


def pharma_shapes():
    ############################################################
    ##### Pharma Shapes
    ############################################################
    global negotiate_contract_source_pharma_shapes, start_transfer_source_pharma_shapes, negotiate_contract_target_file_pharma_shapes, start_transfer_target_file_pharma_shapes, negotiate_contract_target_graphql_pharma, start_transfer_target_graphql_pharma

    logging.info("")
    logging.info("PHARMA SHAPES")
    logging.info("")
    logging.info("  Download Pharma Shapes")
    logging.info("")
    logging.info(f"    4. FETCH CATALOG")
    if stepwise_confirmation: input("Press Enter to continue...")
    response_json=call_endpoint(f"{provider_url_and_management_port}/management/v3/catalog/request", json.dumps(fetch_catalog))
    jsonPath = f"$.\"dcat:dataset\"[?id = \"pharmaShapes\"].\"odrl:hasPolicy\".\"@id\""
    logging.debug(f"       JSON PATH: {jsonPath}")
    jsonpath_expr = jsonpath_ng.ext.parse(jsonPath)
    dataset_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Dataset ID: {dataset_id}")
    if (not dataset_id or not dataset_id.startswith("MQ")):
        logging.error(f"      Found an unexpected kind of dataset identifier: {dataset_id}")
        return ""

    logging.info("")
    logging.info(f"    5. NEGOTIATE CONTRACT SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    negotiate_contract_source_pharma_shapes=json.loads(json.dumps(negotiate_contract_source_pharma_shapes).replace("{{DATASET_ID}}", dataset_id))
    logging.debug(f"      negotiate_contract_source_pharma_shapes as json:\n{json.dumps(negotiate_contract_source_pharma_shapes, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations", json.dumps(negotiate_contract_source_pharma_shapes))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    negotiation_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Negotiation ID: {negotiation_id}")
    if (not negotiation_id or not is_valid_uuid(negotiation_id)):
        logging.error(f"      Found an unexpected kind of negotiation identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    6. GET AGREEMENT ID SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the agreement identifier
    endtime = time.time() + timeout_agreement
    count=0
    agreement_id=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations/{negotiation_id}")
        jsonpath_expr = jsonpath_ng.ext.parse('$.contractAgreementId')
        agreement_id=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Agreement ID: {agreement_id}")
        if (not agreement_id or not is_valid_uuid(agreement_id)):
            if (time.time()+1 < endtime):
                logging.info(f"          no agreement identifier found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not agreement_id or not is_valid_uuid(agreement_id)):
        logging.error(f"      Found an unexpected kind of agreement identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    7. START TRANSFER SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    start_transfer_source_pharma_shapes=json.loads(json.dumps(start_transfer_source_pharma_shapes).replace("{{CONTRACT_ID}}", agreement_id))
    logging.debug(f"      start_transfer_source_pharma_shapes as json:\n{json.dumps(start_transfer_source_pharma_shapes, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/transferprocesses", json.dumps(start_transfer_source_pharma_shapes))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    transfer_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Transfer ID: {transfer_id}")
    if (not transfer_id or not is_valid_uuid(transfer_id)):
        logging.error(f"      Found an unexpected kind of transfer identifier: {transfer_id}")
        return ""

    logging.info("")
    logging.info(f"    8. GET ENDPOINT DATA REFERENCE SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the endpoint data reference
    endtime = time.time() + timeout_transfer
    count=0
    data_endpoint=None
    token=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/edrs/{transfer_id}/dataaddress")
        jsonpath_expr = jsonpath_ng.ext.parse('$.endpoint')
        data_endpoint=try_find_value_in_json(jsonpath_expr, response_json)
        jsonpath_expr = jsonpath_ng.ext.parse('$.authorization')
        token=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Endpoint: {data_endpoint} Token: {token[:8] if token else None}...")
        if (not data_endpoint or not token):
            if (time.time()+1 < endtime):
                logging.info(f"          no data endpoint found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not data_endpoint or not token):
        logging.error(f"      Found an unexpected data endpoint: {data_endpoint} with token: {token}")
        return ""

    logging.info("")
    logging.info(f"    9. GET THE DATA FROM ACCURIDS API PHARMA")
    if stepwise_confirmation: input("Press Enter to continue...")
    response = requests.get(url=data_endpoint, headers={"Authorization": token, "Accept": "text/turtle"})
    logging.debug(f"      Headers:\n{pretty_repr(dict(response.headers))}")
    logging.debug(f"      Content:\n{pretty_repr(response.content)}")

    if (not response.content or b'' == response.content or b'{"errors":["NOT_AUTHORIZED"]}' == response.content):
        logging.error(f"      File download failed.")
        return ""

    turtle=response.content

    f = open('pharmaShapes.ttl', "w", encoding="utf-8")
    f.write(str(turtle, 'utf-8'))
    f.close()

    logging.info("        Download done.")

    if not turtle:
        logging.info("      Empty file. Skip upload.")
        return ""

    if (os.path.isfile('pharmaShapes_previous.ttl')):
        previous_turtle = open('pharmaShapes_previous.ttl', "rb").read()
        if str(turtle, 'utf-8') == str(previous_turtle, 'utf-8'):
            logging.info("      The downloaded file is the same as before. Skip upload.")
            return ""
        else:
            logging.info("      The downloaded file is different from before.")
            f = open('pharmaShapes_previous.ttl', "w", encoding="utf-8")
            f.write(str(turtle, 'utf-8'))
            f.close()
    else:
        logging.info("      This is the first download.")
        f = open('pharmaShapes_previous.ttl', "w", encoding="utf-8")
        f.write(str(turtle, 'utf-8'))
        f.close()

    if stepwise_confirmation: input("Press Enter to continue...")

    logging.info("")
    logging.info("  Upload Pharma Shapes")
    logging.info("")

    logging.info(f"    10. FETCH CATALOG TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    dataset_id=""
    response_json=call_endpoint(f"{provider_url_and_management_port}/management/v3/catalog/request", json.dumps(fetch_catalog))
    jsonpath_expr = jsonpath_ng.ext.parse(f"$.\"dcat:dataset\"[?id = \"pharmaShapesFile\"].\"odrl:hasPolicy\".\"@id\"")
    dataset_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Dataset ID: {dataset_id}")
    if (not dataset_id or not dataset_id.startswith("MQ")):
        logging.error(f"      Found an unexpected kind of dataset identifier: {dataset_id}")
        return ""

    logging.info("")
    logging.info(f"    11. NEGOTIATE CONTRACT TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    negotiation_id=""
    negotiate_contract_target_file_pharma_shapes=json.loads(json.dumps(negotiate_contract_target_file_pharma_shapes).replace("{{DATASET_ID}}", dataset_id))
    logging.debug(f"      negotiate_contract_target_file_pharma_shapes as json:\n{json.dumps(negotiate_contract_target_file_pharma_shapes, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations", json.dumps(negotiate_contract_target_file_pharma_shapes))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    negotiation_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Negotiation ID: {negotiation_id}")
    if (not negotiation_id or not is_valid_uuid(negotiation_id)):
        logging.error(f"      Found an unexpected kind of negotiation identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    12. GET AGREEMENT ID TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the agreement identifier
    endtime = time.time() + timeout_agreement
    count=0
    agreement_id=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations/{negotiation_id}")
        jsonpath_expr = jsonpath_ng.ext.parse('$.contractAgreementId')
        agreement_id=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Agreement ID: {agreement_id}")
        if (not agreement_id or not is_valid_uuid(agreement_id)):
            if (time.time()+1 < endtime):
                logging.info(f"          no agreement identifier found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not agreement_id or not is_valid_uuid(agreement_id)):
        logging.error(f"      Found an unexpected kind of agreement identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    13. START TRANSFER TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    transfer_id=""
    start_transfer_target_file_pharma_shapes=json.loads(json.dumps(start_transfer_target_file_pharma_shapes).replace("{{CONTRACT_ID}}", agreement_id))
    logging.debug(f"      start_transfer_target_file_pharma_shapes as json:\n{json.dumps(start_transfer_target_file_pharma_shapes, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/transferprocesses", json.dumps(start_transfer_target_file_pharma_shapes))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    transfer_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Transfer ID: {transfer_id}")
    if (not transfer_id or not is_valid_uuid(transfer_id)):
        logging.error(f"      Found an unexpected kind of transfer identifier: {transfer_id}")
        return ""

    logging.info("")
    logging.info(f"    14. GET ENDPOINT DATA REFERENCE TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the endpoint data reference
    endtime = time.time() + timeout_transfer
    count=0
    data_endpoint=None
    token=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/edrs/{transfer_id}/dataaddress")
        jsonpath_expr = jsonpath_ng.ext.parse('$.endpoint')
        data_endpoint=try_find_value_in_json(jsonpath_expr, response_json)
        jsonpath_expr = jsonpath_ng.ext.parse('$.authorization')
        token=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Endpoint: {data_endpoint} Token: {token[:8] if token else None}...")
        if (not data_endpoint or not token):
            if (time.time()+1 < endtime):
                logging.info(f"          no data endpoint found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not data_endpoint or not token):
        logging.error(f"      Found an unexpected data endpoint: {data_endpoint} with token: {token}")
        return ""

    logging.info("")
    logging.info(f"    15. PUSH THE DATA TO ACCURIDS API HOSPITAL FILE UPLOAD")
    if stepwise_confirmation: input("Press Enter to continue...")

    #FILE MULTIPART
    boundary = "---------888888888"
    file_content = open('pharmaShapes.ttl', "rb").read()
    body = f"""\r\n\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"upload\"; filename=\"pharmaShapes.ttl\"\r\nContent-Type: application/octet-stream\r\n\r\n{file_content.decode("utf-8")}\r\n--{boundary}--\r\n"""

    logging.debug(f"      Body:\n|START|{body}|END|")
    content_length=str(len(body))
    logging.debug(f"      Content-Length: {content_length}")

    # Headers
    headers = {
        "Authorization": token,
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": content_length
    }
    logging.debug(f"      Request Headers:\n{headers}")

    response = requests.post(url=data_endpoint, headers={"Authorization": token, "Content-Type": f"multipart/form-data; boundary={boundary}", "Content-Length": f"{content_length}" }, data=body)

    logging.debug(f"      Response Headers:\n{pretty_repr(dict(response.headers))}")
    logging.debug(f"      Response Content:\n{pretty_repr(response.content)}")

    if (not response.content or not b'success' in response.content):
        logging.error(f"        File upload failed.")
        return ""
    else:
        logging.debug(f"        File upload complete.")

    logging.info("")
    logging.info(f"    16. FETCH CATALOG TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    dataset_id=""
    response_json=call_endpoint(f"{provider_url_and_management_port}/management/v3/catalog/request", json.dumps(fetch_catalog))
    jsonpath_expr = jsonpath_ng.ext.parse(f"$.\"dcat:dataset\"[?id = \"pharmaGraphql\"].\"odrl:hasPolicy\".\"@id\"")
    dataset_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Dataset ID: {dataset_id}")
    if (not dataset_id or not dataset_id.startswith("MQ")):
        logging.error(f"      Found an unexpected kind of dataset identifier: {dataset_id}")
        return ""

    logging.info("")
    logging.info(f"    17. NEGOTIATE CONTRACT TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    negotiation_id=""
    negotiate_contract_target_graphql_pharma=json.loads(json.dumps(negotiate_contract_target_graphql_pharma).replace("{{DATASET_ID}}", dataset_id))
    logging.debug(f"      negotiate_contract_target_graphql_pharma as json:\n{json.dumps(negotiate_contract_target_graphql_pharma, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations", json.dumps(negotiate_contract_target_graphql_pharma))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    negotiation_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Negotiation ID: {negotiation_id}")
    if (not negotiation_id or not is_valid_uuid(negotiation_id)):
        logging.error(f"      Found an unexpected kind of negotiation identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    18. GET AGREEMENT ID TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the agreement identifier
    endtime = time.time() + timeout_agreement
    count=0
    agreement_id=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations/{negotiation_id}")
        jsonpath_expr = jsonpath_ng.ext.parse('$.contractAgreementId')
        agreement_id=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Agreement ID: {agreement_id}")
        if (not agreement_id or not is_valid_uuid(agreement_id)):
            if (time.time()+1 < endtime):
                logging.info(f"          no agreement identifier found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not agreement_id or not is_valid_uuid(agreement_id)):
        logging.error(f"      Found an unexpected kind of agreement identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    19. START TRANSFER TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    transfer_id=""
    start_transfer_target_graphql_pharma=json.loads(json.dumps(start_transfer_target_graphql_pharma).replace("{{CONTRACT_ID}}", agreement_id))
    logging.debug(f"      start_transfer_target_graphql_pharma as json:\n{json.dumps(start_transfer_target_graphql_pharma, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/transferprocesses", json.dumps(start_transfer_target_graphql_pharma))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    transfer_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Transfer ID: {transfer_id}")
    if (not transfer_id or not is_valid_uuid(transfer_id)):
        logging.error(f"      Found an unexpected kind of transfer identifier: {transfer_id}")
        return ""

    logging.info("")
    logging.info(f"    20. GET ENDPOINT DATA REFERENCE TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the endpoint data reference
    endtime = time.time() + timeout_transfer
    count=0
    data_endpoint=None
    token=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/edrs/{transfer_id}/dataaddress")
        jsonpath_expr = jsonpath_ng.ext.parse('$.endpoint')
        data_endpoint=try_find_value_in_json(jsonpath_expr, response_json)
        jsonpath_expr = jsonpath_ng.ext.parse('$.authorization')
        token=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Endpoint: {data_endpoint} Token: {token[:8] if token else None}...")
        if (not data_endpoint or not token):
            if (time.time()+1 < endtime):
                logging.info(f"          no data endpoint found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not data_endpoint or not token):
        logging.error(f"      Found an unexpected data endpoint: {data_endpoint} with token: {token}")
        return ""

    logging.info("")
    logging.info(f"    21. PUSH THE DATA TO ACCURIDS API HOSPITAL DATASET UPDATE")
    if stepwise_confirmation: input("Press Enter to continue...")

    sources = f'{{type: FILE, fileName: "{os.path.basename('pharmaShapes.ttl')}"}},'
    sources = sources[:-1]

    mutation = """
        mutation {
            updateDataset(
                tag: "constraints",
                name: "constraints",
                description: "",
                datasetSources: [%s]
                append: false
            ) {
                id
            }
        }
    """ % (
        sources
    )

    logging.debug(f"      query: {mutation}")
    response = requests.post(url=data_endpoint, headers={"Authorization": token}, json={"query": mutation})
    logging.debug(f"      Response Headers:\n{pretty_repr(dict(response.headers))}")
    logging.debug(f"      Response Content:\n{pretty_repr(response.content)}")
    if not b'{"errors"' in response.content:
        logging.info("        Dataset upload done.")
    else:
        logging.debug(f"      Updating the dataset failed. Trying to create a new one.")

        mutation = """
            mutation {
                createDataset(
                    tag: "constraints",
                    name: "constraints",
                    description: "",
                    datasetSources: [%s]
                ) {
                    id
                }
            }
        """ % (
            sources
        )

        logging.debug(f"      query: {mutation}")
        response = requests.post(url=data_endpoint, headers={"Authorization": token}, json={"query": mutation})
        logging.debug(f"      Response Headers:\n{pretty_repr(dict(response.headers))}")
        logging.debug(f"      Response Content:\n{pretty_repr(response.content)}")
        if not b'{"errors"' in response.content:
            logging.info("        Dataset upload done.")
        else:
            logging.error("        Dataset upload failed.")
            return ""


def pharma_trial():
    ############################################################
    ##### Pharma Trial
    ############################################################
    global negotiate_contract_source_pharma_trial, start_transfer_source_pharma_trial, negotiate_contract_target_file_pharma_trial, start_transfer_target_file_pharma_trial, negotiate_contract_target_graphql_pharma, start_transfer_target_graphql_pharma

    logging.info("")
    logging.info("PHARMA TRIAL")
    logging.info("")
    logging.info("  Download Pharma Trial")
    logging.info("")
    logging.info(f"    4. FETCH CATALOG")
    if stepwise_confirmation: input("Press Enter to continue...")
    response_json=call_endpoint(f"{provider_url_and_management_port}/management/v3/catalog/request", json.dumps(fetch_catalog))
    jsonPath = f"$.\"dcat:dataset\"[?id = \"pharmaTrial\"].\"odrl:hasPolicy\".\"@id\""
    logging.debug(f"       JSON PATH: {jsonPath}")
    jsonpath_expr = jsonpath_ng.ext.parse(jsonPath)
    dataset_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Dataset ID: {dataset_id}")
    if (not dataset_id or not dataset_id.startswith("MQ")):
        logging.error(f"      Found an unexpected kind of dataset identifier: {dataset_id}")
        return ""

    logging.info("")
    logging.info(f"    5. NEGOTIATE CONTRACT SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    negotiate_contract_source_pharma_trial=json.loads(json.dumps(negotiate_contract_source_pharma_trial).replace("{{DATASET_ID}}", dataset_id))
    logging.debug(f"      negotiate_contract_source_pharma_trial as json:\n{json.dumps(negotiate_contract_source_pharma_trial, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations", json.dumps(negotiate_contract_source_pharma_trial))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    negotiation_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Negotiation ID: {negotiation_id}")
    if (not negotiation_id or not is_valid_uuid(negotiation_id)):
        logging.error(f"      Found an unexpected kind of negotiation identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    6. GET AGREEMENT ID SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the agreement identifier
    endtime = time.time() + timeout_agreement
    count=0
    agreement_id=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations/{negotiation_id}")
        jsonpath_expr = jsonpath_ng.ext.parse('$.contractAgreementId')
        agreement_id=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Agreement ID: {agreement_id}")
        if (not agreement_id or not is_valid_uuid(agreement_id)):
            if (time.time()+1 < endtime):
                logging.info(f"          no agreement identifier found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not agreement_id or not is_valid_uuid(agreement_id)):
        logging.error(f"      Found an unexpected kind of agreement identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    7. START TRANSFER SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    start_transfer_source_pharma_trial=json.loads(json.dumps(start_transfer_source_pharma_trial).replace("{{CONTRACT_ID}}", agreement_id))
    logging.debug(f"      start_transfer_source_pharma_trial as json:\n{json.dumps(start_transfer_source_pharma_trial, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/transferprocesses", json.dumps(start_transfer_source_pharma_trial))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    transfer_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Transfer ID: {transfer_id}")
    if (not transfer_id or not is_valid_uuid(transfer_id)):
        logging.error(f"      Found an unexpected kind of transfer identifier: {transfer_id}")
        return ""

    logging.info("")
    logging.info(f"    8. GET ENDPOINT DATA REFERENCE SOURCE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the endpoint data reference
    endtime = time.time() + timeout_transfer
    count=0
    data_endpoint=None
    token=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/edrs/{transfer_id}/dataaddress")
        jsonpath_expr = jsonpath_ng.ext.parse('$.endpoint')
        data_endpoint=try_find_value_in_json(jsonpath_expr, response_json)
        jsonpath_expr = jsonpath_ng.ext.parse('$.authorization')
        token=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Endpoint: {data_endpoint} Token: {token[:8] if token else None}...")
        if (not data_endpoint or not token):
            if (time.time()+1 < endtime):
                logging.info(f"          no data endpoint found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not data_endpoint or not token):
        logging.error(f"      Found an unexpected data endpoint: {data_endpoint} with token: {token}")
        return ""

    logging.info("")
    logging.info(f"    9. GET THE DATA FROM ACCURIDS API PHARMA")
    if stepwise_confirmation: input("Press Enter to continue...")
    response = requests.get(url=data_endpoint, headers={"Authorization": token, "Accept": "text/turtle"})
    logging.debug(f"      Headers:\n{pretty_repr(dict(response.headers))}")
    logging.debug(f"      Content:\n{pretty_repr(response.content)}")

    if (not response.content or b'' == response.content or b'{"errors":["NOT_AUTHORIZED"]}' == response.content):
        logging.error(f"      File download failed.")
        return ""

    turtle=response.content

    f = open('pharmaTrial.ttl', "w", encoding="utf-8")
    f.write(str(turtle, 'utf-8'))
    f.close()

    logging.info("        Download done.")

    if not turtle:
        logging.info("      Empty file. Skip upload.")
        return ""

    if (os.path.isfile('pharmaTrial_previous.ttl')):
        previous_turtle = open('pharmaTrial_previous.ttl', "rb").read()
        if str(turtle, 'utf-8') == str(previous_turtle, 'utf-8'):
            logging.info("      The downloaded file is the same as before. Skip upload.")
            return ""
        else:
            logging.info("      The downloaded file is different from before.")
            f = open('pharmaTrial_previous.ttl', "w", encoding="utf-8")
            f.write(str(turtle, 'utf-8'))
            f.close()
    else:
        logging.info("      This is the first download.")
        f = open('pharmaTrial_previous.ttl', "w", encoding="utf-8")
        f.write(str(turtle, 'utf-8'))
        f.close()

    if stepwise_confirmation: input("Press Enter to continue...")

    logging.info("")
    logging.info("  Upload Pharma Trial")
    logging.info("")

    logging.info(f"    10. FETCH CATALOG TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    dataset_id=""
    response_json=call_endpoint(f"{provider_url_and_management_port}/management/v3/catalog/request", json.dumps(fetch_catalog))
    jsonpath_expr = jsonpath_ng.ext.parse(f"$.\"dcat:dataset\"[?id = \"pharmaTrialFile\"].\"odrl:hasPolicy\".\"@id\"")
    dataset_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Dataset ID: {dataset_id}")
    if (not dataset_id or not dataset_id.startswith("MQ")):
        logging.error(f"      Found an unexpected kind of dataset identifier: {dataset_id}")
        return ""

    logging.info("")
    logging.info(f"    11. NEGOTIATE CONTRACT TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    negotiation_id=""
    negotiate_contract_target_file_pharma_trial=json.loads(json.dumps(negotiate_contract_target_file_pharma_trial).replace("{{DATASET_ID}}", dataset_id))
    logging.debug(f"      negotiate_contract_target_file_pharma_trial as json:\n{json.dumps(negotiate_contract_target_file_pharma_trial, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations", json.dumps(negotiate_contract_target_file_pharma_trial))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    negotiation_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Negotiation ID: {negotiation_id}")
    if (not negotiation_id or not is_valid_uuid(negotiation_id)):
        logging.error(f"      Found an unexpected kind of negotiation identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    12. GET AGREEMENT ID TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the agreement identifier
    endtime = time.time() + timeout_agreement
    count=0
    agreement_id=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations/{negotiation_id}")
        jsonpath_expr = jsonpath_ng.ext.parse('$.contractAgreementId')
        agreement_id=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Agreement ID: {agreement_id}")
        if (not agreement_id or not is_valid_uuid(agreement_id)):
            if (time.time()+1 < endtime):
                logging.info(f"          no agreement identifier found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not agreement_id or not is_valid_uuid(agreement_id)):
        logging.error(f"      Found an unexpected kind of agreement identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    13. START TRANSFER TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    transfer_id=""
    start_transfer_target_file_pharma_trial=json.loads(json.dumps(start_transfer_target_file_pharma_trial).replace("{{CONTRACT_ID}}", agreement_id))
    logging.debug(f"      start_transfer_target_file_pharma_trial as json:\n{json.dumps(start_transfer_target_file_pharma_trial, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/transferprocesses", json.dumps(start_transfer_target_file_pharma_trial))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    transfer_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Transfer ID: {transfer_id}")
    if (not transfer_id or not is_valid_uuid(transfer_id)):
        logging.error(f"      Found an unexpected kind of transfer identifier: {transfer_id}")
        return ""

    logging.info("")
    logging.info(f"    14. GET ENDPOINT DATA REFERENCE TARGET FILE")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the endpoint data reference
    endtime = time.time() + timeout_transfer
    count=0
    data_endpoint=None
    token=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/edrs/{transfer_id}/dataaddress")
        jsonpath_expr = jsonpath_ng.ext.parse('$.endpoint')
        data_endpoint=try_find_value_in_json(jsonpath_expr, response_json)
        jsonpath_expr = jsonpath_ng.ext.parse('$.authorization')
        token=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Endpoint: {data_endpoint} Token: {token[:8] if token else None}...")
        if (not data_endpoint or not token):
            if (time.time()+1 < endtime):
                logging.info(f"          no data endpoint found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not data_endpoint or not token):
        logging.error(f"      Found an unexpected data endpoint: {data_endpoint} with token: {token}")
        return ""

    logging.info("")
    logging.info(f"    15. PUSH THE DATA TO ACCURIDS API HOSPITAL FILE UPLOAD")
    if stepwise_confirmation: input("Press Enter to continue...")

    #FILE MULTIPART
    boundary = "---------888888888"
    file_content = open('pharmaTrial.ttl', "rb").read()
    body = f"""\r\n\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"upload\"; filename=\"pharmaTrial.ttl\"\r\nContent-Type: application/octet-stream\r\n\r\n{file_content.decode("utf-8")}\r\n--{boundary}--\r\n"""

    logging.debug(f"      Body:\n|START|{body}|END|")
    content_length=str(len(body))
    logging.debug(f"      Content-Length: {content_length}")

    # Headers
    headers = {
        "Authorization": token,
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": content_length
    }
    logging.debug(f"      Request Headers:\n{headers}")

    response = requests.post(url=data_endpoint, headers={"Authorization": token, "Content-Type": f"multipart/form-data; boundary={boundary}", "Content-Length": f"{content_length}" }, data=body)

    logging.debug(f"      Response Headers:\n{pretty_repr(dict(response.headers))}")
    logging.debug(f"      Response Content:\n{pretty_repr(response.content)}")

    if (not response.content or not b'success' in response.content):
        logging.error(f"        File upload failed.")
        return ""
    else:
        logging.debug(f"        File upload complete.")

    logging.info("")
    logging.info(f"    16. FETCH CATALOG TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    dataset_id=""
    response_json=call_endpoint(f"{provider_url_and_management_port}/management/v3/catalog/request", json.dumps(fetch_catalog))
    jsonpath_expr = jsonpath_ng.ext.parse(f"$.\"dcat:dataset\"[?id = \"pharmaGraphql\"].\"odrl:hasPolicy\".\"@id\"")
    dataset_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Dataset ID: {dataset_id}")
    if (not dataset_id or not dataset_id.startswith("MQ")):
        logging.error(f"      Found an unexpected kind of dataset identifier: {dataset_id}")
        return ""

    logging.info("")
    logging.info(f"    17. NEGOTIATE CONTRACT TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    negotiation_id=""
    negotiate_contract_target_graphql_pharma=json.loads(json.dumps(negotiate_contract_target_graphql_pharma).replace("{{DATASET_ID}}", dataset_id))
    logging.debug(f"      negotiate_contract_target_graphql_pharma as json:\n{json.dumps(negotiate_contract_target_graphql_pharma, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations", json.dumps(negotiate_contract_target_graphql_pharma))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    negotiation_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Negotiation ID: {negotiation_id}")
    if (not negotiation_id or not is_valid_uuid(negotiation_id)):
        logging.error(f"      Found an unexpected kind of negotiation identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    18. GET AGREEMENT ID TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the agreement identifier
    endtime = time.time() + timeout_agreement
    count=0
    agreement_id=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/contractnegotiations/{negotiation_id}")
        jsonpath_expr = jsonpath_ng.ext.parse('$.contractAgreementId')
        agreement_id=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Agreement ID: {agreement_id}")
        if (not agreement_id or not is_valid_uuid(agreement_id)):
            if (time.time()+1 < endtime):
                logging.info(f"          no agreement identifier found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not agreement_id or not is_valid_uuid(agreement_id)):
        logging.error(f"      Found an unexpected kind of agreement identifier: {negotiation_id}")
        return ""

    logging.info("")
    logging.info(f"    19. START TRANSFER TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    transfer_id=""
    start_transfer_target_graphql_pharma=json.loads(json.dumps(start_transfer_target_graphql_pharma).replace("{{CONTRACT_ID}}", agreement_id))
    logging.debug(f"      start_transfer_target_graphql_pharma as json:\n{json.dumps(start_transfer_target_graphql_pharma, indent=4, sort_keys=True)}")
    response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/transferprocesses", json.dumps(start_transfer_target_graphql_pharma))
    jsonpath_expr = jsonpath_ng.ext.parse('$."@id"')
    transfer_id=try_find_value_in_json(jsonpath_expr, response_json)
    logging.info(f"        Transfer ID: {transfer_id}")
    if (not transfer_id or not is_valid_uuid(transfer_id)):
        logging.error(f"      Found an unexpected kind of transfer identifier: {transfer_id}")
        return ""

    logging.info("")
    logging.info(f"    20. GET ENDPOINT DATA REFERENCE TARGET GRAPHQL")
    if stepwise_confirmation: input("Press Enter to continue...")
    # poll for the endpoint data reference
    endtime = time.time() + timeout_transfer
    count=0
    data_endpoint=None
    token=None
    while time.time() < endtime:
        count+=1
        response_json = call_endpoint(f"{consumer_url_and_management_port}/management/v3/edrs/{transfer_id}/dataaddress")
        jsonpath_expr = jsonpath_ng.ext.parse('$.endpoint')
        data_endpoint=try_find_value_in_json(jsonpath_expr, response_json)
        jsonpath_expr = jsonpath_ng.ext.parse('$.authorization')
        token=try_find_value_in_json(jsonpath_expr, response_json)
        logging.info(f"        Endpoint: {data_endpoint} Token: {token[:8] if token else None}...")
        if (not data_endpoint or not token):
            if (time.time()+1 < endtime):
                logging.info(f"          no data endpoint found, poll again in a second ({count})")
                time.sleep(1)
            else:
                logging.info(f"        timeout reached")
        else:
            break
    if (not data_endpoint or not token):
        logging.error(f"      Found an unexpected data endpoint: {data_endpoint} with token: {token}")
        return ""

    logging.info("")
    logging.info(f"    21. PUSH THE DATA TO ACCURIDS API HOSPITAL DATASET UPDATE")
    if stepwise_confirmation: input("Press Enter to continue...")

    sources = f'{{type: FILE, fileName: "{os.path.basename('pharmaTrial.ttl')}"}},'
    sources = sources[:-1]

    mutation = """
        mutation {
            updateDataset(
                tag: "clinical-trial",
                name: "Clinical Trial dataset",
                description: "",
                datasetSources: [%s]
                append: false
            ) {
                id
            }
        }
    """ % (
        sources
    )

    logging.debug(f"      query: {mutation}")
    response = requests.post(url=data_endpoint, headers={"Authorization": token}, json={"query": mutation})
    logging.debug(f"      Response Headers:\n{pretty_repr(dict(response.headers))}")
    logging.debug(f"      Response Content:\n{pretty_repr(response.content)}")
    if not b'{"errors"' in response.content:
        logging.info("        Dataset upload done.")
    else:
        logging.debug(f"      Updating the dataset failed. Trying to create a new one.")

        mutation = """
            mutation {
                createDataset(
                    tag: "clinical-trial",
                    name: "Clinical Trial dataset",
                    description: "",
                    datasetSources: [%s]
                ) {
                    id
                }
            }
        """ % (
            sources
        )

        logging.debug(f"      query: {mutation}")
        response = requests.post(url=data_endpoint, headers={"Authorization": token}, json={"query": mutation})
        logging.debug(f"      Response Headers:\n{pretty_repr(dict(response.headers))}")
        logging.debug(f"      Response Content:\n{pretty_repr(response.content)}")
        if not b'{"errors"' in response.content:
            logging.info("        Dataset upload done.")
        else:
            logging.error("        Dataset upload failed.")
            return ""

### Execute the workflow

cycle=1
while True:
    logging.info("")
    logging.info(f"UPDATE CYCLE {cycle:05}")
    pharma_reference_data()
    pharma_shapes()
    pharma_trial()
    hospital_human_biosample()
    hospital_patient_collaboration()
    cycle+=1

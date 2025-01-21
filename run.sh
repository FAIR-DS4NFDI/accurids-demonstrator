#!/bin/bash

echo "Starting the Provider..."
java -Dedc.keystore=./certs/cert.pfx -Dedc.keystore.password=123456 -Dedc.fs.config=./config/provider-configuration.properties -jar accurids-connector.jar > provider.log 2>&1 &

sleep 5

echo "Starting the Consumer..."
java -Dedc.keystore=./certs/cert.pfx -Dedc.keystore.password=123456 -Dedc.fs.config=./config/consumer-configuration.properties -jar accurids-connector.jar > consumer.log 2>&1 &

sleep 5

echo "Starting the Demonstrator Manager Service..."
python ./edc_demo.py

wait -n

exit $?
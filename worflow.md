

Web frontend ----> Api ----> S3 -----|Trigger| -----> lambda_ --->cluster de EC2 (iA) ----> lambda |recoger los datos y almacenar|  ---> DynamoDB  ----> API GATEWAY -----> web frontend //solo los tuyos y otra view todos 
                             |      
                             |
                             |--trigger--> lambda --> sqs ---> email

posible?

recursos:
https://webrtc.org/
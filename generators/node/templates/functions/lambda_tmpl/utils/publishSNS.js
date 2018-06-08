const SNS = require("aws-sdk/clients/sns");

export default ({
  jsonMsg,
  topicArn,
  summaryStr="SNS summary"
}) => {
  console.log("publishing SNS");
  return new Promise((resolve, reject) => {
    const params = {
      TopicArn=topicArn,
      Message=JSON.stringify(jsonMsg),
      MessageStructure='string',
      MessageAttributes={
        'summary': {
            'StringValue': summaryStr,
            'DataType': 'String'
          }
      }
    };
    SNS.publish(params)
      .then((data) => {
        resolve(data);
      })
      .catch(reject);
  });
}

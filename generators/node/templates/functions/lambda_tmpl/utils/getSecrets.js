const SecretsManager = require("aws-sdk/clients/secretsmanager");

module.export = ({secretId, region="us-east-1"}) => {
  console.log("Getting secrets");
  const endpoint = `https://secretsmanager.${region}.amazonaws.com`;
  return new Promise((resolve, reject) => {
    const params = {
      endpoint: endpoint,
      region: region
    };
    new SecretsManager(params)
      .getSecretValue({ SecretId: secretId })
      .then((data) => {
        resolve(data);
      })
      .catch(reject);
  })
}

const SecretsManager = require("aws-sdk/clients/secretsmanager");

export default ({secretId, region}) => {
  console.log("Getting secrets");
  const endpointURL = `https://secretsmanager.${region}.amazonaws.com`;
  return new Promise((resolve, reject) => {
    new SecretsManager({
      endpoint: endpoint,
      region: region
    })
    .getSecretValue({ SecretId: secretId })
    .then((data) => {
      resolve(data);
    })
    .catch(reject);
  })
}

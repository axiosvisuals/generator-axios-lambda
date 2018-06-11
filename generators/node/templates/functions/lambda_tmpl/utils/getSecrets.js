const SecretsManager = require("aws-sdk/clients/secretsmanager");

module.exports = async (secretId, region="us-east-1") => {
  console.log("Getting secrets");
  const sm = new SecretsManager({ region: region });
  try {
    const secretsData = await sm.getSecretValue({ SecretId: secretId }).promise();
    return secretsData;
  } catch (error) {
    console.error("Error getting secrets");
    console.error(error);
  }
}

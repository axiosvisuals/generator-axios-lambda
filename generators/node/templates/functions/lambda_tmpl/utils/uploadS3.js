const S3 = require("aws-sdk/clients/s3");

module.export = ({
  data,
  filename,
  bucket,
  s3Client=S3,
  acl='private'
}) => {
  console.log("uploading to S3");
  return new Promise((resolve, reject) => {
    const params = {
      "Bucket": bucket,
      "Key": filename,
      "Body": data,
      "Metadata": {'Content-Type': 'application/json'},
      "ACL": acl
    };
    S3.putObject(params)
    .then((data) => {
      resolve(data);
    })
    .catch(reject);
  });
}

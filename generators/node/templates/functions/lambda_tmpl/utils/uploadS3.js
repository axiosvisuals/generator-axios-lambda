const S3 = require("aws-sdk/clients/s3");

export default ({
  data,
  filename,
  bucket,
  s3Client=S3,
  acl='private'
}) => {
  console.log("uploading to S3");
  return new Promise((resolve, reject) => {
    S3.putObject({
      Bucket=bucket,
      Key=filename,
      Body=data,
      Metadata={'Content-Type': 'application/json'},
      ACL=acl
    })
    .then((data) => {
      resolve(data);
    })
    .catch(reject);
  });
}

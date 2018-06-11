// const AWS = require("aws-sdk");

// MUST export "handle" function
exports.handle = async (e, ctx, cb) => {
  console.log('processing event: %j', e);
  cb(null, { hello: e.hello });
};
